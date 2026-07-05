# Project Kinship — Demo Guide

This document lists every prepared demo, what it demonstrates, and how to run it.

---

## Prerequisites

Run once before any demo:

```bash
cd project-kinship
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

---

## Recommended: Streamlit Dashboard

Best for recording the 5-minute capstone video. All demos are available in one UI.

```bash
streamlit run dashboard.py
# or
python main.py --dashboard
```

### Dashboard tabs

| Tab | Demo |
|-----|------|
| **Hero** | Going-out negotiation with Mommy/Daddy persona |
| **Watchdog** | Proactive IoT safety alerts |
| **Memory** | Parent correction → ChromaDB learning |
| **Trace Log** | Chain-of-thought evidence per agent |
| **Demo Playback** | Step-through of scripted demo sequences |

### Sidebar one-click demos

| Button | What it runs |
|--------|--------------|
| **Full video demo (all arcs)** | Learning loop + distress + smoke alert |
| **Learning loop** | 8 PM curfew → parent corrects to 7 PM → retry |
| **Distress + paging** | Panicking child + silent parent escalation |

---

## Scripted one-click demos (CLI)

### 1. Full video demo

Recommended sequence for a 5-minute recording. Runs in order:

1. Hero going-out negotiation
2. Learning loop (curfew correction)
3. Distress + paging
4. Smoke IoT alert

```bash
python main.py --full-demo
python main.py --full-demo --daddy    # Daddy persona
python main.py --full-demo --trace    # Print agent trace to terminal
```

---

### 2. Learning loop demo

Child asks to go out → parent corrects curfew to 7 PM → child asks again (7 PM applied).

**CLI (Phase 4 mode):**

```bash
python main.py --phase4
# then type: demo
```

**Programmatic (same as dashboard “Learning loop” button):**

```python
from core.orchestrator import Orchestrator
from demo_runner import run_learning_demo

o = Orchestrator(persona_type="mommy")
o.setup_memory_agents()
run_learning_demo(o)
```

---

### 3. Distress + paging demo

Child in panic → calming reply + behind-the-scenes parent paging.

**Dashboard:** Sidebar → **Distress + paging**

**Programmatic:**

```python
from demo_runner import run_escalation_demo

run_escalation_demo(o)
```

---

### 4. Watchdog / IoT proactive demo

Automatic warning without the child speaking first.

**CLI:**

```bash
python main.py --phase3
```

Then use these commands:

| Command | Event |
|---------|-------|
| `simulate door` | Front door opened (exit attempt) |
| `simulate stove` | Stove left on unattended |
| `simulate smoke` | Smoke detected |
| `simulate window` | Window opened after hours |
| `simulate garage` | Garage door opened |
| `simulate exit` | Motion toward front door |
| `listen` | Background listener (auto-fires door event in 3s) |

**Programmatic:**

```python
from demo_runner import run_watchdog_demo

