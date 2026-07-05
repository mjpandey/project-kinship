# Architecture — Project Kinship

## System overview

Project Kinship is a **multi-agent orchestration system** where specialized agents communicate via a structured A2A (Agent-to-Agent) message protocol. An `Orchestrator` coordinates flows; agents never talk directly to the user except through the **Persona** agent.

```mermaid
flowchart TB
    subgraph inputs [Inputs]
        Child[Child message]
        Parent[Parent correction]
        IoT[IoT sensor stream]
    end

    subgraph core [Core]
        ORCH[Orchestrator]
        MEM[(ChromaDB VectorMemory)]
        LOG[Trace Log]
    end

    subgraph agents [Agents]
        PER[Persona Agent]
        LOG_A[Logistics Agent]
        SAF[Safety Agent]
        ESC[Escalation Agent]
        REF[Reflection Agent]
        WDG[Watchdog Agent]
    end

    subgraph mcp [Mock MCP Tools]
        HH[Household MCP]
        LG[Logistics MCP]
        IOT[IoT Stream MCP]
        FB[Parental Feedback MCP]
    end

    subgraph output [Outputs]
        Reply[Natural parent reply]
        Page[Silent parent paging]
    end

    Child --> ORCH
    Parent --> FB --> ORCH
    IoT --> WDG --> ORCH

    ORCH --> PER
    ORCH --> LOG_A
    ORCH --> SAF
    ORCH --> ESC
    ORCH --> REF
    ORCH --> WDG

    LOG_A --> HH
    LOG_A --> LG
    WDG --> IOT
    REF --> MEM
    PER --> MEM
    SAF --> MEM
    FB --> REF

    PER --> Reply
    ESC --> Page

    PER --> LOG
    SAF --> LOG
    ESC --> LOG
    REF --> LOG
    WDG --> LOG
    ORCH --> LOG
```

---

## A2A message protocol

All agents extend a common `Agent` base class and exchange `A2A_Message` objects:

| Field | Purpose |
|-------|---------|
| `sender` / `receiver` | Routing |
| `content` | User text or agent output |
| `thought` | Chain-of-thought (logged) |
| `action` | What the agent did (logged) |
| `context` | Pipeline state (`stage`, `safety`, `logistics`, etc.) |

The `context` dict carries state across the pipeline without global variables.

---

## Phase 2 — Hero flow

```mermaid
sequenceDiagram
    participant User as Child
    participant O as Orchestrator
    participant P as Persona
    participant L as Logistics
    participant S as Safety
    participant E as Escalation

    User->>O: "Can I go out tonight?"
    O->>P: analyze mood
    P->>L: forward context
    L->>L: query Household + Logistics MCP
    L->>S: forward + logistics data
    S->>S: check curfew & rules
    S->>E: forward + safety data
    E->>E: evaluate paging rules
    E-->>O: escalation decision
    O->>O: page parent if needed (silent)
    O->>P: compose final response
    P->>User: natural Mommy/Daddy reply
```

---

## Phase 3 — Proactive Watchdog

```mermaid
sequenceDiagram
    participant IoT as IoT Stream
    participant W as Watchdog
    participant O as Orchestrator
    participant P as Persona
    participant E as Escalation

    IoT->>W: danger event
    W->>O: alert payload
    O->>P: proactive warning (alert stage)
    P->>O: watchful voice response
    O->>E: evaluate IoT severity
    E-->>O: page parent (critical/high)
    O-->>User: warning (no meta-talk)
```

**Danger events:** front door, stove unattended, smoke, window after hours, garage/exit motion.

---

## Phase 4 — Memory & self-learning

```mermaid
sequenceDiagram
    participant Parent
    participant O as Orchestrator
    participant R as Reflection
    participant DB as ChromaDB
    participant S as Safety
    participant P as Persona

    Parent->>O: "Actually, curfew is 7 PM"
    O->>R: feedback message
    R->>R: parse correction
    R->>DB: update rules + store feedback
    R->>S: refresh curfew from memory

    Note over P,S: Later interaction
    O->>S: check rules
    S->>DB: get curfew_hour
    S->>P: safety with 7 PM curfew
    P->>Parent: "Be home by 7:00 PM"
```

**ChromaDB collections:**
- `personality_vectors` — learned rules (curfew, nicknames, vibe)
- `parental_feedback` — semantic search over past corrections

---

## Escalation grounding rules

The **Escalation Agent** decides paging independently of persona speech.

| Category | Example signals | Default urgency | Pages? |
|----------|-----------------|-----------------|--------|
| `going_out` | friends, hang out, leave | medium | Yes |
| `danger` | hurt, fire, help me | critical | Yes |
| `hazard` | gas leak, smoke, stove | high | Yes |
| `theft` | burglar, stole, break in | high | Yes |
| `anxious` | panic, freaking out | medium–high | Yes |
| `urgency` | right now, ASAP, 911 | high | Yes |
| IoT alert | smoke_detected, etc. | by severity | Yes |

Paging is logged to the trace file and shown in the dashboard as a system chip — never spoken to the child.

---

## Mock MCP servers

MCP (Model Context Protocol) tools are simulated as plain Python classes:

| Server | Methods |
|--------|---------|
| `HouseholdMCP` | meals, groceries, laundry |
| `LogisticsMCP` | work calendar, traffic |
| `IoTStreamMCP` | poll events, simulate danger |
| `ParentalFeedbackMCP` | submit_correction |

Phase 1 routes keyword queries directly to these tools without agents.

---

## Trace logging

`core/logger.py` → `trace_log(agent, thought, action, result)`

- Written to `logs/trace.log`
- Parsed by `core/trace_viewer.py` for the dashboard
- In-memory `trace[]` lists returned with every orchestrator flow

This is the **quality evidence** layer: every decision is auditable.

---

## Technology stack

| Layer | Choice |
|-------|--------|
| Language | Python 3.11+ |
| Agent messages | Pydantic models |
| Vector memory | ChromaDB (persistent) |
| Demo UI | Streamlit |
| LLM | Not required (rule/template-based); OpenAI deps reserved for future |

---

## Extension points

1. **LLM integration** — Swap template responses in Persona/Reflection for LangChain + OpenAI
2. **Real MCP** — Replace mock servers with live household APIs
3. **Parent paging** — Wire Escalation output to SMS/push notification service
4. **Auth** — Parent vs child roles in dashboard
