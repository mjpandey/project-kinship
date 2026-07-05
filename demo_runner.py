"""One-click demo sequences for recording and dashboard playback."""

from typing import Any, Callable, Dict, List

from core.orchestrator import Orchestrator


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
    """Show distress handling + behind-the-scenes paging."""
    steps: List[DemoStep] = []

    def emit(step_num: int, title: str, result: Dict[str, Any]):
        entry = {"step": step_num, "title": title, "result": result}
        steps.append(entry)
        if on_step:
            on_step(step_num, title, result)

    orchestrator.setup_memory_agents()
    emit(1, "Child in distress", orchestrator.run_hero_flow(
        "Mom I'm freaking out and panicking, I need help right now"
    ))
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
    Recommended 5-minute recording sequence:
    1. Hero going-out
    2. Learning loop
    3. Distress + paging
    4. Smoke alert
    """
    all_steps: List[DemoStep] = []
    offset = 0

    for batch in (
        run_learning_demo(orchestrator),
        run_escalation_demo(orchestrator),
        run_watchdog_demo(orchestrator, "smoke"),
    ):
        for step in batch:
            offset += 1
            step["step"] = offset
            all_steps.append(step)
            if on_step:
                on_step(offset, step["title"], step["result"])

    return all_steps
