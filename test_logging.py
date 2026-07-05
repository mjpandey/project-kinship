from core.agent import Agent, A2A_Message
from core.orchestrator import Orchestrator

def test_logging():
    orchestrator = Orchestrator()
    # Mocking a simple agent to test logging via the orchestrator flow
    class MockAgent(Agent):
        def process_message(self, message: A2A_Message) -> A2A_Message:
            # Assuming log_trace exists based on project requirements
            self.log_trace("Thinking about the request", "Processing message", "Success")
            return message

    agent = MockAgent("TestAgent")
    orchestrator.register_agent(agent)
    
    # This will trigger orchestrator logging and agent logging
    orchestrator.route_request("Hello, this is a test message.")
    
    print("Logging test completed.")

if __name__ == "__main__":
    test_logging()