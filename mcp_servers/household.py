from typing import Any, Dict, List
from core.logger import logger


class HouseholdMCP:
    """Mock MCP server for household data: meals, groceries, and laundry."""

    def __init__(self):
        self.current_meal = {
            "meal": "Pasta with marinara sauce",
            "time": "6:30 PM",
            "status": "planned",
            "servings": 4,
        }
        self.grocery_list: List[str] = [
            "Milk",
            "Eggs",
            "Bread",
            "Tomatoes",
            "Pasta",
            "Olive oil",
        ]
        self.laundry_status = {
            "washer": "idle",
            "dryer": "running",
            "loads_remaining": 2,
            "last_updated": "2026-06-26T14:30:00",
        }

    def get_current_meal(self) -> Dict[str, Any]:
        logger.info("Fetching current meal plan.")
        return self.current_meal

    def get_grocery_list(self) -> List[str]:
        logger.info("Fetching grocery list.")
        return self.grocery_list

    def get_laundry_status(self) -> Dict[str, Any]:
        logger.info("Fetching laundry status.")
        return self.laundry_status

    def get_all(self) -> Dict[str, Any]:
        logger.info("Fetching all household data.")
        return {
            "current_meal": self.current_meal,
            "grocery_list": self.grocery_list,
            "laundry_status": self.laundry_status,
        }
