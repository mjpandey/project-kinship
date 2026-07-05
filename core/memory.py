import json
import os
import re
import shutil
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.utils import embedding_functions

from core.logger import logger

# One PersistentClient per storage path (avoids SQLite readonly errors from
# multiple connections, e.g. Streamlit reruns opening the same ChromaDB file).
_CHROMA_CLIENTS: Dict[str, chromadb.PersistentClient] = {}


def resolve_storage_path(path: str) -> str:
    """Resolve relative VECTOR_DB_PATH to an absolute project-root path."""
    if os.path.isabs(path):
        return path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(project_root, path)


def get_chroma_client(storage_path: str) -> chromadb.PersistentClient:
    abs_path = resolve_storage_path(storage_path)
    os.makedirs(abs_path, exist_ok=True)
    if abs_path not in _CHROMA_CLIENTS:
        _CHROMA_CLIENTS[abs_path] = chromadb.PersistentClient(path=abs_path)
    return _CHROMA_CLIENTS[abs_path]


def reset_chroma_storage(storage_path: str) -> str:
    """Close cached client and delete on-disk ChromaDB data."""
    abs_path = resolve_storage_path(storage_path)
    _CHROMA_CLIENTS.pop(abs_path, None)
    if os.path.exists(abs_path):
        shutil.rmtree(abs_path)
    os.makedirs(abs_path, exist_ok=True)
    return abs_path


def parse_time_to_hour(time_str: str) -> Optional[int]:
    """Parse strings like '7 PM', '7:30 PM', '20:00' into 24-hour integer."""
    if not time_str:
        return None

    lower = time_str.strip().lower()

    match = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", lower)
    if not match:
        return None

    hour = int(match.group(1))
    meridiem = match.group(3)

    if meridiem == "pm" and hour < 12:
        hour += 12
    elif meridiem == "am" and hour == 12:
        hour = 0
    elif meridiem is None and hour <= 12 and hour < 8:
        hour += 12

    return hour


def format_hour(hour: int) -> str:
    """Format 24-hour integer as '7:00 PM'."""
    if hour >= 12:
        display = hour % 12 or 12
        return f"{display}:00 PM"
    return f"{hour}:00 AM"


