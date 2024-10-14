# bot.py

from swarm import Swarm
from agents.comm_agent.agent import CommunicatingAgent
from agents.alphazero_agent.agent import DecisionMaker
from memory import Memory
import os
from dotenv import load_dotenv

class Bot:
    def __init__(self, ollama_api_key, ollama_endpoint):
        self.client = Swarm()
        self.memory = Memory()
        self.agent_a = CommunicatingAgent(
            ollama_api_key=ollama_api_key,
            ollama_endpoint=ollama_endpoint,
            instructions="You are a helpful agent interfacing with Ollama."
        )
        self.agent_b = DecisionMaker(
            decision_maker_name="Agent B",
            instructions="Only speak in Haikus."
        )
        self.environment = Environment()

    def run(self, agent, messages):
        response = self.client.run(agent=agent, messages=messages)
        if response.messages:
            print(response.messages[-1]["content"])
        else:
            print("No response received.")

async def main():
    load_dotenv()  # Load environment variables

    # Initialize Memory
    memory = Memory()

    # Initialize Agents
    ollama_api_key = os.getenv("OLLAMA_API_KEY")
    ollama_endpoint = os.getenv("OLLAMA_ENDPOINT")
    
    

    agent_b = DecisionMaker(
        decision_maker_name="Agent B",
        instructions="Only speak in Haikus."
    )

    # Initialize and Run Swarm Client
    swarm_client = SwarmClient()
    swarm_client.run(
        agent=agent_a,
        messages=[{"role": "user", "content": "I want to talk to agent B."}],
    )

    # Example of interaction with Agent B
    state = memory.character.__dict__  # Use character attributes as state
    possible_actions = ["up", "down", "left", "right"]  # Example actions
    action = agent_b.act(state, possible_actions)
    print(f"Agent B's action: {action}")

if __name__ == "__main__":
    main()