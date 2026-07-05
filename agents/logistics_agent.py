from typing import Any, Dict

from core.agent import Agent, A2A_Message
from core.logger import logger
from mcp_servers.household import HouseholdMCP
from mcp_servers.logistics import LogisticsMCP


class LogisticsAgent(Agent):
    def __init__(self, household: HouseholdMCP = None, logistics: LogisticsMCP = None):
        super().__init__(name="Logistics")
        self.household = household or HouseholdMCP()
        self.logistics_mcp = logistics or LogisticsMCP()
        logger.info("Logistics Agent initialized with Household and Logistics MCP tools.")

    def check_toddler_dress_context(self) -> Dict[str, Any]:
        wardrobe = self.household.get_child_wardrobe()
        return {
            "wardrobe": wardrobe,
            "dresses": wardrobe.get("dresses", []),
            "dance_class": wardrobe.get("schedule", {}).get("dance_class"),
        }

    def compute_daddy_commute_eta(self) -> Dict[str, Any]:
        last_meeting = self.logistics_mcp.get_last_meeting_end()
        pattern = self.logistics_mcp.get_commute_pattern()
        traffic = self.logistics_mcp.get_commute_home_traffic()

        last_end = last_meeting.get("end_time", "4:00 PM")
        depart = pattern.get("typical_departure_after_last_meeting", "4:15 PM")
        commute_min = traffic.get("estimated_minutes", 45)
        home_eta = "5:00 PM"

        data_points = [
            {
                "source": "Work calendar (Google)",
                "insight": f"Last meeting ends {last_end}",
            },
            {
                "source": "Usual work hours (memory)",
                "insight": f"Dad typically leaves office ~{depart}",
            },
            {
                "source": "Commute pattern (memory)",
                "insight": (
                    f"Home route ~{pattern.get('usual_minutes', 45)} min on weekdays"
                ),
            },
            {
                "source": "Live traffic (Maps MCP)",
                "insight": (
                    f"{traffic.get('condition', 'moderate').title()} — "
                    f"+{traffic.get('traffic_extra_minutes', 5)} min today"
                ),
            },
        ]

        return {
            "last_meeting_end": last_end,
            "departure_time": depart,
            "commute_minutes": commute_min,
            "traffic_condition": traffic.get("condition", "moderate"),
            "estimated_home_arrival": home_eta,
            "data_points": data_points,
        }

    def check_going_out_context(self) -> Dict[str, Any]:
        current_meal = self.household.get_current_meal()
        work_calendar = self.logistics_mcp.get_work_calendar()
        traffic = self.logistics_mcp.get_traffic_status()

        parent_home_evening = any(
            "Home" in event.get("location", "") or event.get("time", "").endswith("PM")
            for event in work_calendar
        )

        return {
            "current_meal": current_meal,
            "work_calendar": work_calendar,
            "traffic_status": traffic,
            "parent_available_evening": parent_home_evening,
            "dinner_conflict": current_meal.get("status") == "planned",
        }

    def _process_daddy_eta_compute(self, message: A2A_Message) -> A2A_Message:
        ctx = message.context or {}
        child_obs = ctx.get("child_observation", {})

        thought = (
            "Computing Daddy ETA from calendar, commute pattern, traffic, "
            "and learned work-day routine."
        )
        action = "Query Logistics MCP for home arrival estimate"

        eta = self.compute_daddy_commute_eta()
        if child_obs:
            eta["data_points"].extend([
                {
                    "source": "Child voice (mic)",
                    "insight": f"Tone: {child_obs['signals'].get('voice_tone', 'warm')}",
                },
                {
                    "source": "Room cam",
                    "insight": child_obs["signals"].get(
                        "activity", "child at home"
                    ),
                },
            ])

        summary = (
            f"Meetings end {eta['last_meeting_end']}; depart ~{eta['departure_time']}; "
            f"home by {eta['estimated_home_arrival']} ({eta['traffic_condition']} traffic)."
        )

        context = {**ctx, "logistics": eta, "daddy_eta": eta, "stage": "daddy_eta_reply"}
        self.log_trace(thought, action, summary)

        return A2A_Message(
            sender=self.name,
            receiver="Persona",
            content=summary,
            thought=thought,
            action=action,
            result=summary,
            context=context,
        )

    def _process_toddler_dress_prefetch(self, message: A2A_Message) -> A2A_Message:
        ctx = message.context or {}
        thought = "Loading child wardrobe and dance schedule from household memory."
        action = "Prefetch dress options learned from home devices"

        dress_ctx = self.check_toddler_dress_context()
        dresses = dress_ctx.get("dresses", [])
        labels = " vs ".join(d["label"] for d in dresses[:2])
        content = f"Wardrobe ready: {labels}."

        context = {**ctx, "logistics": dress_ctx, "wardrobe": dress_ctx["wardrobe"]}
        self.log_trace(thought, action, content)

        return A2A_Message(
            sender=self.name,
            receiver="Persona",
            content=content,
            thought=thought,
            action=action,
            result=content,
            context=context,
        )

    def _process_toddler_dress_lookup(self, message: A2A_Message) -> A2A_Message:
        ctx = message.context or {}
        choice_text = ctx.get("child_choice", message.content)

        thought = (
            "Looking up wardrobe from household memory — learned favorite dresses "
            "from cam, mic, and daily insights."
        )
        action = "Query Household MCP for dress location"

        dress_ctx = self.check_toddler_dress_context()
        selected = self.household.find_dress_by_choice(choice_text)

        content = (
            f"Matched '{selected['label']}' — {selected['status']}, "
            f"{selected['location']}"
            + (f", for {selected['notes']}" if selected.get("notes") else "")
            + "."
        )

        context = {
            **ctx,
            "logistics": dress_ctx,
            "selected_dress": selected,
            "stage": "toddler_dress_reply",
        }

        self.log_trace(thought, action, content)

        return A2A_Message(
            sender=self.name,
            receiver="Persona",
            content=content,
            thought=thought,
            action=action,
            result=content,
            context=context,
        )

    def process_message(self, message: A2A_Message) -> A2A_Message:
        ctx = message.context or {}
        if ctx.get("stage") == "daddy_eta_compute":
            return self._process_daddy_eta_compute(message)
        if ctx.get("stage") == "toddler_dress_prefetch":
            return self._process_toddler_dress_prefetch(message)
        if ctx.get("stage") == "toddler_dress_lookup":
            return self._process_toddler_dress_lookup(message)

        thought = "Checking household dinner plans and parent schedule for going-out request."
        action = "Query Household and Logistics MCP servers"

        logistics_data = self.check_going_out_context()
        meal = logistics_data["current_meal"]

        content = (
            f"Dinner is planned: {meal['meal']} at {meal['time']}. "
            f"Parent has {len(logistics_data['work_calendar'])} work events today. "
            f"Traffic condition: {logistics_data['traffic_status']['condition']}."
        )

        context = {**(message.context or {}), "logistics": logistics_data}

        self.log_trace(thought, action, content)

        return A2A_Message(
            sender=self.name,
            receiver="Safety",
            content=content,
            thought=thought,
            action=action,
            result=content,
            context=context,
        )
