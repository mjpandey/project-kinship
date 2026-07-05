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
from demo_runner import (
    run_daddy_eta_demo,
    run_escalation_demo,
    run_full_video_demo,
    run_learning_demo,
    run_toddler_presence_demo,
    run_watchdog_demo,
)

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
    "Observed worry — school": (
        "School was rough. Some kids were talking about me and I can't stop thinking about it."
    ),
    "Toddler — favorite dress": (
        "Hey mommy, where is my favorite dress? I want to wear it."
    ),
    "Daddy — coming home": "Hi Daddy, when are you coming back home?",
    "Custom": "",
}

OBSERVED_WORRY_PRESET = "Observed worry — school"
TODDLER_DRESS_PRESET = "Toddler — favorite dress"
DADDY_ETA_PRESET = "Daddy — coming home"
DEFAULT_TODDLER_DRESS_CHOICE = "The red butterfly one!"

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
    st.sidebar.markdown("## Hey Mommy · Hi Dad")
    st.sidebar.caption("Project Kinship — Multi-Agent Parental Presence AI")

    persona = st.sidebar.radio("Persona", ["mommy", "daddy"], format_func=str.title)
    st.session_state.persona = persona

    st.sidebar.divider()
    st.sidebar.markdown("### Quick demos")
    if st.sidebar.button("▶ Full video demo (6 scenes)", use_container_width=True):
        st.session_state.run_full_demo = True
    if st.sidebar.button("🧠 Learning loop", use_container_width=True):
        st.session_state.run_learning_demo = True
    if st.sidebar.button("😰 Observed distress + paging", use_container_width=True):
        st.session_state.run_distress_demo = True
    if st.sidebar.button("👶 Toddler — favorite dress", use_container_width=True):
        st.session_state.run_toddler_demo = True
    if st.sidebar.button("🧱 Daddy — coming home (Lego)", use_container_width=True):
        st.session_state.run_daddy_eta_demo = True

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


def apply_observed_distress_messages(result: dict):
    """Rebuild chat from observed-distress flow (sensors → check-in → teen → comfort)."""
    st.session_state.messages = []
    obs = result.get("observation", {})
    st.session_state.messages.append({
        "role": "system",
        "content": f"Observed: {obs.get('signal_summary', 'elevated distress')}",
    })
    st.session_state.messages.append({"role": "persona", "content": result["check_in"]})
    st.session_state.messages.append({"role": "child", "content": result["teen_response"]})
    st.session_state.messages.append({"role": "persona", "content": result["response"]})


def apply_toddler_presence_messages(result: dict):
    """Rebuild chat from toddler dress flow (insights → ask → choice → reply)."""
    st.session_state.messages = []
    insights = result.get("daily_insights", {})
    st.session_state.messages.append({
        "role": "system",
        "content": f"Learned: {insights.get('signal_summary', 'device insights')}",
    })
    st.session_state.messages.append({"role": "child", "content": result["child_ask"]})
    st.session_state.messages.append({"role": "persona", "content": result["greeting"]})
    st.session_state.messages.append({"role": "child", "content": result["child_choice"]})
    st.session_state.messages.append({"role": "persona", "content": result["response"]})


def apply_daddy_eta_messages(result: dict):
    """Rebuild chat from Daddy ETA flow (observe → data → ask → reply + paging)."""
    st.session_state.messages = []
    obs = result.get("child_observation", {})
    st.session_state.messages.append({
        "role": "system",
        "content": f"Observed: {obs.get('signal_summary', 'missing parent')}",
    })
    data_points = result.get("data_points", [])
    if data_points:
        summary = "; ".join(f"{dp['source']}: {dp['insight']}" for dp in data_points)
        st.session_state.messages.append({"role": "system", "content": f"Data: {summary}"})
    st.session_state.messages.append({"role": "child", "content": result["child_ask"]})
    st.session_state.messages.append({"role": "persona", "content": result["response"]})


