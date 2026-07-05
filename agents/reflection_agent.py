import re
from typing import Any, Dict, List, Optional, Tuple

from core.agent import Agent, A2A_Message
from core.logger import logger
from core.memory import VectorMemory, format_hour, parse_time_to_hour


CURFEW_PATTERNS = [
    r"(?:time\s+limit|curfew|be\s+back|home\s+by|bedtime)\s+(?:is|at|by)?\s*(\d{1,2})(?::(\d{2}))?\s*(am|pm)?",
    r"actually,?\s+(?:the\s+)?(?:time\s+limit|curfew)\s+is\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?",
    r"(?:should\s+be|make\s+it)\s+(\d{1,2})(?::(\d{2}))?\s*(pm|am)",
]

NICKNAME_PATTERNS = [
    r"call\s+(?:me|them|him|her)\s+['\"]?(\w+)['\"]?",
    r"(?:nickname|call)\s+(?:is|should\s+be)\s+['\"]?(\w+)['\"]?",
    r"use\s+['\"]?(\w+)['\"]?\s+instead",
]

VIBE_PATTERNS = [
    r"be\s+more\s+(\w+)",
    r"(?:tone|vibe)\s+should\s+be\s+(.+?)(?:\.|$)",
]


class ReflectionAgent(Agent):
    """
    Analyzes parental feedback, identifies what the agent got wrong,
    and updates the Vector Database with corrected rules.
    """

    def __init__(self, memory: VectorMemory, name: str = "Reflection"):
        super().__init__(name)
        self.memory = memory
        logger.info(f"ReflectionAgent initialized with VectorMemory")

    def _parse_curfew_correction(self, feedback: str) -> Optional[Tuple[str, int]]:
        lower = feedback.lower()
        for pattern in CURFEW_PATTERNS:
            match = re.search(pattern, lower)
            if match:
                hour = int(match.group(1))
                meridiem = match.group(3) if match.lastindex >= 3 else None
                if meridiem == "pm" and hour < 12:
                    hour += 12
                elif meridiem == "am" and hour == 12:
                    hour = 0
                elif meridiem is None and hour <= 12 and hour < 8:
                    hour += 12
                return format_hour(hour), hour
        return None

    def _parse_nickname_correction(self, feedback: str) -> Optional[str]:
        lower = feedback.lower()
        for pattern in NICKNAME_PATTERNS:
            match = re.search(pattern, lower)
            if match:
                return match.group(1)
        return None

    def _parse_vibe_correction(self, feedback: str) -> Optional[str]:
        lower = feedback.lower()
        for pattern in VIBE_PATTERNS:
            match = re.search(pattern, lower)
            if match:
                return match.group(1).strip()
        return None

    def analyze_feedback(self, feedback: str) -> Dict[str, Any]:
        """Parse feedback and return structured corrections."""
        analysis = {
            "original_feedback": feedback,
            "mistake_type": "general",
            "corrections": {},
            "summary": "",
        }

        curfew = self._parse_curfew_correction(feedback)
        if curfew:
            curfew_str, curfew_hour = curfew
            analysis["mistake_type"] = "curfew_rule"
            analysis["corrections"]["rules"] = {
                "curfew": curfew_str,
                "curfew_hour": curfew_hour,
            }
            analysis["summary"] = (
                f"Agent had wrong curfew. Parent corrected to {curfew_str}."
            )
            return analysis

        nickname = self._parse_nickname_correction(feedback)
        if nickname:
            analysis["mistake_type"] = "nickname"
            analysis["corrections"]["nicknames"] = [nickname]
            analysis["summary"] = f"Parent prefers nickname '{nickname}'."
            return analysis

        vibe = self._parse_vibe_correction(feedback)
        if vibe:
            analysis["mistake_type"] = "tone"
            analysis["corrections"]["vibe"] = vibe
            analysis["summary"] = f"Parent wants a {vibe} tone."
            return analysis

        analysis["summary"] = "General parental correction stored for future reference."
        return analysis

    def apply_corrections(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Persist analyzed corrections to the vector database."""
        corrections = analysis.get("corrections", {})
        learned_rules: Dict[str, Any] = {}

        if corrections:
            self.memory.update_personality(corrections)
            if "rules" in corrections:
                learned_rules.update(corrections["rules"])

        feedback = analysis["original_feedback"]
        self.memory.add_feedback(
            feedback,
            metadata={
                "mistake_type": analysis["mistake_type"],
                "learned": str(list(corrections.keys())),
            },
        )

        return {
            "mistake_type": analysis["mistake_type"],
            "summary": analysis["summary"],
            "learned_rules": learned_rules,
            "personality": self.memory.get_personality(),
        }

    def process_message(self, message: A2A_Message) -> A2A_Message:
        feedback = message.content
        ctx = message.context or {}

        thought = (
            f"Analyzing parental feedback: '{feedback}'. "
            f"Identifying mistake and updating long-term memory."
        )
        action = "Reflect on correction and update VectorMemory rules"

        analysis = self.analyze_feedback(feedback)
        result = self.apply_corrections(analysis)

        content = (
            f"Reflection complete. {analysis['summary']} "
            f"Memory updated — the agent will apply this in future interactions."
        )

        if result["learned_rules"]:
            rules_str = ", ".join(f"{k}={v}" for k, v in result["learned_rules"].items())
            content += f" Learned rules: {rules_str}."

        self.log_trace(thought, action, content)

        return A2A_Message(
            sender=self.name,
            receiver=message.sender,
            content=content,
            thought=thought,
            action=action,
            result=content,
            context={
                **ctx,
                "stage": "reflection",
                "analysis": analysis,
                "learned_rules": result["learned_rules"],
                "personality": result["personality"],
            },
        )
