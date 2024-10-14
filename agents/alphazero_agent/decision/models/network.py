# models/network.py

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple

class AlphaZeroNetwork(nn.Module):
    def __init__(self, input_shape: Tuple[int, int], num_actions: int):
        super(AlphaZeroNetwork, self).__init__()
        self.input_shape = input_shape
        self.num_actions = num_actions

        self.conv1 = nn.Conv2d(6, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        
        self.bn1 = nn.BatchNorm2d(32)
        self.bn2 = nn.BatchNorm2d(64)
        self.bn3 = nn.BatchNorm2d(64)

        self.fc1 = nn.Linear(64 * input_shape[0] * input_shape[1], 256)
        self.fc_policy = nn.Linear(256, num_actions)
        self.fc_value = nn.Linear(256, 1)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        policy = self.fc_policy(x)
        value = self.fc_value(x)
        return policy, value
