# Privacy — Project Kinship

**Hey Mommy · Hello Dad** handles family-like conversations, rules, and safety scenarios. This document describes what the **capstone demo** collects today and how a **production Kinship Voice Platform** would treat personal devices and data.

---

## Capstone demo (this repository)

The submitted demo is **local-first** and **does not require real personal devices or cloud accounts**.

| Aspect | Demo behavior |
|--------|----------------|
| **Data sources** | Mock MCP servers (household, logistics, IoT) — no live calendar, camera, or microphone feeds |
| **Storage** | ChromaDB on disk (`memory/vector_db`) for curfew/rules and feedback embeddings; trace log at `logs/trace.log` |
| **Network** | No telemetry or data sent to external services by default |
| **API keys** | Optional (`OPENAI_API_KEY` in `.env`); not used by core demo agents |
| **Children / voices** | Sample preset messages only — no real child recordings |

**You control local data:** delete `memory/vector_db` and `logs/trace.log` to reset, or use the dashboard **Reset memory** control. Copy `.env.example` to `.env` — never commit secrets.

**Educational use:** This project is a capstone demonstration, not a production child-safety or parental-control product.

---

## Responsible design (demo)

- **Safety Agent** — Applies curfew and conditional rules from memory  
- **Escalation Agent** — Pages a parent *silently*; the child-facing Persona never mentions backend notifications  
- **Watchdog** — Simulated IoT events only in the demo  
- **Audit trail** — Agent steps logged locally (Thought → Action → Result) for review  

See [ARCHITECTURE.md](./ARCHITECTURE.md) and [SUBMISSION_PITCH.md](./SUBMISSION_PITCH.md) §3.9 for security context.

---

## Production vision (not implemented)

A future **Kinship Voice Platform** would connect phones, smart speakers (Google Nest, Alexa), and cameras through one agent backend. That requires the same **opt-in trust model** as Google Workspace, smart-home assistants, and family safety apps:

- **Consent first** — Parents pair devices and accept terms before voice, calendar, camera, or location access  
- **Purpose limitation** — Data used only for parental presence, safety, and learned preferences  
- **Parent control** — Manage rules, connected devices, memory export/delete, and who can hear recordings  
- **Transparency** — Trace and preference screens explain *why* the system acted  
- **Minimization** — Agents request only the context needed for each decision  

Personal data at scale enables warm attachment (parent-like voice, remembered curfew, home-aware safety). That depth would **always** require documented user agreement — not implied permission from installing an app or enabling a speaker.

Details: [SUBMISSION_PITCH.md](./SUBMISSION_PITCH.md) §6 (Kinship Voice Platform).

---

## Questions

For capstone or research use, open an issue in the repository or contact the project author.

*Last updated for capstone submission — demo scope only unless otherwise stated.*
