"""Parental feedback tool — lets a parent correct the agent's behavior."""

from typing import Any, Dict, Optional

from core.logger import logger


class ParentalFeedbackMCP:
    """
    MCP-style tool for parents to submit corrections.
    Example: "Actually, the time limit is 7 PM"
    """

    def __init__(self, on_feedback: Optional[callable] = None):
        self._on_feedback = on_feedback
        self._history: list[Dict[str, Any]] = []

    def set_handler(self, handler: callable):
        self._on_feedback = handler

    def submit_correction(self, correction: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Submit a parental correction for the Reflection Agent to process."""
        correction = correction.strip()
        if not correction:
            return {"success": False, "error": "Correction text cannot be empty."}

        logger.info(f"Parental feedback received: {correction}")

        entry = {"correction": correction, "context": context or {}}
        self._history.append(entry)

        if self._on_feedback:
            result = self._on_feedback(correction, context)
            return {"success": True, "correction": correction, "result": result}

        return {
            "success": True,
            "correction": correction,
            "message": "Feedback recorded. Wire a handler to process it.",
        }

    def get_history(self) -> list[Dict[str, Any]]:
        return list(self._history)
