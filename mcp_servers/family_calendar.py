from typing import List, Dict, Any
from core.logger import logger

class FamilyCalendarMCP:
    """
    Mock MCP Server for family calendar management.
    """
    def __init__(self):
        self.events = [
            {"date": "2026-06-25", "activity": "Family Dinner", "location": "Home"},
            {"date": "2026-06-28", "activity": "Kids Soccer Practice", "location": "Community Field"},
            {"date": "2026-07-01", "activity": "Birthday Party", "location": "Central Park"}
        ]

    def get_events(self, date_range: str) -> List[Dict[str, Any]]:
        logger.info(f"Querying family calendar for range: {date_range}")
        # Mock filtering logic
        return self.events

    def add_event(self, date: str, activity: str, location: str) -> Dict[str, Any]:
        logger.info(f"Adding event to calendar: {activity} on {date}")
        new_event = {"date": date, "activity": activity, "location": location}
        self.events.append(new_event)
        return {"status": "success", "event": new_event}

    def check_availability(self, date: str) -> Dict[str, Any]:
        logger.info(f"Checking availability for: {date}")
        events = [e for e in self.events if e["date"] == date]
        if not events:
            return {"status": "available", "message": "No events scheduled for this date."}
        else:
            return {"status": "busy", "events": events}