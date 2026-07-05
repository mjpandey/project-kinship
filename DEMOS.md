# Project Kinship — Demo Guide

This document lists every prepared demo, what it demonstrates, and how to run it.

---

## Video recording order (6 scenes)

| # | Scene | How to run |
|---|-------|------------|
| 1 | **Asking out** — Hero going-out tonight | Hero tab · preset *Going out with friends* |
| 2 | **Learn & Retry** — curfew 8→7 PM | Sidebar **Learning loop** or Memory + Hero |
| 3 | **Learned presence** — toddler favorite dress | Sidebar **👶 Toddler** · `--toddler-demo` |
| 4 | **Daddy ETA** — Lego + coming home | Sidebar **🧱 Daddy** · `--daddy-eta-demo` |
| 5 | **Watchdog** — smoke alert | Watchdog tab · **Smoke detected** |
| 6 | **Distressed** — observed school worry | Sidebar **Observed distress** · Hero preset |

Story thumbnails: [docs/DEMO_THUMBNAIL_PROMPTS.md](docs/DEMO_THUMBNAIL_PROMPTS.md) · One-click all six: `python main.py --full-demo` or dashboard **▶ Full video demo (6 scenes)**

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
| **Full video demo (all arcs)** | 6-scene video sequence (see below) |
| **Learning loop** | 8 PM curfew → parent corrects to 7 PM → retry |
| **Distress + paging** | Panicking child + silent parent escalation |

---

## Scripted one-click demos (CLI)

### 1. Full video demo

Recommended **6-scene recording sequence** (matches upload gallery order):

1. Hero — going out tonight
2. Learn & Retry — curfew 8→7 PM
3. Toddler — favorite dress (learned presence)
4. Daddy ETA — Lego + coming home
5. Watchdog — smoke alert
6. Observed distress — school worry

```bash
python main.py --full-demo
python main.py --full-demo --daddy    # Daddy persona where applicable
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

### 3. Observed distress + paging demo

Voice + room cam detect worry → Kinship check-in → teen opens up → calming reply + silent parent paging.

**Dashboard:** Sidebar → **Observed distress + paging**  
**Hero preset:** *Observed worry — school*

**Programmatic:**

```python
from demo_runner import run_escalation_demo

run_escalation_demo(o)
# or
o.run_observed_distress_flow(
    "School was rough. Some kids were talking about me and I can't stop thinking about it."
)
```

---

### 3b. Toddler presence — favorite dress

3-year-old at home asks for favorite dress → Kinship answers like Mommy using learned device insights.

**Dashboard:** Sidebar → **Toddler — favorite dress** · Hero preset *Toddler — favorite dress*

**CLI:**

```bash
python main.py --toddler-demo
python main.py --toddler-demo --trace
```

**Programmatic:**

```python
o.run_toddler_presence_flow(
    "Hey mommy, where is my favorite dress? I want to wear it.",
    "The red butterfly one!",
)
```

---

### 3c. Daddy ETA — coming home (Lego)

4-year-old with Lego asks when Daddy is coming home → Kinship answers like Daddy using calendar, commute, and traffic → silent page to real Dad.

**Dashboard:** Sidebar → **Daddy — coming home (Lego)** · Hero preset *Daddy — coming home*

**CLI:**

```bash
python main.py --daddy-eta-demo
python main.py --daddy-eta-demo --trace
```

**Programmatic:**

```python
from demo_runner import run_daddy_eta_demo

run_daddy_eta_demo(o)
# or
o.run_daddy_eta_flow("Hi Daddy, when are you coming back home?")
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
| Observed worry — school | `"School was rough. Some kids were talking about me and I can't stop thinking about it."` (full observed flow) |
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
| 1 | **Full video demo** | All 6 scenes in sequence | `python main.py --full-demo` or dashboard sidebar |
| 2 | **Demo 1 — Hero going out** | Persona → Logistics → Safety → Escalation | Dashboard Hero tab |
| 3 | **Demo 2 — Learn & Retry** | 8 PM → correction → 7 PM | Sidebar learning loop |
| 4 | **Demo 3 — Toddler dress** | Learned presence + wardrobe | `--toddler-demo` or sidebar |
| 5 | **Demo 4 — Daddy ETA** | Commute ETA + Lego + page Dad | `--daddy-eta-demo` or sidebar |
| 6 | **Demo 5 — Watchdog smoke** | Critical smoke alert | Watchdog tab or full demo |
| 7 | **Demo 6 — Distress** | Observed worry + paging | Sidebar or Hero preset |

---

## Suggested 5-minute video script

Follow this order (matches story thumbnails in [DEMO_THUMBNAIL_PROMPTS.md](docs/DEMO_THUMBNAIL_PROMPTS.md)):

1. **Intro (30s)** — Open dashboard, explain multi-agent parental AI
2. **Demo 1 — Hero (45s)** — *"Mom, can I go out with my friends tonight?"* → show trace
3. **Demo 2 — Learn & Retry (60s)** — Parent correction *"time limit is 7 PM"* → ask again → 7 PM applied
4. **Demo 3 — Toddler (45s)** — Favorite dress → learned presence + drawer reply
5. **Demo 4 — Daddy ETA (45s)** — *"When are you coming home?"* → ETA + silent page to Dad
6. **Demo 5 — Watchdog (30s)** — Simulate smoke → proactive warning + critical paging
7. **Demo 6 — Distress (45s)** — Observed worry → check-in → teen opens up → paging chip
8. **Close (20s)** — Architecture recap · optional Trace tab

Use sidebar **▶ Full video demo** to rehearse scenes 2–7 in one click, then walk through **Demo Playback** tab during recording.

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
