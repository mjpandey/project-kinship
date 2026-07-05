from typing import Any, Callable, Dict, List, Optional
import uuid

from core.agent import Agent, A2A_Message
from core.logger import logger, trace_log
from core.memory import VectorMemory, SessionState
from agents.persona_agent import PersonaAgent
from agents.logistics_agent import LogisticsAgent
from agents.safety_agent import SafetyAgent
from agents.watchdog_agent import WatchdogAgent
from agents.reflection_agent import ReflectionAgent
from agents.escalation_agent import EscalationAgent
from mcp_servers.household import HouseholdMCP
from mcp_servers.logistics import LogisticsMCP
from mcp_servers.iot_stream import IoTStreamMCP
from mcp_servers.feedback import ParentalFeedbackMCP

HOUSEHOLD_KEYWORDS = {
    "meal": "current_meal",
    "dinner": "current_meal",
    "lunch": "current_meal",
    "breakfast": "current_meal",
    "food": "current_meal",
    "cook": "current_meal",
    "pasta": "current_meal",
    "grocery": "grocery_list",
    "groceries": "grocery_list",
    "shopping": "grocery_list",
    "store": "grocery_list",
    "laundry": "laundry_status",
    "washer": "laundry_status",
    "dryer": "laundry_status",
    "clothes": "laundry_status",
    "wash": "laundry_status",
}

LOGISTICS_KEYWORDS = {
    "calendar": "work_calendar",
    "schedule": "work_calendar",
    "meeting": "work_calendar",
    "work": "work_calendar",
    "office": "work_calendar",
    "traffic": "traffic_status",
    "commute": "traffic_status",
    "drive": "traffic_status",
    "road": "traffic_status",
    "route": "traffic_status",
}

CATEGORY_KEYWORDS = {
    "household": HOUSEHOLD_KEYWORDS,
    "logistics": LOGISTICS_KEYWORDS,
}


