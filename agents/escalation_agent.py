"""Decides whether to page the real parent based on conversation criticality."""

from typing import Any, Dict, List, Optional, Set

from core.agent import Agent, A2A_Message
from core.logger import logger

# Grounding rules: signals that may require paging the human parent.
ESCALATION_GROUNDING = {
    "going_out": {
        "keywords": (
            "go out", "hang out", "friends", "leave", "outside",
            "meet up", "sleepover", "party", "drive", "uber",
        ),
        "default_urgency": "medium",
        "page": True,
        "reason": "Child is requesting to leave the home or change plans.",
    },
    "danger": {
        "keywords": (
            "hurt", "bleeding", "fire", "smoke", "stranger", "scared",
            "help me", "emergency", "can't breathe", "unconscious",
        ),
        "default_urgency": "critical",
        "page": True,
        "reason": "Possible immediate danger to the child.",
    },
    "hazard": {
        "keywords": (
            "stove", "gas", "leak", "flood", "electrical", "spark",
            "broken glass", "chemical", "carbon monoxide",
        ),
        "default_urgency": "high",
        "page": True,
        "reason": "Environmental hazard detected or reported.",
    },
    "theft": {
        "keywords": (
            "stole", "stolen", "robbed", "burglar", "break in",
            "broke in", "missing", "someone took",
        ),
        "default_urgency": "high",
        "page": True,
        "reason": "Possible theft or intrusion.",
    },
    "anxious": {
        "keywords": (
            "panic", "anxious", "freaking out", "can't calm down",
            "worried sick", "stressed", "overwhelmed", "crying",
        ),
        "default_urgency": "medium",
        "page": True,
        "reason": "Child appears distressed and may need adult support.",
    },
    "urgency": {
        "keywords": (
            "right now", "hurry", "asap", "urgent", "immediately",
            "911", "call someone", "need you now",
        ),
        "default_urgency": "high",
        "page": True,
        "reason": "Conversation signals time-sensitive urgency.",
    },
}

URGENCY_RANK = {"low": 0, "medium": 1, "high": 2, "critical": 3}

IOT_SEVERITY_URGENCY = {
    "low": "medium",
    "medium": "high",
    "high": "critical",
    "critical": "critical",
}


class EscalationAgent(Agent):
    """
    Analyzes conversation context and decides if the real parent should be paged.
    This decision stays behind the scenes — the Persona never mentions paging.
    """

    def __init__(self, persona_type: str = "mommy"):
        super().__init__(name="Escalation")
        self.persona_type = persona_type
        logger.info("EscalationAgent initialized.")

    def _match_categories(self, text: str) -> Set[str]:
        lower = text.lower()
        return {
            category
            for category, rule in ESCALATION_GROUNDING.items()
            if any(kw in lower for kw in rule["keywords"])
        }

    def _highest_urgency(self, urgencies: List[str]) -> str:
        if not urgencies:
            return "low"
        return max(urgencies, key=lambda u: URGENCY_RANK.get(u, 0))

    def evaluate(
        self,
        user_input: str = "",
        safety: Dict[str, Any] = None,
        alert: Dict[str, Any] = None,
        mood: str = None,
        proactive: bool = False,
    ) -> Dict[str, Any]:
        safety = safety or {}
        alert = alert or {}
        text = user_input or ""

        matched = self._match_categories(text)
        reasons: List[str] = []
        urgencies: List[str] = []
        should_page = False

        for category in matched:
            rule = ESCALATION_GROUNDING[category]
            if rule["page"]:
                should_page = True
                reasons.append(rule["reason"])
                urgencies.append(rule["default_urgency"])

        if safety.get("going_out_request"):
            should_page = True
            reasons.append("Child going-out request requires parent awareness.")
            urgencies.append("medium")

        if safety.get("request_type") == "distress":
            should_page = True
            reasons.append("Child distress signal — parent should be alerted.")
            urgencies.append("high")

        if safety.get("approved") is False and safety.get("request_type") != "distress":
            should_page = True
            reasons.append("Safety rules denied the request — parent should review.")
            urgencies.append("medium")

        if alert:
            severity = alert.get("severity", "medium")
            event = alert.get("event_type", "unknown")
            should_page = True
            reasons.append(f"IoT alert: {alert.get('description', event)}")
            urgencies.append(IOT_SEVERITY_URGENCY.get(severity, "high"))

        if proactive and alert:
            should_page = True

        if mood in ("eager",) and "going_out" in matched:
            urgencies.append("medium")

        urgency = self._highest_urgency(urgencies) if should_page else "low"

        parent_label = "Mommy" if self.persona_type == "mommy" else "Daddy"

        return {
            "should_page_parent": should_page,
            "urgency": urgency,
            "matched_categories": sorted(matched),
            "reasons": reasons,
            "parent_target": parent_label,
            "page_message": self._build_page_message(parent_label, reasons, urgency) if should_page else None,
        }

    def _build_page_message(self, parent: str, reasons: List[str], urgency: str) -> str:
        summary = "; ".join(reasons[:3])
        return f"[PAGE {urgency.upper()}] Notify {parent}: {summary}"

    def process_message(self, message: A2A_Message) -> A2A_Message:
        ctx = message.context or {}
        user_input = ctx.get("user_input", message.content)
        safety = ctx.get("safety", {})
        alert = ctx.get("alert")
        mood = ctx.get("mood")
        proactive = ctx.get("proactive", False)

        escalation = self.evaluate(
            user_input=user_input,
            safety=safety,
            alert=alert,
            mood=mood,
            proactive=proactive,
        )

        thought = (
            f"Evaluated escalation signals. Categories: {escalation['matched_categories']}. "
            f"Urgency={escalation['urgency']}, page={escalation['should_page_parent']}."
        )
        action = "Decide whether to page the real parent"

        if escalation["should_page_parent"]:
            content = escalation["page_message"]
        else:
            content = "No escalation — conversation stays between child and persona."

        self.log_trace(thought, action, content)

        return A2A_Message(
            sender=self.name,
            receiver="Orchestrator",
            content=content,
            thought=thought,
            action=action,
            result=content,
            context={**ctx, "escalation": escalation},
        )
