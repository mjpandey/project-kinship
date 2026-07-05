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
        self.commute_home = {
            "route": "Office to Home",
            "usual_minutes": 45,
            "traffic_extra_minutes": 5,
            "condition": "moderate",
        }
        self.work_hours = {
            "usual_start": "9:00 AM",
            "usual_end": "5:00 PM",
            "typical_departure_after_last_meeting": "4:15 PM",
        }
        # Ensure a last meeting ending at 4 PM for Daddy ETA demo
        self.work_calendar.append({
            "date": "2026-06-26",
            "time": "3:00 PM",
            "end_time": "4:00 PM",
            "title": "Client Wrap-up",
            "location": "Office",
        })

    def get_commute_pattern(self) -> Dict[str, Any]:
        logger.info("Fetching usual commute pattern from memory.")
        return {
            **self.commute_home,
            **self.work_hours,
        }

    def get_commute_home_traffic(self) -> Dict[str, Any]:
        logger.info("Fetching live traffic for commute home.")
        total = (
            self.commute_home["usual_minutes"]
            + self.commute_home["traffic_extra_minutes"]
        )
        return {
            **self.commute_home,
            "estimated_minutes": total,
            "last_updated": self.traffic_status["last_updated"],
        }

    def get_last_meeting_end(self) -> Dict[str, Any]:
        """Return the latest meeting end time from today's calendar."""
        logger.info("Fetching last meeting end time.")
        with_end = [e for e in self.work_calendar if e.get("end_time")]
        if not with_end:
            return {"end_time": "4:00 PM", "title": "Last meeting"}
        # Demo: prefer explicit 4:00 PM wrap-up
        for event in with_end:
            if event.get("end_time") == "4:00 PM":
                return event
        return with_end[-1]

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
