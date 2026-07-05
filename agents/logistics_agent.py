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

    def process_message(self, message: A2A_Message) -> A2A_Message:
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
