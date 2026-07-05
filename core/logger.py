import logging
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

LOG_FILE = os.getenv("TRACE_LOG_PATH", "logs/trace.log")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

os.makedirs(os.path.dirname(LOG_FILE) or ".", exist_ok=True)

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("ProjectKinship")


def trace_log(agent_name: str, thought: str, action: str, result: str = None):
    """Logs the Chain of Thought and actions of the agents."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = (
        f"[{timestamp}] {agent_name} | THOUGHT: {thought} | "
        f"ACTION: {action} | RESULT: {result if result else 'N/A'}"
    )
    logger.info(message)
