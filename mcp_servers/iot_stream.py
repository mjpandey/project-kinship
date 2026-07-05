import queue
import threading
import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from core.logger import logger

DANGER_EVENTS = {
    "front_door_opened",
    "stove_unattended",
    "smoke_detected",
    "window_opened_after_hours",
    "garage_door_opened",
    "motion_detected_exit",
}


class IoTStreamMCP:
    """Mock IoT event stream for home sensors and smart devices."""

    def __init__(self):
        self._event_queue: queue.Queue = queue.Queue()
        self._history: List[Dict[str, Any]] = []
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def push_event(
        self,
        event_type: str,
        location: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        event = {
            "event_type": event_type,
            "location": location,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
        }
        self._history.append(event)
        self._event_queue.put(event)
        logger.info(f"IoT stream event: {event_type} at {location}")
        return event

    def poll_event(self, block: bool = False, timeout: float = 0.5) -> Optional[Dict[str, Any]]:
        try:
            return self._event_queue.get(block=block, timeout=timeout if block else 0)
        except queue.Empty:
            return None

    def get_recent_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self._history[-limit:]

    def simulate_danger_scenario(self, scenario: str = "door") -> Dict[str, Any]:
        scenarios = {
            "door": ("front_door_opened", "front_door", {"sensor": "smart_lock"}),
            "stove": ("stove_unattended", "kitchen", {"temperature_f": 450, "duration_minutes": 5}),
            "smoke": ("smoke_detected", "kitchen", {"level": "elevated"}),
            "window": ("window_opened_after_hours", "bedroom", {"time": "9:45 PM"}),
            "garage": ("garage_door_opened", "garage", {"sensor": "garage_opener"}),
            "exit": ("motion_detected_exit", "hallway", {"direction": "toward_front_door"}),
        }
        event_type, location, metadata = scenarios.get(
            scenario, scenarios["door"]
        )
        return self.push_event(event_type, location, metadata)

    def start_demo_stream(
        self,
        interval_seconds: float = 3.0,
        scenario: str = "door",
        callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ):
        """Start a background thread that emits a demo IoT event after a delay."""
        self._running = True

        def _emit():
            time.sleep(interval_seconds)
            if self._running:
                event = self.simulate_danger_scenario(scenario)
                if callback:
                    callback(event)

        self._thread = threading.Thread(target=_emit, daemon=True)
        self._thread.start()
        logger.info(f"Demo IoT stream started (scenario={scenario}, delay={interval_seconds}s)")

    def stop(self):
        self._running = False
