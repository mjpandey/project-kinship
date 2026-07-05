import os
import re
from typing import Any, Dict, Optional

from core.agent import Agent, A2A_Message
from core.logger import logger
from core.memory import VectorMemory, format_hour

DISTRESS_KEYWORDS = (
    "panic", "panicking", "freaking out", "scared", "anxious",
    "help me", "emergency", "hurt", "crying", "can't breathe",
)


class SafetyAgent(Agent):
    DEFAULT_CURFEW_HOUR = 20  # 8 PM

    def __init__(self, curfew_hour: int = None, memory: VectorMemory = None):
        super().__init__(name="Safety")
        self.memory = memory
        self.curfew_hour = curfew_hour or self._resolve_curfew_hour()
        logger.info(f"Safety Agent initialized. Curfew hour: {self.curfew_hour}:00")

    def _resolve_curfew_hour(self) -> int:
        if self.memory:
            return self.memory.get_curfew_hour()
        return int(os.getenv("CURFEW_HOUR", self.DEFAULT_CURFEW_HOUR))

    def refresh_from_memory(self):
        """Reload curfew and rules from vector memory after parental correction."""
        if self.memory:
            self.curfew_hour = self.memory.get_curfew_hour()
            logger.info(f"Safety Agent refreshed curfew from memory: {self.curfew_hour}:00")

    def _parse_return_hour(self, text: str) -> Optional[int]:
        lower = text.lower()

        match = re.search(r"back\s+(?:by|at)\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", lower)
        if match:
            hour = int(match.group(1))
            meridiem = match.group(3)
            if meridiem == "pm" and hour < 12:
                hour += 12
            elif meridiem == "am" and hour == 12:
                hour = 0
            elif meridiem is None and hour <= 12:
                hour = hour if hour >= 12 else hour + 12 if hour < 8 else hour
            return hour

        match = re.search(r"(\d{1,2})\s*(pm|am)", lower)
        if match:
            hour = int(match.group(1))
            if match.group(2) == "pm" and hour < 12:
                hour += 12
            return hour

        return None

    def _is_distress(self, text: str) -> bool:
        lower = text.lower()
        return any(kw in lower for kw in DISTRESS_KEYWORDS)

    def _is_going_out_request(self, text: str) -> bool:
        lower = text.lower()
        return any(kw in lower for kw in ("go out", "hang out", "friends", "leave", "outside", "meet up"))

    def check_going_out_rules(self, user_input: str, logistics: Dict[str, Any]) -> Dict[str, Any]:
        self.refresh_from_memory()

        if self._is_distress(user_input) and not self._is_going_out_request(user_input):
            return {
                "approved": False,
                "request_type": "distress",
                "curfew": format_hour(self.curfew_hour),
                "reason": None,
                "going_out_request": False,
                "conditions": [],
            }

        requested_hour = self._parse_return_hour(user_input)
        curfew_str = format_hour(self.curfew_hour)

        if requested_hour is not None and requested_hour > self.curfew_hour:
            return {
                "approved": False,
                "curfew": curfew_str,
                "requested_return_hour": requested_hour,
                "reason": f"you wanted to stay out past {curfew_str}, and that's past our cutoff",
                "going_out_request": True,
                "conditions": [],
            }

        conditions = [
            "Stay with your friends and don't go anywhere else without checking in.",
            "Keep your phone on so we can reach you.",
        ]

        meal = logistics.get("current_meal", {})
        if logistics.get("dinner_conflict"):
            conditions.append(
                f"Eat {meal.get('meal', 'dinner')} with the family at {meal.get('time', '6:30 PM')} before you leave."
            )

        return {
            "approved": True,
            "curfew": curfew_str,
            "requested_return_hour": requested_hour,
            "reason": None,
            "going_out_request": True,
            "conditions": conditions,
            "rules_checked": [
                f"Return time before {curfew_str}",
                "Going-out request logged for escalation review",
            ],
        }

    def process_message(self, message: A2A_Message) -> A2A_Message:
        ctx = message.context or {}
        user_input = ctx.get("user_input", message.content)
        logistics = ctx.get("logistics", {})

        thought = f"Verifying going-out rules. Checking curfew ({self.curfew_hour}:00) and return time."
        action = "Run family safety rule checks"

        safety_data = self.check_going_out_rules(user_input, logistics)

        if safety_data.get("request_type") == "distress":
            content = "Distress signal detected — escalate to parent, do not treat as going-out."
        elif safety_data["approved"]:
            content = (
                f"Request approved with conditions. Curfew: {safety_data['curfew']}."
            )
        else:
            content = f"Request denied: {safety_data['reason']}"

        context = {**ctx, "safety": safety_data}

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
