# Project Journey — Writeup Log

A chronological record of how **Project Kinship** was built, phase by phase. Use this for your capstone writeup and 5-minute video narrative.

---

## Vision

**Project name:** Hey Mommy · Hello Dad (Project Kinship)

**Problem:** Parents need an AI that can talk to children with warmth and consistency, enforce household rules, monitor safety proactively, learn from parent corrections, and know when to escalate to a real human.

**Approach:** Multi-agent architecture with specialized roles, mock MCP data tools, vector memory for persistence, and full chain-of-thought traceability.

---

## Phase 1 — The Router (Foundation)

**Goal:** Prove the system can route requests to the right data source.

**What we built:**
- `Orchestrator.route_request()` with keyword classification
- Mock **Household MCP** (meals, groceries, laundry)
- Mock **Logistics MCP** (calendar, traffic)
- Chain-of-thought logging from day one

**Key decision:** Separate household vs logistics at the orchestrator level before introducing agents.

**Demo:** `python main.py --phase1`  
Ask: *"What's for dinner?"* → Household MCP. *"How's traffic?"* → Logistics MCP.

**Outcome:** Data layer works; ready for agent personas.

---

## Phase 2 — The Hero Scenario (Multi-Agent Negotiation)

**Goal:** Handle *"Mom, can I go out with my friends tonight?"* through collaborative agents.

**What we built:**
- **Persona Agent** — Mommy/Daddy profiles, mood detection, warm negotiation
- **Logistics Agent** — Dinner conflict, parent schedule
- **Safety Agent** — Curfew rules, approve/deny logic
- **Hero flow:** Persona → Logistics → Safety → Persona

**Key decision:** Persona bookends the flow — only the persona speaks to the child.

**Demo:** `python main.py --phase2` with `--mommy` or `--daddy`

**Outcome:** End-to-end multi-agent negotiation working with trace logs.

---

## Phase 3 — The Watchdog (Proactive Safety)

**Goal:** Warn the child without waiting for input — IoT-driven intervention.

**What we built:**
- **IoT Stream MCP** — simulated sensors (door, stove, smoke, window)
- **Watchdog Agent** — danger classification, severity levels
- **Proactive flow:** IoT → Watchdog → Orchestrator interrupt → Persona alert voice

**Key decision:** Persona switches from conversational to watchful tone for alerts.

**Demo:** `python main.py --phase3` → `simulate smoke`

**Outcome:** System can act proactively, not just reactively.

---

## Phase 4 — The Brain (Memory & Self-Learning)

**Goal:** Give the agent persistence and evolution from parent feedback.

**What we built:**
- **ChromaDB VectorMemory** — `parental_feedback` + `personality_vectors` collections
- **Parental Feedback MCP** — parent correction entry point
- **Reflection Agent** — parses feedback, updates rules (e.g. curfew 7 PM)
- **Memory-aware Persona & Safety** — curfew and preferences from vector DB

**Key decision:** Reflection writes to memory; Safety reads on every check.

**Success criteria met:** Parent says *"Actually, the time limit is 7 PM"* → next going-out request uses 7 PM.

**Demo:** `python main.py --phase4` → `demo` command

**Outcome:** Agent learns and applies corrections across sessions.

---

## Phase 4.5 — Human Voice & Escalation (Polish)

**Goal:** Sound like a real parent; page humans only when critical.

**What we built:**
- Removed robotic phrases (*"notify the real mommy"*)
- **Escalation Agent** — grounding rules for going out, danger, anxiety, theft, urgency
- Silent paging logged to trace / dashboard, never spoken to child
- Distress detection — panic messages get calming replies, not going-out approval

**Key decision:** Separate **what we say** (Persona) from **who we alert** (Escalation).

**Outcome:** Demo-ready conversational quality with responsible escalation.

---

## Phase 5 — Production & Demo Polish

**Goal:** Finalize for capstone demo and 5-minute video recording.

**What we built:**
- **Streamlit dashboard** (`dashboard.py`) — Hero, Watchdog, Memory, Trace, Demo Playback tabs
- **Trace viewer** (`core/trace_viewer.py`) — parse and filter `logs/trace.log`
- **Demo runner** (`demo_runner.py`) — one-click full video sequence
- **Documentation** — README, ARCHITECTURE.md, this journey log

**Key decision:** Dashboard as primary demo surface; CLI retained for development.

**Demo:** `streamlit run dashboard.py` or `python main.py --dashboard`

**Outcome:** Recordable, explainable, auditable demo.

---

## Agent roster (final)

| Agent | Phase introduced | Responsibility |
|-------|------------------|----------------|
| Orchestrator | 1 | Flow coordination, routing |
| Persona | 2 | Child-facing voice |
| Logistics | 2 | Schedule & household data |
| Safety | 2 | Rules & curfew |
| Watchdog | 3 | IoT danger detection |
| Reflection | 4 | Learn from parent feedback |
| Escalation | 4.5 | Silent parent paging |

---

## Challenges & solutions

| Challenge | Solution |
|-----------|----------|
| Agents felt robotic | Rewrote Persona templates; natural closings |
| When to notify real parent? | Dedicated Escalation Agent with grounding rules |
| Learning persisted how? | ChromaDB with merge-on-update personality |
| Proving quality | Chain-of-thought trace log + dashboard viewer |
| Demo complexity | Preset prompts + one-click demo runner |

---

## Metrics for writeup

- **7 agents** orchestrated through A2A messages
- **4 mock MCP servers** (household, logistics, IoT, feedback)
- **2 ChromaDB collections** for long-term memory
- **6 escalation categories** + IoT severity mapping
- **5 development phases** delivered incrementally
- **Full trace audit trail** on every interaction

---

## Suggested writeup sections

1. **Introduction** — Problem, vision, target users (families)
2. **Architecture** — Diagram from ARCHITECTURE.md
3. **Implementation** — Phase-by-phase (this document)
4. **Quality & safety** — Trace logs, escalation rules
5. **Demo** — Screenshots from Streamlit dashboard
6. **Future work** — LLM integration, real MCP, push notifications
7. **Conclusion** — What we learned about multi-agent design

---

## Video recording checklist

- [ ] Dashboard open, Mommy persona selected
- [ ] Hero: going out with friends
- [ ] Trace tab: expand Persona → Safety → Escalation steps
- [ ] Memory: submit 7 PM correction
- [ ] Hero again: verify 7 PM in response
- [ ] Distress preset: show calming reply + paging chip
- [ ] Watchdog: simulate smoke
- [ ] Sidebar: run Full video demo
- [ ] Mention architecture diagram in README

---

*Last updated: Phase 5 completion*
