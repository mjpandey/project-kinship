from typing import Dict, Any
from core.logger import logger

class HomeAutomationMCP:
    """
    Mock MCP Server for home automation tasks.
    """
    def __init__(self):
        self.devices = {
            "living_room_light": {"status": "off", "brightness": 80},
            "kitchen_light": {"status": "on", "brightness": 100},
            "thermostat": {"temp": 72, "mode": "cool"},
            "smart_tv": {"status": "off"}
        }

    def set_device_state(self, device_id: str, state_updates: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Updating home automation device: {device_id} with {state_updates}")
        if device_id in self.devices:
            self.devices[device_id].update(state_updates)
            return {"status": "success", "device": self.devices[device_id]}
        return {"status": "error", "message": "Device not found"}

    def get_all_devices(self) -> Dict[str, Any]:
        logger.info("Fetching status of all home automation devices.")
        return self.devices

    def get_temperature(self) -> Dict[str, Any]:
        logger.info("Reading current thermostat temperature.")
        return {"temperature": self.devices["thermostat"]["temp"], "unit": "F"}