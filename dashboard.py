"""
Project Kinship — Demo Dashboard
Run: streamlit run dashboard.py
"""

import streamlit as st

from core.orchestrator import Orchestrator
from core.memory import VectorMemory
from core.trace_viewer import (
    AGENT_COLORS,
    escalation_badge,
    filter_entries,
    log_entries_to_markdown,
    read_trace_log,
    trace_to_markdown,
)
from demo_runner import run_escalation_demo, run_full_video_demo, run_learning_demo, run_watchdog_demo

st.set_page_config(
    page_title="Project Kinship",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    .persona-bubble {
        background: linear-gradient(135deg, #fce4ec 0%, #f8bbd0 100%);
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        margin: 0.5rem 0 1rem 0;
        border-left: 4px solid #e91e63;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    .persona-bubble-daddy {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left-color: #2196f3;
    }
    .system-chip {
        background: #f5f5f5;
        border-radius: 8px;
        padding: 0.5rem 0.75rem;
        font-size: 0.85rem;
        color: #555;
        margin-bottom: 0.5rem;
    }
    .trace-agent {
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 4px;
        color: white;
        font-size: 0.8rem;
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .hero-sub {
        color: #666;
        margin-bottom: 1.5rem;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

HERO_PRESETS = {
    "Going out with friends": "Mom, can I go out with my friends tonight?",
    "Stay out late (denied)": "Can I hang out with friends and be back by 11 PM?",
    "Child in distress": "Mom I'm freaking out and panicking, I need help right now",
    "Custom": "",
}

IOT_SCENARIOS = {
    "Front door opened": "door",
    "Stove unattended": "stove",
    "Smoke detected": "smoke",
    "Window after hours": "window",
}


def init_session():
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = None
    if "persona" not in st.session_state:
        st.session_state.persona = "mommy"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_trace" not in st.session_state:
        st.session_state.last_trace = []
    if "last_result" not in st.session_state:
        st.session_state.last_result = None
    if "demo_steps" not in st.session_state:
        st.session_state.demo_steps = []
    if "demo_baseline_applied" not in st.session_state:
        st.session_state.demo_baseline_applied = False


def get_orchestrator(persona: str) -> Orchestrator:
    """Return a cached orchestrator — one ChromaDB client per process."""
    if (
        st.session_state.orchestrator is None
        or st.session_state.persona != persona
    ):
        st.session_state.orchestrator = _create_orchestrator(persona)
        st.session_state.persona = persona

    if not st.session_state.demo_baseline_applied:
        st.session_state.orchestrator.ensure_demo_baseline()
        st.session_state.demo_baseline_applied = True

    return st.session_state.orchestrator


@st.cache_resource
def _create_orchestrator(persona: str) -> Orchestrator:
    orchestrator = Orchestrator(persona_type=persona)
    orchestrator.setup_memory_agents(persona)
    return orchestrator


def persona_bubble(text: str, persona: str):
    css_class = "persona-bubble" if persona == "mommy" else "persona-bubble persona-bubble-daddy"
    st.markdown(f'<div class="{css_class}">{text}</div>', unsafe_allow_html=True)


def render_escalation(result: dict):
    escalation = result.get("escalation")
    if not escalation:
        return
    if escalation.get("should_page_parent"):
        st.markdown(
            f'<div class="system-chip">🔔 Behind the scenes: {escalation_badge(escalation)}'
            f' — categories: {", ".join(escalation.get("matched_categories", [])) or "alert"}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="system-chip">✓ No parent paging needed for this interaction</div>',
            unsafe_allow_html=True,
        )


def render_trace_steps(trace: list):
    if not trace:
        st.info("Run a scenario to see the agent chain-of-thought trace.")
        return

    for i, step in enumerate(trace, 1):
        agent = step.get("agent", "?")
        color = AGENT_COLORS.get(agent, "#607d8b")
        with st.expander(
            f"Step {i}: {agent} — {step.get('stage', '')}",
            expanded=i == len(trace),
        ):
            st.markdown(
                f'<span class="trace-agent" style="background:{color}">{agent}</span>',
                unsafe_allow_html=True,
            )
            st.markdown(f"**Thought:** {step.get('thought', '')}")
            st.markdown(f"**Action:** {step.get('action', '')}")
            st.markdown(f"**Output:** {step.get('output', '')}")


def sidebar():
    st.sidebar.markdown("## Project Kinship")
    st.sidebar.caption("Hey Mommy · Hello Dad — Multi-Agent Parental AI")

    persona = st.sidebar.radio("Persona", ["mommy", "daddy"], format_func=str.title)
    st.session_state.persona = persona

    st.sidebar.divider()
    st.sidebar.markdown("### Quick demos")
    if st.sidebar.button("▶ Full video demo (all arcs)", use_container_width=True):
        st.session_state.run_full_demo = True
    if st.sidebar.button("🧠 Learning loop", use_container_width=True):
        st.session_state.run_learning_demo = True
    if st.sidebar.button("😰 Distress + paging", use_container_width=True):
        st.session_state.run_distress_demo = True

    st.sidebar.divider()
    st.sidebar.markdown("### Memory")
    orch = get_orchestrator(persona)
    personality = orch.memory.get_personality()
    rules = personality.get("rules", {})
    st.sidebar.metric("Curfew", rules.get("curfew", "—"))
    st.sidebar.caption("Demo baseline: 8:00 PM")
    if st.sidebar.button("Reset memory", use_container_width=True):
        VectorMemory.reset_storage()
        _create_orchestrator.clear()
        st.session_state.orchestrator = None
        st.session_state.demo_baseline_applied = False
        st.session_state.messages = []
        st.session_state.demo_steps = []
        st.session_state.pop("watchdog_response", None)
        st.rerun()

    return persona


def tab_hero(persona: str):
    st.markdown('<p class="hero-title">Hero Scenario</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-sub">Multi-agent negotiation: Persona → Logistics → Safety → Escalation → Persona</p>',
        unsafe_allow_html=True,
    )

    preset = st.selectbox("Preset prompts", list(HERO_PRESETS.keys()))
    default_text = HERO_PRESETS[preset]
    user_input = st.text_input(
        "Child says…",
        value=default_text,
        placeholder="Mom, can I go out with my friends tonight?",
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        send = st.button("Send", type="primary", use_container_width=True)

    if send and user_input.strip():
        orch = get_orchestrator(persona)
        st.session_state.messages.append({"role": "child", "content": user_input})

        with st.spinner("Agents collaborating…"):
            result = orch.run_hero_flow(user_input.strip())

        st.session_state.last_result = result
        st.session_state.last_trace = result.get("trace", [])
        st.session_state.messages.append({"role": "persona", "content": result["response"]})

    for msg in st.session_state.messages:
        if msg["role"] == "child":
            with st.chat_message("user", avatar="🧒"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant", avatar="👩" if persona == "mommy" else "👨"):
                st.write(msg["content"])

    if st.session_state.last_result:
        render_escalation(st.session_state.last_result)
        if st.session_state.last_result.get("curfew"):
            st.caption(f"Active curfew from memory: {st.session_state.last_result['curfew']}")


def tab_watchdog(persona: str):
    st.markdown('<p class="hero-title">Proactive Watchdog</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-sub">IoT sensors trigger warnings without child input — Watchdog → Persona → Escalation</p>',
        unsafe_allow_html=True,
    )

    cols = st.columns(len(IOT_SCENARIOS))
    for col, (label, scenario) in zip(cols, IOT_SCENARIOS.items()):
        with col:
            if st.button(label, use_container_width=True):
                orch = get_orchestrator(persona)
                orch.setup_watchdog_agents(persona)
                with st.spinner(f"Simulating {label}…"):
                    result = orch.simulate_iot_danger(scenario)
                st.session_state.last_result = result
                st.session_state.last_trace = result.get("trace", [])
                st.session_state.watchdog_response = result

    if "watchdog_response" in st.session_state and st.session_state.watchdog_response:
        result = st.session_state.watchdog_response
        st.warning("**Proactive warning**")
        persona_bubble(result["response"], persona)
        alert = result.get("alert", {})
        st.caption(f"Severity: {alert.get('severity', '?')} · Event: {alert.get('event_type', '?')}")
        render_escalation(result)


def tab_memory(persona: str):
    st.markdown('<p class="hero-title">Memory & Self-Learning</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-sub">Parent corrects the agent → Reflection updates ChromaDB → future interactions apply the rule</p>',
        unsafe_allow_html=True,
    )

    correction = st.text_input(
        "Parent correction",
        value="Actually, the time limit is 7 PM",
    )
    if st.button("Submit correction", type="primary"):
        orch = get_orchestrator(persona)
        with st.spinner("Reflection agent analyzing…"):
            result = orch.run_feedback_flow(correction)
        st.session_state.last_trace = result.get("trace", [])
        st.success(result["response"])
        if result.get("learned_rules"):
            st.json(result["learned_rules"])

    st.divider()
    st.markdown("#### Learned personality")
    orch = get_orchestrator(persona)
    st.json(orch.memory.get_personality())


def tab_trace():
    st.markdown('<p class="hero-title">Chain-of-Thought Trace</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-sub">Quality evidence — every agent thought, action, and output</p>',
        unsafe_allow_html=True,
    )

    view = st.radio("Source", ["Last interaction", "Full trace log file"], horizontal=True)

    if view == "Last interaction":
        render_trace_steps(st.session_state.last_trace)
        if st.session_state.last_trace:
            with st.expander("Copy as markdown"):
                st.code(trace_to_markdown(st.session_state.last_trace), language="markdown")
    else:
        entries = read_trace_log(limit=200)
        agents = ["All"] + sorted({e["agent"] for e in entries})
        c1, c2 = st.columns(2)
        with c1:
            agent_filter = st.selectbox("Filter by agent", agents)
        with c2:
            search = st.text_input("Search trace", placeholder="curfew, paging, smoke…")

        filtered = filter_entries(entries, agent=agent_filter, search=search or None)
        st.caption(f"Showing {len(filtered)} of {len(entries)} entries")

        for entry in reversed(filtered):
            agent = entry.get("agent", "?")
            color = AGENT_COLORS.get(agent, "#607d8b")
            with st.expander(f"[{entry.get('timestamp', '')}] {agent}"):
                st.markdown(
                    f'<span class="trace-agent" style="background:{color}">{agent}</span>',
                    unsafe_allow_html=True,
                )
                st.markdown(f"**Thought:** {entry.get('thought', '')}")
                st.markdown(f"**Action:** {entry.get('action', '')}")
                st.markdown(f"**Result:** {entry.get('result', '')}")

        if st.button("Refresh log"):
            st.rerun()


def tab_demo_playback():
    st.markdown('<p class="hero-title">Demo Playback</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-sub">Step through recorded demo sequences — ideal for your 5-minute video</p>',
        unsafe_allow_html=True,
    )

    if not st.session_state.demo_steps:
        st.info("Run a demo from the sidebar to populate playback steps.")
        return

    for step in st.session_state.demo_steps:
        result = step["result"]
        with st.expander(f"Step {step['step']}: {step['title']}", expanded=False):
            if "response" in result:
                st.write(result["response"])
            render_escalation(result)
            render_trace_steps(result.get("trace", []))


def run_demo_flags(persona: str):
    orch = get_orchestrator(persona)
    steps = []

    def capture(step_num, title, result):
        steps.append({"step": step_num, "title": title, "result": result})
        st.session_state.last_trace = result.get("trace", [])
        st.session_state.last_result = result

    if st.session_state.get("run_full_demo"):
        st.session_state.run_full_demo = False
        with st.spinner("Running full video demo…"):
            steps = run_full_video_demo(orch, on_step=capture)
        st.session_state.demo_steps = steps
        st.toast("Full demo complete — see Demo Playback tab")

    if st.session_state.get("run_learning_demo"):
        st.session_state.run_learning_demo = False
        with st.spinner("Running learning demo…"):
            steps = run_learning_demo(orch, on_step=capture)
        st.session_state.demo_steps = steps
        st.toast("Learning demo complete")

    if st.session_state.get("run_distress_demo"):
        st.session_state.run_distress_demo = False
        with st.spinner("Running distress demo…"):
            steps = run_escalation_demo(orch, on_step=capture)
        st.session_state.demo_steps = steps
        st.toast("Distress demo complete")


def main():
    init_session()
    persona = sidebar()
    run_demo_flags(persona)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💬 Hero",
        "🚨 Watchdog",
        "🧠 Memory",
        "📋 Trace Log",
        "🎬 Demo Playback",
    ])

    with tab1:
        tab_hero(persona)
    with tab2:
        tab_watchdog(persona)
    with tab3:
        tab_memory(persona)
    with tab4:
        tab_trace()
    with tab5:
        tab_demo_playback()


if __name__ == "__main__":
    main()
