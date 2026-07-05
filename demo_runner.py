"""One-click demo sequences for recording and dashboard playback."""

from typing import Any, Callable, Dict, List

from core.orchestrator import (
    Orchestrator,
    DEFAULT_DADDY_ETA_ASK,
    DEFAULT_TODDLER_DRESS_ASK,
    DEFAULT_TODDLER_DRESS_CHOICE,
    DEFAULT_TEEN_DISCLOSURE,
)


DemoStep = Dict[str, Any]


def run_learning_demo(
    orchestrator: Orchestrator,
    on_step: Callable[[int, str, Dict[str, Any]], None] = None,
) -> List[DemoStep]:
    """
    Full memory learning arc for the 5-minute video:
    going out -> parent correction -> going out again (7 PM).
    """
    steps: List[DemoStep] = []

    def emit(step_num: int, title: str, result: Dict[str, Any]):
        entry = {"step": step_num, "title": title, "result": result}
        steps.append(entry)
        if on_step:
            on_step(step_num, title, result)

    orchestrator.ensure_demo_baseline()

    emit(1, "Child asks to go out (8 PM curfew)", orchestrator.run_hero_flow(
        "Mom, can I go out with my friends tonight?"
    ))
    emit(2, "Parent corrects curfew to 7 PM", orchestrator.run_feedback_flow(
        "Actually, the time limit is 7 PM"
    ))
    emit(3, "Child asks again — agent applies learned curfew", orchestrator.run_hero_flow(
        "Mom, can I go out with my friends tonight?"
    ))
    return steps


def run_escalation_demo(
    orchestrator: Orchestrator,
    on_step: Callable[[int, str, Dict[str, Any]], None] = None,
) -> List[DemoStep]:
    """Observed distress: sensors -> check-in -> teen opens up -> silent paging."""
    steps: List[DemoStep] = []

    def emit(step_num: int, title: str, result: Dict[str, Any]):
        entry = {"step": step_num, "title": title, "result": result}
        steps.append(entry)
        if on_step:
            on_step(step_num, title, result)

    orchestrator.setup_memory_agents()
    emit(
        1,
        "Observed distress (voice + room) → check-in → teen disclosure → page parent",
        orchestrator.run_observed_distress_flow(DEFAULT_TEEN_DISCLOSURE),
    )
    return steps


def run_toddler_presence_demo(
    orchestrator: Orchestrator,
    on_step: Callable[[int, str, Dict[str, Any]], None] = None,
) -> List[DemoStep]:
    """Toddler digital presence — favorite dress with learned device insights."""
    steps: List[DemoStep] = []

    def emit(step_num: int, title: str, result: Dict[str, Any]):
        entry = {"step": step_num, "title": title, "result": result}
        steps.append(entry)
        if on_step:
            on_step(step_num, title, result)

    orchestrator.setup_memory_agents()
    emit(
        1,
        "Toddler asks for favorite dress — Kinship answers like Mommy",
        orchestrator.run_toddler_presence_flow(
            DEFAULT_TODDLER_DRESS_ASK,
            DEFAULT_TODDLER_DRESS_CHOICE,
        ),
    )
    return steps


def run_daddy_eta_demo(
    orchestrator: Orchestrator,
    on_step: Callable[[int, str, Dict[str, Any]], None] = None,
) -> List[DemoStep]:
    """Preschooler asks when Daddy is home — commute ETA + silent page to real Dad."""
    steps: List[DemoStep] = []

    def emit(step_num: int, title: str, result: Dict[str, Any]):
        entry = {"step": step_num, "title": title, "result": result}
        steps.append(entry)
        if on_step:
            on_step(step_num, title, result)

    orchestrator.setup_memory_agents("daddy")
    emit(
        1,
        "Preschooler asks when Daddy comes home — ETA + Lego promise",
        orchestrator.run_daddy_eta_flow(DEFAULT_DADDY_ETA_ASK),
    )
    return steps


def run_watchdog_demo(
    orchestrator: Orchestrator,
    scenario: str = "smoke",
    on_step: Callable[[int, str, Dict[str, Any]], None] = None,
) -> List[DemoStep]:
    """Proactive IoT safety intervention."""
    steps: List[DemoStep] = []

    def emit(step_num: int, title: str, result: Dict[str, Any]):
        entry = {"step": step_num, "title": title, "result": result}
        steps.append(entry)
        if on_step:
            on_step(step_num, title, result)

    orchestrator.setup_watchdog_agents()
    emit(1, f"IoT alert: {scenario}", orchestrator.simulate_iot_danger(scenario))
    return steps


def run_full_video_demo(
    orchestrator: Orchestrator,
    on_step: Callable[[int, str, Dict[str, Any]], None] = None,
) -> List[DemoStep]:
    """
    Recommended 6-scene capstone video sequence:
    1. Hero going-out
    2. Learn & Retry (curfew 8→7 PM)
    3. Toddler — favorite dress
    4. Daddy ETA — Lego
    5. Watchdog — smoke alert
    6. Observed distress — school worry
    """
    all_steps: List[DemoStep] = []
    offset = 0

    for batch in (
        run_learning_demo(orchestrator),
        run_toddler_presence_demo(orchestrator),
        run_daddy_eta_demo(orchestrator),
        run_watchdog_demo(orchestrator, "smoke"),
        run_escalation_demo(orchestrator),
    ):
        for step in batch:
            offset += 1
            step["step"] = offset
            all_steps.append(step)
            if on_step:
                on_step(offset, step["title"], step["result"])

    return all_steps