class VectorMemory:
    """
    Vector Database implementation for long-term memory and personality vectors.
    Uses ChromaDB for persistent storage.
    """

    PERSONALITY_ID = "initial_personality"

    def __init__(self, storage_path: str = None):
        raw_path = storage_path or os.getenv("VECTOR_DB_PATH", "memory/vector_db")
        self.storage_path = resolve_storage_path(raw_path)
        os.makedirs(self.storage_path, exist_ok=True)

        self.client = get_chroma_client(raw_path)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self._bind_collections()

        if self.personality_collection.count() == 0:
            self._seed_personality()

        logger.info(f"Vector Memory initialized at {self.storage_path}")

    def _bind_collections(self):
        self.feedback_collection = self.client.get_or_create_collection(
            name="parental_feedback",
            embedding_function=self.embedding_fn,
        )
        self.personality_collection = self.client.get_or_create_collection(
            name="personality_vectors",
            embedding_function=self.embedding_fn,
        )

    def _refresh_client(self):
        """Drop cached Chroma client and reconnect (fixes stale SQLite locks)."""
        _CHROMA_CLIENTS.pop(self.storage_path, None)
        self.client = get_chroma_client(self.storage_path)
        self._bind_collections()

    def _default_personality(self) -> Dict[str, Any]:
        curfew_hour = int(os.getenv("CURFEW_HOUR", "20"))
        return {
            "rules": {
                "bedtime": "8 PM",
                "curfew": format_hour(curfew_hour),
                "curfew_hour": curfew_hour,
            },
            "child_profiles": {
                "toddler": {
                    "age": 3,
                    "nicknames": ["baby", "sweetie"],
                    "favorite_dress": "red_butterfly",
                    "favorite_color": "red",
                },
                "preschool": {
                    "age": 4,
                    "nicknames": ["love", "buddy"],
                    "favorite_activity": "lego",
                },
            },
        }

    def _seed_personality(self):
        personality = self._default_personality()
        self._write_personality(personality)

    def _write_personality(self, personality: Dict[str, Any]):
        payload = {
            "ids": [self.PERSONALITY_ID],
            "documents": [json.dumps(personality)],
            "metadatas": [{"type": "base_personality"}],
        }
        for attempt in range(2):
            try:
                self.personality_collection.upsert(**payload)
                return
            except chromadb.errors.InternalError as exc:
                if attempt == 0 and "readonly" in str(exc).lower():
                    logger.warning(
                        "ChromaDB write blocked (readonly) — refreshing client and retrying."
                    )
                    self._refresh_client()
                    continue
                raise

    def reset_to_demo_defaults(self):
        """Reset learned rules to baseline 8 PM curfew for demo runs."""
        logger.info("Resetting memory to demo baseline (8:00 PM curfew).")
        self._write_personality(self._default_personality())

    def get_personality(self) -> Dict[str, Any]:
        logger.info("Fetching personality vector memory.")
        results = self.personality_collection.get(ids=[self.PERSONALITY_ID])
        if results["documents"]:
            return json.loads(results["documents"][0])
        return self._default_personality()

    def update_personality(self, updates: Dict[str, Any]):
        logger.info(f"Updating personality memory with: {updates}")
        current = self.get_personality()
        merged = {**current, **{k: v for k, v in updates.items() if k != "rules"}}

        if "rules" in updates:
            merged["rules"] = {**current.get("rules", {}), **updates["rules"]}

        self._write_personality(merged)

    def get_rule(self, rule_name: str) -> Optional[Any]:
        return self.get_personality().get("rules", {}).get(rule_name)

    def update_rule(self, rule_name: str, value: Any):
        rules = {rule_name: value}
        if rule_name == "curfew" and isinstance(value, str):
            hour = parse_time_to_hour(value)
            if hour is not None:
                rules["curfew_hour"] = hour
        self.update_personality({"rules": rules})

    def get_curfew_hour(self) -> int:
        rules = self.get_personality().get("rules", {})
        if "curfew_hour" in rules:
            return int(rules["curfew_hour"])

        curfew_str = rules.get("curfew")
        if curfew_str:
            hour = parse_time_to_hour(curfew_str)
            if hour is not None:
                return hour

        return int(os.getenv("CURFEW_HOUR", "20"))

    def add_feedback(self, feedback: str, metadata: Dict[str, Any] = None):
        logger.info(f"Adding parental feedback to memory: {feedback}")
        meta = metadata or {}
        self.feedback_collection.add(
            ids=[os.urandom(8).hex()],
            documents=[feedback],
            metadatas=[meta] if meta else None,
        )

    def get_relevant_memories(self, query: str, n_results: int = 3) -> List[str]:
        logger.info(f"Searching vector database for: {query}")
        if self.feedback_collection.count() == 0:
            return []

        results = self.feedback_collection.query(
            query_texts=[query],
            n_results=min(n_results, self.feedback_collection.count()),
        )
        return results["documents"][0] if results["documents"] else []


    @classmethod
    def reset_storage(cls, storage_path: str = None) -> "VectorMemory":
        """Wipe ChromaDB files and return a fresh VectorMemory instance."""
        raw_path = storage_path or os.getenv("VECTOR_DB_PATH", "memory/vector_db")
        reset_chroma_storage(raw_path)
        return cls(storage_path=raw_path)


class SessionState:
    """Manages short-term context for the current conversation."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.history: List[Dict[str, Any]] = []

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def get_history(self) -> List[Dict[str, Any]]:
        return self.history

    def get_recent_context(self, limit: int = 5) -> str:
        recent = self.history[-limit:]
        return "\n".join([f"{m['role']}: {m['content']}" for m in recent])
