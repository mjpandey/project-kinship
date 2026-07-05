from typing import Any, Dict, List
from core.logger import logger


class LogisticsMCP:
    """Mock MCP server for logistics data: work calendar and traffic."""

    def __init__(self):
        self.work_calendar: List[Dict[str, Any]] = [
            {
                "date": "2026-06-26",
                "time": "09:00 AM",
                "title": "Team Standup",
                "location": "Zoom",
            },
            {
                "date": "2026-06-26",
                "time": "02:00 PM",
                "title": "Client Review",
                "location": "Office - Room 3B",
            },
            {
                "date": "2026-06-27",
                "time": "10:00 AM",
                "title": "Project Planning",
                "location": "Conference Room A",
            },
        ]
        self.traffic_status = {
            "route": "Home to Office",
            "condition": "moderate",
            "estimated_minutes": 35,
            "incidents": ["Accident on I-95 southbound near Exit 12"],
            "last_updated": "2026-06-26T15:00:00",
        }

    def get_work_calendar(self) -> List[Dict[str, Any]]:
        logger.info("Fetching parent's work calendar.")
        return self.work_calendar

    def get_traffic_status(self) -> Dict[str, Any]:
        logger.info("Fetching traffic status.")
        return self.traffic_status

    def get_all(self) -> Dict[str, Any]:
        logger.info("Fetching all logistics data.")
        return {
            "work_calendar": self.work_calendar,
            "traffic_status": self.traffic_status,
        }
