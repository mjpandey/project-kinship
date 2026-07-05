"""Mock ambient sensors — voice tone and room camera signals for distress observation."""

from datetime import datetime
from typing import Any, Dict

from core.logger import logger


class AmbientSensorsMCP:
    """Simulates voice + room-camera observation without the child initiating chat."""

    def observe_distress(self, location: str = "teen bedroom") -> Dict[str, Any]:
        observation = {
            "observation_type": "elevated_distress",
            "location": location,
            "signals": {
                "voice_tone": "shaky",
                "posture": "withdrawn",
                "alone_in_room": True,
            },
            "signal_summary": "voice · shaky tone · room cam · withdrawn posture",
            "confidence": 0.82,
            "timestamp": datetime.now().isoformat(),
        }
        logger.info(
            f"Ambient observation: elevated distress at {location} "
            f"({observation['signal_summary']})"
        )
        return observation

    def gather_daily_insights(self, child_profile: str = "toddler") -> Dict[str, Any]:
        """Simulate learned preferences from cam, mic, speaker, and memory."""
        insights = {
            "child_profile": child_profile,
            "sources": ["smart_camera", "microphone", "speaker", "memory"],
            "signal_summary": (
                "cam · mic · speaker · memory → favorites, colors, routines"
            ),
            "learned": {
                "favorite_dress": "red butterfly",
                "favorite_color": "red",
                "dance_class": "tomorrow",
                "caregiver_present": "nanny",
                "mommy_tone": "warm, uses 'baby'",
            },
            "timestamp": datetime.now().isoformat(),
        }
        logger.info(
            f"Daily insights gathered for {child_profile}: "
            f"{insights['signal_summary']}"
        )
        return insights

    def observe_missing_parent(
        self,
        location: str = "living room",
        parent: str = "Daddy",
    ) -> Dict[str, Any]:
        """Simulate mic + room cam: child missing parent, activity context."""
        observation = {
            "observation_type": "missing_parent",
            "location": location,
            "parent": parent,
            "signals": {
                "voice_tone": "missing you badly",
                "activity": "holding Lego blocks",
                "intent": "wants to play with Dad",
            },
            "signal_summary": "voice · missing you badly · room cam · Lego in hand",
            "confidence": 0.88,
            "timestamp": datetime.now().isoformat(),
        }
        logger.info(
            f"Ambient observation: child missing {parent} at {location} "
            f"({observation['signal_summary']})"
        )
        return observation
