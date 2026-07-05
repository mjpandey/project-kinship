import threading
import time
from typing import Any, Callable, Dict, List, Optional

from core.agent import Agent, A2A_Message
from core.logger import logger
from mcp_servers.iot_stream import DANGER_EVENTS, IoTStreamMCP

DANGER_RULES: Dict[str, Dict[str, Any]] = {
    "front_door_opened": {
        "severity": "high",
        "threat": "unexpected exit attempt",
        "description": "The front door was opened",
    },
    "stove_unattended": {
        "severity": "critical",
        "threat": "fire hazard",
        "description": "The stove is on with no one in the kitchen",
    },
    "smoke_detected": {
        "severity": "critical",
        "threat": "fire or smoke hazard",
        "description": "Smoke was detected in the home",
    },
    "window_opened_after_hours": {
        "severity": "medium",
        "threat": "after-hours exit or entry",
        "description": "A window was opened after curfew hours",
    },
    "garage_door_opened": {
        "severity": "high",
        "threat": "unauthorized exit route",
        "description": "The garage door was opened",
    },
    "motion_detected_exit": {
        "severity": "high",
        "threat": "movement toward exit",
        "description": "Motion detected heading toward the front door",
    },
}


class WatchdogAgent(Agent):
    """Background worker that monitors the IoT stream and detects danger."""

    def __init__(self, iot_stream: IoTStreamMCP = None, poll_interval: float = 0.5):
        super().__init__(name="Watchdog")
        self.iot_stream = iot_stream or IoTStreamMCP()
        self.poll_interval = poll_interval
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._on_alert: Optional[Callable[[Dict[str, Any]], None]] = None
        logger.info("Watchdog Agent initialized.")

    def set_alert_callback(self, callback: Callable[[Dict[str, Any]], None]):
        self._on_alert = callback

    def analyze_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        event_type = event.get("event_type", "")
        if event_type not in DANGER_EVENTS:
            return None

        rule = DANGER_RULES.get(event_type, {})
        alert = {
            "event": event,
            "event_type": event_type,
            "severity": rule.get("severity", "medium"),
            "threat": rule.get("threat", "unknown hazard"),
            "description": rule.get("description", event_type),
            "location": event.get("location", "unknown"),
            "requires_intervention": True,
        }
        logger.warning(
            f"Watchdog detected danger: {event_type} ({alert['severity']}) at {alert['location']}"
        )
        return alert

    def process_message(self, message: A2A_Message) -> A2A_Message:
        """Analyze a single IoT event passed via A2A message."""
        event = (message.context or {}).get("iot_event", {})
        alert = self.analyze_event(event)

        if alert:
            thought = f"Danger detected: {alert['description']} ({alert['severity']} severity)."
            action = "Escalate to Orchestrator for proactive intervention"
            content = f"ALERT: {alert['description']} at {alert['location']}"
        else:
            thought = "IoT event reviewed — no danger detected."
            action = "Continue monitoring"
            content = "No intervention required."

        self.log_trace(thought, action, content)

        return A2A_Message(
            sender=self.name,
            receiver="Orchestrator",
            content=content,
            thought=thought,
            action=action,
            result=content,
            context={**(message.context or {}), "alert": alert},
        )

    def start_listening(self):
        """Start background polling of the IoT event stream."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()
        logger.info("Watchdog background listener started.")

    def stop_listening(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
        logger.info("Watchdog background listener stopped.")

    def _listen_loop(self):
        while self._running:
            event = self.iot_stream.poll_event(block=True, timeout=self.poll_interval)
            if event and self._on_alert:
                alert = self.analyze_event(event)
                if alert:
                    self._on_alert(alert)
