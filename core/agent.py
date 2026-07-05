from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from core.logger import trace_log

class A2A_Message(BaseModel):
    sender: str
    receiver: str
    content: str
    thought: str
    action: str
    result: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class Agent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def process_message(self, message: A2A_Message) -> A2A_Message:
        """
        Process an incoming message and return a response message.
        """
        pass

    def log_trace(self, thought: str, action: str, result: Optional[str] = None):
        trace_log(self.name, thought, action, result)