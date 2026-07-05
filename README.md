# Project Kinship

**Hey Mommy · Hello Dad** — A multi-agent parental AI assistant that negotiates with children, monitors home safety, learns from parent corrections, and escalates to real parents when it matters.

Built as a capstone project demonstrating agent-to-agent (A2A) orchestration, mock MCP tools, vector memory, and chain-of-thought traceability.

---

## Quick start

```bash
# 1. Clone and enter the project
cd project-kinship

# 2. Create a virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Copy environment config
cp .env.example .env

# 4. Launch the demo dashboard (recommended for recording)
streamlit run dashboard.py
# or
python main.py --dashboard
```

---

## Demo dashboard

The Streamlit dashboard is the primary interface for the 5-minute video demo.  
**Full demo guide:** [DEMOS.md](DEMOS.md)

| Tab | What it shows |
|-----|----------------|
| **Hero** | Going-out negotiation with Mommy/Daddy persona |
| **Watchdog** | Proactive IoT safety alerts (door, stove, smoke) |
| **Memory** | Parent corrections → Reflection → ChromaDB learning |
| **Trace Log** | Chain-of-thought evidence per agent |
| **Demo Playback** | Step-through of one-click demo sequences |

**Sidebar quick demos:**
- **Full video demo** — 6-scene sequence: Hero → Learn & Retry → Toddler → Daddy ETA → Watchdog → Distress
- **Learning loop** — curfew correction (8 PM → 7 PM)
- **Observed distress + paging** — voice/cam worry → check-in → teen opens up → silent escalation
- **Toddler — favorite dress** — learned device insights → Mommy dress conversation

---

## CLI modes

```bash
python main.py --dashboard          # Streamlit demo (Phase 5)
python main.py --phase2 --mommy     # Hero scenario (default)
python main.py --phase3 --watchdog  # Proactive IoT watchdog
python main.py --phase4 --memory    # Memory & self-learning
python main.py --phase1             # Mock MCP router
python main.py --phase2 --trace     # Hero + print trace to terminal
```

---

## Architecture at a glance

```
Child / Parent / IoT
        │
        ▼
   Orchestrator
        │
   ┌────┴────┬──────────┬───────────┬────────────┐
   ▼         ▼          ▼           ▼            ▼
Persona  Logistics   Safety   Escalation   Reflection
   │         │          │           │            │
   │    Household MCP   │      Page real     ChromaDB
   │    Logistics MCP   │       parent      (memory)
   └─────────┴──────────┴───────────┴────────────┘
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for full diagrams and agent responsibilities.

---

## Hero scenario flow

1. **Persona** — Acknowledges the child naturally (warm Mommy/Daddy voice)
2. **Logistics** — Checks dinner plans, parent calendar, traffic (mock MCP)
3. **Safety** — Applies curfew and family rules (memory-aware)
4. **Escalation** — Decides silently whether to page the real parent
5. **Persona** — Delivers the final human-sounding response

The child never hears “I’m notifying the real mommy.” Paging happens behind the scenes.

---

## Agents

| Agent | Role |
|-------|------|
| **Persona** | Mommy/Daddy voice, mood analysis, final negotiation |
| **Logistics** | Household & schedule data via mock MCP servers |
| **Safety** | Curfew, going-out rules, distress detection |
| **Escalation** | Grounding rules for paging (danger, anxiety, going out, urgency) |
| **Watchdog** | IoT stream monitoring, proactive danger detection |
| **Reflection** | Parental feedback → analyze mistake → update vector DB |

---

## Trace log (quality evidence)

Every agent logs **Thought → Action → Result** to `logs/trace.log`.

View in the dashboard **Trace Log** tab, or in the terminal with `--trace`.

Example:
```
[2026-06-26 14:28:45] Persona | THOUGHT: Child seems hopeful... | ACTION: Reply like a real parent | RESULT: Oh sweetheart, yeah — you can go out...
```

---

## Project phases

| Phase | Focus | Status |
|-------|-------|--------|
| 1 | Mock MCP router (household vs logistics) | Done |
| 2 | Hero multi-agent negotiation | Done |
| 3 | Proactive Watchdog (IoT) | Done |
| 4 | ChromaDB memory & self-learning | Done |
| 5 | Demo dashboard & documentation | Done |

Full writeup timeline: [docs/PROJECT_JOURNEY.md](docs/PROJECT_JOURNEY.md)

---

## Documentation

| Doc | Contents |
|-----|----------|
| [DEMOS.md](DEMOS.md) | How to run every demo |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Agents, flows, diagrams |
| [docs/SUBMISSION_PITCH.md](docs/SUBMISSION_PITCH.md) | Capstone pitch & writeup |
| [docs/PRIVACY.md](docs/PRIVACY.md) | Demo data scope & privacy notes |
| [docs/DEMO_THUMBNAIL_PROMPTS.md](docs/DEMO_THUMBNAIL_PROMPTS.md) | Story-slide image prompts per demo |
| [docs/PROJECT_JOURNEY.md](docs/PROJECT_JOURNEY.md) | Build phases |

---

## 5-minute video script (suggested)

Follow the **6-scene order** in [docs/DEMO_THUMBNAIL_PROMPTS.md](docs/DEMO_THUMBNAIL_PROMPTS.md):

1. **Intro (30s)** — Open dashboard, explain multi-agent parental AI
2. **Demo 1 — Hero (45s)** — Going out tonight → show trace
3. **Demo 2 — Learn & Retry (60s)** — Curfew correction 8→7 PM
4. **Demo 3 — Toddler (45s)** — Favorite dress · learned presence
5. **Demo 4 — Daddy ETA (45s)** — Lego · commute ETA · page Dad
6. **Demo 5 — Watchdog (30s)** — Smoke alert · proactive safety
7. **Demo 6 — Distress (45s)** — Observed worry · check-in · paging
8. **Close (20s)** — Architecture recap

Use sidebar **▶ Full video demo** to rehearse demos 1–6 in one click.

---

## Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `VECTOR_DB_PATH` | `memory/vector_db` | ChromaDB storage |
| `CURFEW_HOUR` | `20` | Default 8 PM curfew |
| `TRACE_LOG_PATH` | `logs/trace.log` | Chain-of-thought log |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

---

## Project structure

```
project-kinship/
├── dashboard.py          # Streamlit demo UI (Phase 5)
├── main.py               # CLI entry point
├── demo_runner.py        # One-click demo sequences
├── agents/               # Persona, Safety, Watchdog, Reflection, Escalation
├── core/                 # Orchestrator, memory, logger, trace viewer
├── mcp_servers/          # Mock household, logistics, IoT, feedback tools
├── docs/                 # Architecture & project journey
└── logs/trace.log        # Agent chain-of-thought log
```

---

## License

Capstone project — educational use.
