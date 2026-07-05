"""Project Kinship CLI — Phase 1 router through Phase 5 demo dashboard."""

import sys

from core.orchestrator import Orchestrator


def run_phase1(orchestrator: Orchestrator):
    print("Phase 1 — Mock Router")
    print("Ask about household (meals, groceries, laundry) or logistics (work calendar, traffic).")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("> ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break
        print(orchestrator.route_request(user_input))


def _print_escalation(result: dict):
    """Show behind-the-scenes paging decision (not spoken by persona)."""
    escalation = result.get("escalation")
    if not escalation:
        return
    if escalation.get("should_page_parent"):
        target = escalation.get("parent_target", "Parent")
        urgency = escalation.get("urgency", "medium")
        categories = ", ".join(escalation.get("matched_categories", [])) or "alert"
        print(f"[System: Paged {target} — {urgency} urgency ({categories})]")
    else:
        print("[System: No parent paging needed]")


def run_phase2(orchestrator: Orchestrator, persona_type: str):
    print(f"Phase 2 — Hero Scenario ({persona_type.title()} persona)")
    print('Try: "Mom, can I go out with my friends tonight?"')
    print("Type 'quit' to exit.\n")

    orchestrator.setup_hero_agents(persona_type)

    while True:
        user_input = input("> ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break

        result = orchestrator.run_hero_flow(user_input)
        print(f"\n{result['response']}\n")
        _print_escalation(result)

        if "--trace" in sys.argv:
            _print_trace(result["trace"])


def run_phase4(orchestrator: Orchestrator, persona_type: str):
    print(f"Phase 4 — The Brain: Memory & Self-Learning ({persona_type.title()} persona)")
    print("The agent learns from parental corrections and applies them in future interactions.")
    print("\nCommands:")
    print('  correct: <text>  — parent corrects the agent (e.g. "correct: Actually, the time limit is 7 PM")')
    print('  memory           — show current learned rules and personality')
    print('  demo             — run the learning demo (wrong curfew -> correction -> retry)')
    print("  quit             — exit")
    print('\nOr ask naturally: "Mom, can I go out with my friends tonight?"\n')

    orchestrator.setup_memory_agents(persona_type)

    while True:
        user_input = input("> ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break

        if user_input.lower() == "memory":
            personality = orchestrator.memory.get_personality()
            print("\n--- Learned Personality ---")
            print(f"  Vibe:      {personality.get('vibe')}")
            print(f"  Nicknames: {', '.join(personality.get('nicknames', []))}")
            rules = personality.get("rules", {})
            print(f"  Curfew:    {rules.get('curfew', 'not set')}")
            print(f"  Bedtime:   {rules.get('bedtime', 'not set')}")
            memories = orchestrator.memory.get_relevant_memories("curfew rules preferences")
            if memories:
                print(f"  Recent corrections: {memories[0]}")
            print()
            continue

        if user_input.lower() == "demo":
            _run_learning_demo(orchestrator)
            continue

        if user_input.lower().startswith("correct:"):
            correction = user_input[len("correct:"):].strip()
            if not correction:
                print("Please provide correction text after 'correct:'\n")
                continue
            result = orchestrator.run_feedback_flow(correction)
            print(f"\n[Reflection] {result['response']}")
            if result["learned_rules"]:
                print(f"[Learned] {result['learned_rules']}\n")
            else:
                print()
            if "--trace" in sys.argv:
                _print_trace(result["trace"])
            continue

        result = orchestrator.run_hero_flow(user_input)
        print(f"\n{result['response']}\n")
        if result.get("curfew"):
            print(f"[Active curfew from memory: {result['curfew']}]")
        _print_escalation(result)
        print()

        if "--trace" in sys.argv:
            _print_trace(result["trace"])


def _run_learning_demo(orchestrator: Orchestrator):
    """Demonstrate learning: hero flow -> parent correction -> hero flow again."""
    print("\n=== Learning Demo ===")
    orchestrator.ensure_demo_baseline()
    print("Step 1: Child asks to go out (baseline curfew 8:00 PM)...\n")

    result1 = orchestrator.run_hero_flow("Mom, can I go out with my friends tonight?")
    print(result1["response"])
    print(f"\n[Curfew applied: {result1.get('curfew', 'default')}]\n")

    print('Step 2: Parent corrects — "Actually, the time limit is 7 PM"...\n')
    feedback = orchestrator.run_feedback_flow("Actually, the time limit is 7 PM")
    print(f"[Reflection] {feedback['response']}")
    print(f"[Learned] {feedback['learned_rules']}\n")

    print("Step 3: Child asks again — agent should now use 7 PM curfew...\n")
    result2 = orchestrator.run_hero_flow("Mom, can I go out with my friends tonight?")
    print(result2["response"])
    print(f"\n[Curfew applied: {result2.get('curfew', 'default')}]")
    _print_escalation(result2)

    human_ok = "real mommy" not in result2["response"].lower() and "real daddy" not in result2["response"].lower()
    curfew_ok = "7:00 PM" in result2["response"] or result2.get("curfew") == "7:00 PM"

    if curfew_ok and human_ok:
        print("\n✓ Success: Natural voice + learned 7 PM curfew applied.\n")
    elif curfew_ok:
        print("\n✓ Curfew learned. Check persona phrasing.\n")
    else:
        print("\n✗ Curfew may not have updated — check memory with 'memory' command.\n")


def run_phase3(orchestrator: Orchestrator, persona_type: str):
    print(f"Phase 3 — Proactive Watchdog ({persona_type.title()} persona)")
    print("The system monitors IoT sensors and warns automatically — no child input needed.")
    print("\nCommands:")
    print("  simulate door   — front door opened (exit attempt)")
    print("  simulate stove  — stove left on unattended")
    print("  simulate smoke  — smoke detected")
    print("  simulate window — window opened after hours")
    print("  listen          — start background watchdog listener")
    print("  quit            — exit\n")

    orchestrator.setup_watchdog_agents(persona_type)
    listening = False

    while True:
        user_input = input("> ").strip().lower()
        if not user_input:
            continue
        if user_input in ("quit", "exit", "q"):
            if listening:
                orchestrator.stop_watchdog()
            break

        if user_input == "listen":
            if listening:
                print("Watchdog is already listening.\n")
                continue

            def on_warning(result):
                print("\n*** PROACTIVE WARNING ***")
                print(result["response"])
                print(f"[Severity: {result['alert']['severity']} | Tone: {result['tone']}]")
                _print_escalation(result)
                print()

            orchestrator.start_watchdog(on_warning=on_warning)
            listening = True
            print("Watchdog listening... IoT danger event will fire in 3 seconds.\n")
            orchestrator.iot_stream.start_demo_stream(interval_seconds=3.0, scenario="door")
            continue

        scenario_map = {
            "simulate door": "door",
            "simulate stove": "stove",
            "simulate smoke": "smoke",
            "simulate window": "window",
            "simulate garage": "garage",
            "simulate exit": "exit",
        }

        if user_input in scenario_map:
            result = orchestrator.simulate_iot_danger(scenario_map[user_input])
            print("\n*** PROACTIVE WARNING ***")
            print(result["response"])
            print(f"[Severity: {result['alert']['severity']} | Tone: {result['tone']}]")
            _print_escalation(result)
            print()

            if "--trace" in sys.argv:
                _print_trace(result["trace"])
            continue

        print("Unknown command. Try: simulate door, simulate stove, listen, quit\n")


def _print_trace(trace):
    print("--- Trace ---")
    for step in trace:
        print(f"[{step['agent']}] {step['stage']}")
        print(f"  Thought: {step['thought']}")
        print(f"  Action:  {step['action']}")
        output = step["output"]
        print(f"  Output:  {output[:120]}{'...' if len(output) > 120 else ''}")
    print()


def main():
    persona = "mommy"
    mode = "hero"

    if "--daddy" in sys.argv:
        persona = "daddy"
    if "--mommy" in sys.argv:
        persona = "mommy"

    if "--full-demo" in sys.argv:
        from demo_runner import run_full_video_demo
        orchestrator = Orchestrator(persona_type=persona)
        orchestrator.setup_memory_agents(persona)
        print("Running full video demo sequence...\n")
        for step in run_full_video_demo(orchestrator):
            print(f"--- Step {step['step']}: {step['title']} ---")
            print(step["result"].get("response", step["result"].get("page_message", ""))[:500])
            print()
        return

    if "--dashboard" in sys.argv or "--demo" in sys.argv:
        import subprocess
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
        return
    if "--phase1" in sys.argv:
        mode = "phase1"
    elif "--phase4" in sys.argv or "--memory" in sys.argv or "--brain" in sys.argv:
        mode = "phase4"
    elif "--phase3" in sys.argv or "--watchdog" in sys.argv:
        mode = "phase3"
    elif "--phase2" in sys.argv or "--hero" in sys.argv:
        mode = "phase2"

    orchestrator = Orchestrator(persona_type=persona)
    print("Project Kinship\n")

    if mode == "phase1":
        run_phase1(orchestrator)
    elif mode == "phase3":
        run_phase3(orchestrator, persona)
    elif mode == "phase4":
        run_phase4(orchestrator, persona)
    else:
        run_phase2(orchestrator, persona)


if __name__ == "__main__":
    main()
