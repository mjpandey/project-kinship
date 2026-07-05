Project Brief: "Hey Mommy .... Hello Dad"
1. Project Vision
Title: Hey Mommy .... Hello Dad
Concept: A Multi-Agent AI system designed to provide "Digital Presence." It simulates a parent's persona (voice, emotional tone, and behavior) to provide support to children or the elderly when the real parent is physically absent. It is a "Bridge" that uses real-time data to act like a parent would.

2. Target Tracks (Competition Requirements)
Agents for Good: Emotional support for children with autism and elderly loneliness.
Concierge Agents: Lifestyle management and household orchestration.
Technical Requirements: Must demonstrate Multi-agent systems (A2A), Model Context Protocol (MCP) tools, Long/Short-term Memory, Agent Quality (Tracing/Logging), and Production-ready deployment logic.
3. System Architecture (Multi-Agent Design)
The system must be modular, using a Hub and Spoke model with an Orchestrator:

A. The Persona Agent (The Heart)
Responsibility: Handles interaction, emotional nuance, and voice simulation.
Core Logic: Uses "Personality Vector Memory" to ensure it speaks with the specific "Vibe" of the parent (e.g., warm, encouraging, specific nicknames).
B. The Logistics Agent (The Hands)
Responsibility: Interacts with the external world via MCP Servers.
Toolsets:
Parental Life: Google Calendar (Meetings), Maps (Traffic), Work Schedules.
Household: Mock/Real Home Data (Grocery lists, laundry status, dinner plans).
C. The Safety Agent (The Shield)
Responsibility: Guardrails and Human-in-the-Loop (HITL) management.
Core Logic: Monitors for high-risk requests (e.g., a child wanting to go outside alone). If a risk is detected, it "Pages" the real parent via a notification system.
D. The Reflection Agent (The Learner)
Responsibility: Self-learning and evaluation.
Core Logic: Parses "Parental Feedback" (e.g., "Actually, tell him 7 PM, not 8 PM"). It updates the Vector Database and "Self-Corrects" the Persona Agent's future behavior.
4. Technical Specifications & Stack
Language: Python.
Memory: Vector Database (for Long-term memory) + State Management (for Short-term context).
Communication: Agent2Agent (A2A) Protocol for internal communication.
Observability: Implement a "Trace Log" (Chain of Thought) to show how the agents reason before they speak.
Tools: Implement via Model Context Protocol (MCP).
5. Hero Demo Scenario
The primary demo for the Capstone will be: "The Dinner/Going Out Negotiation"

Input: Child asks to go out with friends.
Agent Action:
Logistics Agent checks dinner plans (Pasta).
Persona Agent acknowledges the kid's desire.
Safety Agent checks "Rules" (Time limits).
Agent negotiates: "You can go, but you must be back by 8 PM."
System pings the real parent for confirmation.
Learning Loop: Parent provides feedback 
→
→ Reflection Agent updates the "Time Limit" rule in memory for next time.
6. Development Instructions for Cline
Modularity: Keep agents in a separate /agents directory. Keep tools in a /tools or /mcp_servers directory.
Production-Ready: Write clean, commented, and modular code. Use .env files for all secrets (no hardcoded API keys).
Traceability: Every agent action must be logged to a trace.log or a visible "Thought" output.
Mocking: For the Capstone demo, if a real API (like a Smart Camera) is unavailable, build a "Mock MCP Server" that simulates that data.