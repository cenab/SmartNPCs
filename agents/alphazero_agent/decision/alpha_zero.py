# agents/alphazero_agent/agent.py

import torch
import torch.optim as optim
from typing import List, Tuple, Dict
import numpy as np

# Assuming these modules exist in your project structure
from .models.network import AlphaZeroNetwork
from .search.mcts import MCTS
from .environment.gridworld import GridWorld

class AlphaZeroAgent:
    def __init__(self, grid_size: Tuple[int, int]=(5,5), num_actions: int=4, learning_rate: float=1e-3):
        self.env = GridWorld(size=grid_size)
        self.num_actions = num_actions
        self.network = AlphaZeroNetwork(input_shape=grid_size, num_actions=num_actions)
        self.optimizer = optim.Adam(self.network.parameters(), lr=learning_rate)
        self.mcts = MCTS(self.network, num_simulations=50)
        self.action_map = {0: "up", 1: "down", 2: "left", 3: "right"}
        self.action_to_index = {v: k for k, v in self.action_map.items()}

    def select_action(self, state: Dict, possible_actions: List[str]) -> str:
        # Convert the state dict to a format suitable for your neural network
        network_input = self.state_to_network_input(state)
        action = self.mcts.search(network_input, possible_actions)
        return action

    def state_to_network_input(self, state: Dict) -> np.ndarray:
        # Convert the state dict to a numpy array suitable for your neural network
        # This is a placeholder implementation; adjust according to your network architecture
        grid_size = state['grid_size']
        input_channels = 6  # terrain, agent, goal, npcs, items, weather
        network_input = np.zeros((grid_size[0], grid_size[1], input_channels))

        # Encode terrain
        terrain_types = {"grass": 0, "forest": 1, "mountain": 2, "water": 3, "desert": 4}
        for i in range(grid_size[0]):
            for j in range(grid_size[1]):
                network_input[i, j, 0] = terrain_types[state['terrain'][i][j]]

        # Encode agent position
        network_input[state['agent_position'][0], state['agent_position'][1], 1] = 1

        # Encode goal position
        network_input[state['goal_position'][0], state['goal_position'][1], 2] = 1

        # Encode NPCs
        for npc in state['npcs'].values():
            network_input[npc['position'][0], npc['position'][1], 3] = 1

        # Encode items
        for item in state['items'].values():
            network_input[item['position'][0], item['position'][1], 4] = 1

        # Encode weather (as a global feature)
        weather_types = ["clear", "cloudy", "rainy", "stormy", "foggy"]
        weather_index = weather_types.index(state['weather'])
        network_input[:, :, 5] = weather_index / len(weather_types)

        # You might want to add more channels for other features like time, events, etc.

        return network_input

    def train(self, episodes: int=1000):
        for episode in range(episodes):
            state = self.env.reset()
            done = False
            total_reward = 0
            while not done:
                possible_actions = self.env.get_possible_actions()
                action = self.select_action(state, possible_actions)
                state, reward, done = self.env.step(action)
                total_reward += reward
            print(f"Episode {episode + 1}: Total Reward = {total_reward}")

    def save_model(self, path: str):
        torch.save(self.network.state_dict(), path)

    def load_model(self, path: str):
        self.network.load_state_dict(torch.load(path))
        self.network.eval()
