# search/mcts.py

import math
from typing import Tuple
import numpy as np
import torch

class TreeNode:
    def __init__(self, state, parent=None, prior=1.0):
        self.state = state
        self.parent = parent
        self.children = {}
        self.visit_count = 0
        self.value_sum = 0
        self.prior = prior

    def is_leaf(self):
        return len(self.children) == 0

    def expand(self, actions):
        for action in actions:
            self.children[action] = TreeNode(state=None, parent=self, prior=1.0)

    def value(self):
        if self.visit_count == 0:
            return 0
        return self.value_sum / self.visit_count

class MCTS:
    def __init__(self, network, c_puct=1.4, num_simulations=100):
        self.network = network
        self.c_puct = c_puct
        self.num_simulations = num_simulations
        self.Q = {}
        self.N = {}
        self.P = {}
        self.root = None

    def search(self, state, possible_actions):
        self.root = TreeNode(state)
        self.root.expand(possible_actions)

        for _ in range(self.num_simulations):
            node = self.root
            path = []
            while not node.is_leaf():
                # Select the best action
                best_action, best_value = self.select(node)
                node = node.children[best_action]
                path.append(best_action)

            # Evaluate the leaf node
            policy, value = self.network(state_tensor(state))
            policy = torch.exp(policy).detach().numpy()[0]
            value = value.item()

            # Expand the node
            actions = possible_actions  # Assuming all actions are possible
            node.expand(actions)

            # Propagate the value back up the path
            self.backpropagate(node, value)

        # Choose the action with the highest visit count
        action_visits = {action: child.visit_count for action, child in self.root.children.items()}
        best_action = max(action_visits, key=action_visits.get)
        return best_action

    def select(self, node: TreeNode) -> Tuple[str, float]:
        best_score = -float('inf')
        best_action = None
        for action, child in node.children.items():
            u = self.c_puct * child.prior * math.sqrt(node.visit_count) / (1 + child.visit_count)
            q = child.value()
            score = q + u
            if score > best_score:
                best_score = score
                best_action = action
        return best_action, best_score

    def backpropagate(self, node: TreeNode, value: float):
        while node is not None:
            node.visit_count += 1
            node.value_sum += value
            node = node.parent

def state_tensor(state: np.ndarray) -> torch.Tensor:
    # Convert the state to a PyTorch tensor
    tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0).unsqueeze(0)  # Shape: [1, 1, H, W]
    return tensor