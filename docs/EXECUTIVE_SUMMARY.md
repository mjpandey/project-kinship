# Executive Summary — Project Kinship

**Hey Mommy · Hello Dad**  
*Multi-Agent Parental AI for Digital Presence*

**Tracks:** Agents for Good · Concierge Agents  
**Team / Author:** [Your Name]  
**Repository:** [GitHub URL] · **Demo:** `streamlit run dashboard.py`

---

## Problem

When parents are at work, traveling, or simply unavailable, children still need more than a generic chatbot. They need someone who **sounds like their parent**, knows **what's happening at home** (dinner, schedule, safety), enforces **family rules**, and **knows when to call the real parent**. Today’s assistants collapse empathy, data, safety, and escalation into one voice — producing robotic replies, unsafe approvals, or missed emergencies.

## Solution

**Project Kinship** is a multi-agent system that provides *digital parental presence*. Seven specialized agents collaborate through an Orchestrator and a structured Agent-to-Agent (A2A) protocol. Only the **Persona Agent** speaks to the child — as Mommy or Daddy — while other agents handle data, rules, learning, IoT monitoring, and silent human escalation behind the scenes.

## Why Agents?

Parenting is inherently multi-role. Kinship mirrors that separation:

| Agent | Role |
|-------|------|
| **Persona** | Warm, natural child-facing voice |
| **Logistics** | Household & schedule data (MCP tools) |
| **Safety** | Curfew and family rules |
| **Escalation** | Silent paging of the real parent |
| **Watchdog** | Proactive IoT danger detection |
| **Reflection** | Learns from parent corrections |

## Hero Demo

**Scenario:** *"Mom, can I go out with my friends tonight?"*

1. Persona acknowledges the request warmly  
2. Logistics checks mock MCP data — pasta dinner at 8:30 PM  
3. Safety applies 8 PM curfew and conditions  
4. Escalation pages the parent silently (never spoken to the child)  
5. Persona delivers one natural reply: *"Yes, but home by 8 — eat with us first."*

**Learning loop:** Parent corrects *"Time limit is 7 PM"* → Reflection updates ChromaDB → next request uses 7 PM.  
**Proactive safety:** IoT smoke alert → Watchdog → Persona issues watchful warning without child input.

## Architecture (High Level)

```
Child / Parent / IoT → Orchestrator → Agents → MCP Tools & ChromaDB Memory
                                              ↓
                                    Persona (reply) · Escalation (page parent)
```

Every agent logs **Thought → Action → Result** to a trace file — full auditability for agent quality.

## Technology

Python · Pydantic A2A messages · Mock MCP servers (Household, Logistics, IoT, Feedback) · ChromaDB vector memory · Streamlit demo dashboard · python-dotenv configuration

## Value & Innovation

- **Digital presence**, not impersonation — persona-specific voice with learned rules  
- **Context-aware negotiation** using real household and schedule data  
- **Proactive safety** via IoT Watchdog, not just reactive chat  
- **Self-learning** from parent feedback with persistent memory  
- **Responsible escalation** — human paging separated from child-facing speech  

## Status

All five development phases complete: MCP router, hero multi-agent flow, proactive Watchdog, ChromaDB learning, and production demo dashboard. Ready for capstone submission and 5-minute video recording.

---

*Full pitch, video script, and writeup: [docs/SUBMISSION_PITCH.md](./SUBMISSION_PITCH.md)*