class Orchestrator:
    def __init__(self, persona_type: str = "mommy"):
        self.agents: Dict[str, Agent] = {}
        self.household = HouseholdMCP()
        self.logistics_mcp = LogisticsMCP()
        self.iot_stream = IoTStreamMCP()
        self.persona_type = persona_type
        self._last_proactive_response: Optional[Dict[str, Any]] = None
        self.memory = VectorMemory()
        self.session = SessionState(session_id=str(uuid.uuid4()))
        self.feedback = ParentalFeedbackMCP(on_feedback=self.handle_parental_feedback)
        logger.info("Orchestrator initialized with VectorMemory.")

    def setup_watchdog_agents(self, persona_type: str = None):
        """Register Watchdog, Persona, and Escalation agents for proactive monitoring."""
        persona = persona_type or self.persona_type
        self.register_agent(PersonaAgent(persona_type=persona, memory=self.memory))
        self.register_agent(EscalationAgent(persona_type=persona))
        watchdog = WatchdogAgent(iot_stream=self.iot_stream)
        self.register_agent(watchdog)
        return watchdog

    def _page_parent(self, escalation: Dict[str, Any]) -> None:
        """Silently notify the real parent — never surfaced in persona speech."""
        if not escalation.get("should_page_parent"):
            return
        trace_log(
            "Orchestrator",
            f"Paging {escalation.get('parent_target')} — urgency {escalation.get('urgency')}.",
            "Send alert to human parent",
            escalation.get("page_message"),
        )
        logger.info(escalation.get("page_message"))

    def run_proactive_intervention(self, alert: Dict[str, Any]) -> Dict[str, Any]:
        """
        Proactive flow: IoT alert -> Watchdog (already detected) -> Orchestrator interrupt -> Persona warning.
        """
        if "Persona" not in self.agents:
            self.setup_watchdog_agents()

        logger.info(f"Proactive intervention triggered: {alert.get('event_type')}")
        trace: List[Dict[str, str]] = []

        trace.append({
            "agent": "Watchdog",
            "stage": "detect_danger",
            "thought": f"Danger detected: {alert.get('description')}",
            "action": "Escalate to Orchestrator",
            "output": f"ALERT: {alert.get('description')} at {alert.get('location')}",
        })

        trace_log(
            "Orchestrator",
            f"Interrupting idle state — {alert.get('threat')} detected.",
            "Route alert to Persona for proactive warning",
            alert.get("description"),
        )
        trace.append({
            "agent": "Orchestrator",
            "stage": "interrupt",
            "thought": f"Proactive interrupt for {alert.get('event_type')}",
            "action": "Forward to Persona with alert context",
            "output": "Interrupt initiated",
        })

        persona_msg = A2A_Message(
            sender="Orchestrator",
            receiver="Persona",
            content="",
            thought="Proactive safety alert — no user input.",
            action="Issue watchful voice warning",
            context={"stage": "alert", "alert": alert, "proactive": True},
        )
        persona_step = self.agents["Persona"].process_message(persona_msg)
        trace.append({
            "agent": "Persona",
            "stage": "alert_warning",
            "thought": persona_step.thought,
            "action": persona_step.action,
            "output": persona_step.content,
        })

        if "Escalation" not in self.agents:
            self.register_agent(EscalationAgent(persona_type=self.persona_type))

        escalation_msg = A2A_Message(
            sender="Orchestrator",
            receiver="Escalation",
            content="",
            thought="Evaluate whether to page human parent for IoT alert.",
            action="Run escalation grounding rules",
            context={"stage": "escalate", "alert": alert, "proactive": True},
        )
        escalation_step = self.agents["Escalation"].process_message(escalation_msg)
        escalation = (escalation_step.context or {}).get("escalation", {})
        self._page_parent(escalation)
        trace.append({
            "agent": "Escalation",
            "stage": "evaluate_paging",
            "thought": escalation_step.thought,
            "action": escalation_step.action,
            "output": escalation_step.content,
        })

        result = {
            "response": persona_step.content,
            "alert": alert,
            "proactive": True,
            "tone": "watchful",
            "paged_parent": escalation.get("should_page_parent", False),
            "escalation": escalation,
            "trace": trace,
        }
        self._last_proactive_response = result
        return result

    def start_watchdog(
        self,
        on_warning: Optional[Callable[[Dict[str, Any]], None]] = None,
        persona_type: str = None,
    ) -> WatchdogAgent:
        """Start the Watchdog background listener on the IoT stream."""
        watchdog = self.agents.get("Watchdog")
        if not watchdog:
            watchdog = self.setup_watchdog_agents(persona_type)

        def _handle_alert(alert: Dict[str, Any]):
            result = self.run_proactive_intervention(alert)
            if on_warning:
                on_warning(result)

        watchdog.set_alert_callback(_handle_alert)
        watchdog.start_listening()
        return watchdog

    def stop_watchdog(self):
        if "Watchdog" in self.agents:
            self.agents["Watchdog"].stop_listening()
        self.iot_stream.stop()

    def simulate_iot_danger(self, scenario: str = "door") -> Dict[str, Any]:
        """Simulate an IoT danger event and run the full proactive flow synchronously."""
        event = self.iot_stream.simulate_danger_scenario(scenario)
        if "Watchdog" not in self.agents:
            self.setup_watchdog_agents()

        watchdog_msg = A2A_Message(
            sender="IoTStream",
            receiver="Watchdog",
            content=event.get("event_type", ""),
            thought="",
            action="",
            context={"iot_event": event},
        )
        watchdog_step = self.agents["Watchdog"].process_message(watchdog_msg)
        alert = (watchdog_step.context or {}).get("alert")
        if not alert:
            return {"response": "No danger detected.", "proactive": False, "trace": []}
        return self.run_proactive_intervention(alert)


    def setup_hero_agents(self, persona_type: str = None):
        """Register Persona, Logistics, Safety, and Escalation agents for the hero flow."""
        persona = persona_type or self.persona_type
        self.register_agent(PersonaAgent(persona_type=persona, memory=self.memory))
        self.register_agent(
            LogisticsAgent(household=self.household, logistics=self.logistics_mcp)
        )
        self.register_agent(SafetyAgent(memory=self.memory))
        self.register_agent(EscalationAgent(persona_type=persona))

    def setup_memory_agents(self, persona_type: str = None):
        """Register all agents needed for Phase 4 memory + learning flows."""
        self.setup_hero_agents(persona_type)
        self.register_agent(ReflectionAgent(memory=self.memory))

    def ensure_demo_baseline(self):
        """Reset curfew to default 8 PM so learning demos start from the right baseline."""
        if "Reflection" not in self.agents:
            self.setup_memory_agents()
        self.memory.reset_to_demo_defaults()
        if "Safety" in self.agents:
            self.agents["Safety"].refresh_from_memory()
        curfew = self.memory.get_personality().get("rules", {}).get("curfew", "8:00 PM")
        logger.info(f"Demo baseline ready — curfew {curfew}")

    def handle_parental_feedback(
        self, correction: str, context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Parental feedback entry point — routes to Reflection Agent."""
        return self.run_feedback_flow(correction, context)

    def run_feedback_flow(
        self, correction: str, context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Parental feedback -> Reflection Agent (analyze + update VectorMemory)
        -> Safety Agent refresh.
        """
        if "Reflection" not in self.agents:
            self.setup_memory_agents()

        logger.info(f"Starting feedback flow: {correction}")
        trace: List[Dict[str, str]] = []

        feedback_msg = A2A_Message(
            sender="Parent",
            receiver="Reflection",
            content=correction,
            thought="Parent is correcting the agent's behavior.",
            action="Submit correction for reflection",
            context=context or {},
        )
        reflection_step = self.agents["Reflection"].process_message(feedback_msg)
        trace.append({
            "agent": "Reflection",
            "stage": "analyze_correction",
            "thought": reflection_step.thought,
            "action": reflection_step.action,
            "output": reflection_step.content,
        })

        if "Safety" in self.agents:
            self.agents["Safety"].refresh_from_memory()
            trace.append({
                "agent": "Safety",
                "stage": "refresh_rules",
                "thought": "Reloaded curfew and rules from updated vector memory.",
                "action": "Apply learned rules",
                "output": f"Curfew now {self.memory.get_curfew_hour()}:00",
            })

        self.session.add_message("parent", correction)
        self.session.add_message("reflection", reflection_step.content)

        trace_log(
            "Orchestrator",
            "Feedback flow completed — memory updated.",
            "Persist correction for future interactions",
            reflection_step.content,
        )

        learned = (reflection_step.context or {}).get("learned_rules", {})
        return {
            "response": reflection_step.content,
            "learned_rules": learned,
            "personality": self.memory.get_personality(),
            "trace": trace,
        }

    def run_hero_flow(self, user_input: str, persona_type: str = None) -> Dict[str, Any]:
        """
        Multi-agent flow for the Dinner/Going Out hero scenario:
        Input -> Persona (mood) -> Logistics (data) -> Safety (rules) -> Persona (final).
        """
        if "Persona" not in self.agents:
            self.setup_memory_agents(persona_type)

        logger.info(f"Starting hero flow for: {user_input}")
        trace: List[Dict[str, str]] = []

        # Step 1: Persona analyzes mood
        persona_msg = A2A_Message(
            sender="User",
            receiver="Persona",
            content=user_input,
            thought="",
            action="",
            context={"stage": "analyze", "user_input": user_input},
        )
        persona_step = self.agents["Persona"].process_message(persona_msg)
        trace.append({
            "agent": "Persona",
            "stage": "analyze_mood",
            "thought": persona_step.thought,
            "action": persona_step.action,
            "output": persona_step.content,
        })

        # Step 2: Logistics checks mock data
        logistics_msg = A2A_Message(
            sender="Persona",
            receiver="Logistics",
            content=user_input,
            thought=persona_step.thought,
            action="Forward to Logistics",
            context=persona_step.context,
        )
        logistics_step = self.agents["Logistics"].process_message(logistics_msg)
        trace.append({
            "agent": "Logistics",
            "stage": "check_data",
            "thought": logistics_step.thought,
            "action": logistics_step.action,
            "output": logistics_step.content,
        })

        # Step 3: Safety verifies rules
        safety_msg = A2A_Message(
            sender="Logistics",
            receiver="Safety",
            content=user_input,
            thought=logistics_step.thought,
            action="Forward to Safety",
            context=logistics_step.context,
        )
        safety_step = self.agents["Safety"].process_message(safety_msg)
        trace.append({
            "agent": "Safety",
            "stage": "verify_rules",
            "thought": safety_step.thought,
            "action": safety_step.action,
            "output": safety_step.content,
        })

        # Step 4: Escalation decides whether to page the real parent (behind the scenes)
        escalation_msg = A2A_Message(
            sender="Safety",
            receiver="Escalation",
            content=user_input,
            thought=safety_step.thought,
            action="Evaluate paging need",
            context=safety_step.context,
        )
        escalation_step = self.agents["Escalation"].process_message(escalation_msg)
        escalation = (escalation_step.context or {}).get("escalation", {})
        self._page_parent(escalation)
        trace.append({
            "agent": "Escalation",
            "stage": "evaluate_paging",
            "thought": escalation_step.thought,
            "action": escalation_step.action,
            "output": escalation_step.content,
        })

        # Step 5: Persona composes final negotiation (human voice, no paging talk)
        final_ctx = {**(escalation_step.context or {}), "stage": "final"}
        final_msg = A2A_Message(
            sender="Safety",
            receiver="Persona",
            content=user_input,
            thought=safety_step.thought,
            action="Forward to Persona for final response",
            context=final_ctx,
        )
        final_step = self.agents["Persona"].process_message(final_msg)
        trace.append({
            "agent": "Persona",
            "stage": "final_response",
            "thought": final_step.thought,
            "action": final_step.action,
            "output": final_step.content,
        })

        trace_log(
            "Orchestrator",
            "Hero flow completed successfully.",
            "Return final Persona negotiation",
            final_step.content,
        )

        self.session.add_message("user", user_input)
        self.session.add_message("assistant", final_step.content)

        return {
            "response": final_step.content,
            "approved": (safety_step.context or {}).get("safety", {}).get("approved"),
            "curfew": self.memory.get_personality().get("rules", {}).get("curfew"),
            "paged_parent": escalation.get("should_page_parent", False),
            "escalation": escalation,
            "trace": trace,
        }


    def register_agent(self, agent: Agent):
        self.agents[agent.name] = agent
        logger.info(f"Registered agent: {agent.name}")

    def _classify_category(self, user_input: str) -> str:
        text = user_input.lower()
        household_score = sum(1 for kw in HOUSEHOLD_KEYWORDS if kw in text)
        logistics_score = sum(1 for kw in LOGISTICS_KEYWORDS if kw in text)

        if household_score > logistics_score:
            return "household"
        if logistics_score > household_score:
            return "logistics"
        return "unknown"

    def _pick_tool(self, category: str, user_input: str) -> str:
        text = user_input.lower()
        keywords = CATEGORY_KEYWORDS[category]
        for keyword, tool in keywords.items():
            if keyword in text:
                return tool
        return "all"

    def _fetch_household_data(self, tool: str) -> Any:
        if tool == "current_meal":
            return self.household.get_current_meal()
        if tool == "grocery_list":
            return self.household.get_grocery_list()
        if tool == "laundry_status":
            return self.household.get_laundry_status()
        return self.household.get_all()

    def _fetch_logistics_data(self, tool: str) -> Any:
        if tool == "work_calendar":
            return self.logistics_mcp.get_work_calendar()
        if tool == "traffic_status":
            return self.logistics_mcp.get_traffic_status()
        return self.logistics_mcp.get_all()

    def route_request(self, user_input: str) -> str:
        """Route text input to the Household or Logistics mock MCP tool."""
        logger.info(f"Received user request: {user_input}")
        category = self._classify_category(user_input)

        if category == "unknown":
            thought = "Could not determine whether this is a household or logistics request."
            action = "Return clarification prompt"
            result = (
                "I'm not sure if that's about the household or logistics. "
                "Try asking about dinner, groceries, laundry, work schedule, or traffic."
            )
            trace_log("Orchestrator", thought, action, result)
            return result

        tool = self._pick_tool(category, user_input)
        thought = f"Classified request as {category}; selected tool '{tool}'."
        action = f"Call {category.title()} MCP"

        if category == "household":
            data = self._fetch_household_data(tool)
        else:
            data = self._fetch_logistics_data(tool)

        result = f"[{category.upper()}] {data}"
        trace_log("Orchestrator", thought, action, result)
        return result

    def handle_a2a(self, message: A2A_Message) -> str:
        """Handles communication between agents."""
        receiver_name = message.receiver

        if receiver_name in self.agents:
            agent = self.agents[receiver_name]
            logger.info(f"Routing message from {message.sender} to {receiver_name}")
            response = agent.process_message(message)
            return response.content

        return "Error: Receiver agent not found."