def tab_hero(persona: str):
    st.markdown('<p class="hero-title">Hero Scenario</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-sub">Multi-agent negotiation: Persona → Logistics → Safety → Escalation → Persona</p>',
        unsafe_allow_html=True,
    )

    preset = st.selectbox("Preset prompts", list(HERO_PRESETS.keys()))
    default_text = HERO_PRESETS[preset]
    is_observed = preset == OBSERVED_WORRY_PRESET
    is_toddler = preset == TODDLER_DRESS_PRESET
    is_daddy_eta = preset == DADDY_ETA_PRESET
    if is_observed:
        input_label = "Teen reply (after Kinship check-in)…"
    elif is_toddler:
        input_label = "Toddler asks…"
    elif is_daddy_eta:
        input_label = "Preschooler asks…"
    else:
        input_label = "Child says…"
    user_input = st.text_input(
        input_label,
        value=default_text,
        placeholder=(
            "School was rough. Some kids were talking about me…"
            if is_observed
            else (
                "Hey mommy, where is my favorite dress?"
                if is_toddler
                else (
                    "Hi Daddy, when are you coming back home?"
                    if is_daddy_eta
                    else "Mom, can I go out with my friends tonight?"
                )
            )
        ),
    )
    toddler_choice = DEFAULT_TODDLER_DRESS_CHOICE
    if is_toddler:
        toddler_choice = st.text_input(
            "Toddler picks (simulated reply)",
            value=DEFAULT_TODDLER_DRESS_CHOICE,
        )
        st.caption(
            "Digital Mommy presence: cam · mic · memory → dress choices → "
            "second drawer for dance class."
        )
    if is_daddy_eta:
        st.caption(
            "Runs Daddy ETA flow: voice + room cam → calendar/commute/traffic → "
            "warm ETA reply → silent page to real Dad."
        )
    if is_observed:
        st.caption(
            "Runs observed-distress flow: voice + room cam → Kinship asks what's wrong → "
            "teen opens up → silent parent paging."
        )

    col1, col2 = st.columns([1, 4])
    with col1:
        send = st.button("Send", type="primary", use_container_width=True)

    if send and user_input.strip():
        flow_persona = "daddy" if is_daddy_eta else persona
        if is_daddy_eta:
            st.session_state.persona = "daddy"
        orch = get_orchestrator(flow_persona)

        with st.spinner("Agents collaborating…"):
            if is_observed:
                result = orch.run_observed_distress_flow(user_input.strip())
                apply_observed_distress_messages(result)
            elif is_toddler:
                result = orch.run_toddler_presence_flow(
                    user_input.strip(),
                    toddler_choice.strip() or DEFAULT_TODDLER_DRESS_CHOICE,
                )
                apply_toddler_presence_messages(result)
            elif is_daddy_eta:
                result = orch.run_daddy_eta_flow(user_input.strip())
                apply_daddy_eta_messages(result)
            else:
                st.session_state.messages.append({"role": "child", "content": user_input})
                result = orch.run_hero_flow(user_input.strip())
                st.session_state.messages.append({
                    "role": "persona",
                    "content": result["response"],
                })

        st.session_state.last_result = result
        st.session_state.last_trace = result.get("trace", [])

    for msg in st.session_state.messages:
        if msg["role"] == "system":
            st.markdown(
                f'<div class="system-chip">📡 {msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        elif msg["role"] == "child":
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
        '<p class="hero-sub">Step through recorded demo sequences</p>',
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
        with st.spinner("Running observed distress demo…"):
            steps = run_escalation_demo(orch, on_step=capture)
        if steps:
            apply_observed_distress_messages(steps[0]["result"])
        st.session_state.demo_steps = steps
        st.toast("Observed distress demo complete")

    if st.session_state.get("run_toddler_demo"):
        st.session_state.run_toddler_demo = False
        with st.spinner("Running toddler presence demo…"):
            steps = run_toddler_presence_demo(orch, on_step=capture)
        if steps:
            apply_toddler_presence_messages(steps[0]["result"])
        st.session_state.demo_steps = steps
        st.toast("Toddler presence demo complete")

    if st.session_state.get("run_daddy_eta_demo"):
        st.session_state.run_daddy_eta_demo = False
        st.session_state.persona = "daddy"
        daddy_orch = get_orchestrator("daddy")
        with st.spinner("Running Daddy ETA demo…"):
            steps = run_daddy_eta_demo(daddy_orch, on_step=capture)
        if steps:
            apply_daddy_eta_messages(steps[0]["result"])
            st.session_state.last_result = steps[0]["result"]
            st.session_state.last_trace = steps[0]["result"].get("trace", [])
        st.session_state.demo_steps = steps
        st.toast("Daddy ETA demo complete")


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