run_watchdog_demo(o, scenario="smoke")   # door | stove | smoke | window | garage | exit
```

---

## Phase-by-phase interactive demos (CLI)

### Phase 1 — Mock MCP router

Routes text input to household or logistics mock data.

```bash
python main.py --phase1
```

**Example prompts:**

- `"What's for dinner?"`
- `"Show the grocery list"`
- `"How's traffic on the commute?"`

---

### Phase 2 — Hero scenario (default)

Multi-agent going-out negotiation: Persona → Logistics → Safety → Escalation → Persona.

```bash
python main.py --phase2          # or simply: python main.py
python main.py --hero --mommy
python main.py --hero --daddy
python main.py --phase2 --trace  # Show agent trace in terminal
```

**Example prompts:**

- `"Mom, can I go out with my friends tonight?"`
- `"Can I hang out with friends and be back by 11 PM?"` (denied)

---

### Phase 3 — Proactive Watchdog

See [Watchdog / IoT proactive demo](#4-watchdog--iot-proactive-demo) above.

```bash
python main.py --phase3
python main.py --watchdog --daddy
python main.py --phase3 --trace
```

---

### Phase 4 — Memory & self-learning

Parent corrections update ChromaDB; future hero flows use learned rules.

```bash
python main.py --phase4
python main.py --memory --mommy
python main.py --brain
```

**Commands inside the CLI:**

| Command | What it does |
|---------|--------------|
| `demo` | Run full learning loop |
| `correct: Actually, the time limit is 7 PM` | Submit parent correction |
| `memory` | Show learned personality and rules |
| Natural chat | `"Mom, can I go out with my friends tonight?"` |

---

## Dashboard preset scenarios (Hero tab)

| Preset | Input |
|--------|-------|
| Going out with friends | `"Mom, can I go out with my friends tonight?"` |
| Stay out late (denied) | `"Can I hang out with friends and be back by 11 PM?"` |
| Child in distress | `"Mom I'm freaking out and panicking, I need help right now"` |
| Custom | Your own message |

---

## Dashboard IoT scenarios (Watchdog tab)

| Button | Event |
|--------|-------|
| Front door opened | Exit attempt |
| Stove unattended | Fire hazard |
| Smoke detected | Critical alert |
| Window after hours | After-curfew window open |

---

## Demo summary

| # | Demo | What it shows | How to run |
|---|------|---------------|------------|
| 1 | **Full video demo** | All arcs in one sequence | `python main.py --full-demo` or dashboard sidebar |
| 2 | **Hero — going out** | Persona → Logistics → Safety → Escalation | `python main.py --phase2` or dashboard Hero tab |
| 3 | **Hero — denied late** | Curfew rule enforcement | Dashboard preset or CLI input |
| 4 | **Learning loop** | 8 PM → correction → 7 PM | `python main.py --phase4` → `demo` or sidebar |
| 5 | **Distress + paging** | Anxiety handling + silent escalation | Dashboard sidebar |
| 6 | **Watchdog — door** | Proactive exit warning | `python main.py --phase3` → `simulate door` |
| 7 | **Watchdog — stove** | Fire hazard warning | `simulate stove` |
| 8 | **Watchdog — smoke** | Critical smoke alert | `simulate smoke` or full demo |
| 9 | **Watchdog — background** | Auto-trigger without input | `python main.py --phase3` → `listen` |
| 10 | **Phase 1 router** | Household vs logistics MCP | `python main.py --phase1` |
| 11 | **Trace log viewer** | Chain-of-thought evidence | Dashboard Trace tab or `--trace` flag |
| 12 | **Mommy vs Daddy persona** | Different voice and tone | `--mommy` / `--daddy` on any phase |

---

## Suggested 5-minute video script

1. **Intro (30s)** — Open dashboard, explain multi-agent parental AI
2. **Hero (60s)** — “Mom, can I go out with my friends tonight?” → show trace
3. **Learning (90s)** — Parent correction “time limit is 7 PM” → ask again → 7 PM applied
4. **Distress (45s)** — Panic message → calming reply + escalation chip
5. **Watchdog (45s)** — Simulate smoke → proactive warning + critical paging
6. **Trace (30s)** — Scroll chain-of-thought log as quality evidence
7. **Close (20s)** — Architecture recap

Use sidebar **Full video demo** to rehearse all arcs in one click, then walk through **Demo Playback** tab during recording.

```bash
streamlit run dashboard.py
```

---

## CLI flags reference

| Flag | Effect |
|------|--------|
| `--dashboard` / `--demo` | Launch Streamlit dashboard |
| `--full-demo` | Run full video demo sequence in terminal |
| `--phase1` | Mock MCP router |
| `--phase2` / `--hero` | Hero negotiation (default) |
| `--phase3` / `--watchdog` | Proactive IoT watchdog |
| `--phase4` / `--memory` / `--brain` | Memory and self-learning |
| `--mommy` / `--daddy` | Select persona |
| `--trace` | Print agent chain-of-thought to terminal |

---

## Related docs

- [README.md](README.md) — Quick start and project overview
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — System design and agent flows
- [docs/PROJECT_JOURNEY.md](docs/PROJECT_JOURNEY.md) — Phase-by-phase build timeline
