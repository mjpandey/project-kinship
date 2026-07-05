"""Parse and format agent trace logs for CLI and dashboard display."""

import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

TRACE_LINE_PATTERN = re.compile(
    r"\[(?P<timestamp>[^\]]+)\]\s+(?P<agent>[^|]+)\s*\|\s*"
    r"THOUGHT:\s*(?P<thought>.*?)\s*\|\s*"
    r"ACTION:\s*(?P<action>.*?)\s*\|\s*"
    r"RESULT:\s*(?P<result>.*)$"
)

AGENT_COLORS = {
    "Persona": "#e91e63",
    "Logistics": "#2196f3",
    "Safety": "#ff9800",
    "Escalation": "#9c27b0",
    "Reflection": "#00bcd4",
    "Watchdog": "#f44336",
    "Orchestrator": "#607d8b",
}


def parse_trace_line(line: str) -> Optional[Dict[str, str]]:
    """Parse a single chain-of-thought log line."""
    match = TRACE_LINE_PATTERN.search(line.strip())
    if not match:
        return None
    return {
        "timestamp": match.group("timestamp").strip(),
        "agent": match.group("agent").strip(),
        "thought": match.group("thought").strip(),
        "action": match.group("action").strip(),
        "result": match.group("result").strip(),
        "raw": line.strip(),
    }


def read_trace_log(path: str = None, limit: int = 100) -> List[Dict[str, str]]:
    """Read and parse the trace log file, most recent entries last."""
    log_path = path or os.getenv("TRACE_LOG_PATH", "logs/trace.log")
    if not os.path.exists(log_path):
        return []

    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    entries = []
    for line in lines:
        if " | THOUGHT: " in line and " | ACTION: " in line:
            parsed = parse_trace_line(line)
            if parsed:
                entries.append(parsed)

    return entries[-limit:]


def format_flow_trace(trace: List[Dict[str, str]]) -> str:
    """Format an in-memory orchestrator trace as readable text."""
    blocks = []
    for i, step in enumerate(trace, 1):
        blocks.append(
            f"Step {i} — {step.get('agent', '?')} ({step.get('stage', '')})\n"
            f"  Thought: {step.get('thought', '')}\n"
            f"  Action:  {step.get('action', '')}\n"
            f"  Output:  {step.get('output', '')}"
        )
    return "\n\n".join(blocks)


def trace_to_markdown(trace: List[Dict[str, str]]) -> str:
    """Render orchestrator trace as markdown for Streamlit."""
    if not trace:
        return "_No trace steps recorded._"

    lines = []
    for i, step in enumerate(trace, 1):
        agent = step.get("agent", "Unknown")
        stage = step.get("stage", "")
        lines.append(f"### Step {i}: {agent} — `{stage}`")
        lines.append(f"**Thought:** {step.get('thought', '')}")
        lines.append(f"**Action:** {step.get('action', '')}")
        output = step.get("output", "")
        lines.append(f"**Output:**\n> {output}")
        lines.append("")
    return "\n".join(lines)


def log_entries_to_markdown(entries: List[Dict[str, str]]) -> str:
    """Render parsed log file entries as markdown."""
    if not entries:
        return "_Trace log is empty. Run a scenario to generate chain-of-thought entries._"

    lines = []
    for entry in entries:
        agent = entry.get("agent", "?")
        ts = entry.get("timestamp", "")
        lines.append(f"#### [{ts}] {agent}")
        lines.append(f"- **Thought:** {entry.get('thought', '')}")
        lines.append(f"- **Action:** {entry.get('action', '')}")
        lines.append(f"- **Result:** {entry.get('result', '')}")
        lines.append("")
    return "\n".join(lines)


def filter_entries(
    entries: List[Dict[str, str]],
    agent: str = None,
    search: str = None,
) -> List[Dict[str, str]]:
    """Filter trace log entries by agent name or search text."""
    filtered = entries
    if agent and agent != "All":
        filtered = [e for e in filtered if e.get("agent") == agent]
    if search:
        q = search.lower()
        filtered = [
            e for e in filtered
            if q in e.get("thought", "").lower()
            or q in e.get("action", "").lower()
            or q in e.get("result", "").lower()
        ]
    return filtered


def escalation_badge(escalation: Dict[str, Any]) -> str:
    """Short summary string for escalation status."""
    if not escalation:
        return "No escalation data"
    if escalation.get("should_page_parent"):
        return (
            f"Paged {escalation.get('parent_target', 'Parent')} "
            f"({escalation.get('urgency', '?')} urgency)"
        )
    return "No parent paging needed"
