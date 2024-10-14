# agents/agent_b.py

from swarm import Agent
import numpy as np
import uuid
from typing import List
from agents.alphazero_agent.agent import AlphaZeroAgent

class DecisionMaker(Agent):
    def __init__(self, decision_maker_name: str = "agent-#" + str(uuid.uuid4()), instructions: str = "Only speak in Haikus."):
        super().__init__(
            name=decision_maker_name,
            instructions=instructions,
            functions=[self.createSelf, self.act, self.learn],
        )

        self._agent = AlphaZeroAgent(grid_size=(5,5), num_actions=4, learning_rate=1e-3)
        self._agent = AlphaZeroAgent(grid_size=(5,5), num_actions=4, learning_rate=1e-3)
        self._agent.train(episodes=100)
        self.model_name = decision_maker_name + ".pth"
        self.save_current_model()
        self._agent = AlphaZeroAgent(grid_size=(5,5), num_actions=4, learning_rate=1e-3)

    def createSelf(self):
        self._agent = AlphaZeroAgent(grid_size=(5,5), num_actions=4, learning_rate=1e-3)
        self._agent.train(episodes=100)
        self.save_current_model()
        return self._agent.select_action(state, possible_actions)

    def act(self, state: np.ndarray, possible_actions: List[str]) -> str:
        return self._agent.select_action(state, possible_actions)
        self._agent.train(episodes=100)

    def learn(self, state: np.ndarray, action: str, reward: float, next_state: np.ndarray, done: bool):
        self._agent.train(episodes=100)
        self.save_current_model()

    def save_current_model(self):
        self._agent.save_model(self.model_name)