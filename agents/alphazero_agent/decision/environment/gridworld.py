import numpy as np
from typing import List, Tuple, Dict
import random

class GridWorld:
    def __init__(self, size: Tuple[int, int]=(10, 10), start: Tuple[int, int]=(0, 0), goal: Tuple[int, int]=(9, 9)):
        self.size = size
        self.start = start
        self.goal = goal
        self.reset()

    def reset(self):
        self.agent_pos = self.start
        self.done = False
        self.steps = 0
        self.terrain = self.generate_terrain()
        self.npcs = self.generate_npcs()
        self.items = self.generate_items()
        self.weather = "clear"
        self.time = {"hour": 12, "minute": 0, "day": 1}
        self.events = []
        return self.get_state()

    def generate_terrain(self):
        terrain_types = ["grass", "forest", "mountain", "water", "desert"]
        return [[random.choice(terrain_types) for _ in range(self.size[1])] for _ in range(self.size[0])]

    def generate_npcs(self):
        npcs = {}
        for i in range(3):  # Generate 3 NPCs
            npc_id = f"NPC-{i}"
            npcs[npc_id] = {
                "position": (random.randint(0, self.size[0]-1), random.randint(0, self.size[1]-1)),
                "dialogue": f"Hello, I'm NPC {i}!"
            }
        return npcs

    def generate_items(self):
        items = {}
        for i in range(5):  # Generate 5 items
            item_id = f"Item-{i}"
            items[item_id] = {
                "position": (random.randint(0, self.size[0]-1), random.randint(0, self.size[1]-1)),
                "type": random.choice(["weapon", "potion", "key", "treasure"]),
                "value": random.randint(1, 100)
            }
        return items

    def get_state(self):
        state = {
            "grid_size": self.size,
            "agent_position": self.agent_pos,
            "goal_position": self.goal,
            "terrain": self.terrain,
            "npcs": self.npcs,
            "items": self.items,
            "weather": self.weather,
            "time": self.time,
            "events": self.events[-5:],  # Last 5 events
            "steps": self.steps
        }
        return state

    def step(self, action: str) -> Tuple[Dict, float, bool]:
        if self.done:
            raise Exception("Episode has ended. Please reset the environment.")

        x, y = self.agent_pos
        if action == "up":
            x = max(x - 1, 0)
        elif action == "down":
            x = min(x + 1, self.size[0] - 1)
        elif action == "left":
            y = max(y - 1, 0)
        elif action == "right":
            y = min(y + 1, self.size[1] - 1)
        elif action == "interact":
            self.interact()
        elif action == "use_item":
            self.use_item()
        else:
            raise ValueError("Invalid action.")

        self.agent_pos = (x, y)
        self.steps += 1

        # Update time and potentially weather
        self.update_time()
        if random.random() < 0.1:  # 10% chance to change weather each step
            self.update_weather()

        # Apply random environment changes
        self.apply_environment_changes()

        reward = self.calculate_reward()
        self.check_events()

        if self.agent_pos == self.goal:
            reward += 100
            self.done = True
        elif self.steps >= 100:
            self.done = True  # Max steps to prevent infinite episodes

        return self.get_state(), reward, self.done

    def update_time(self):
        self.time["minute"] += 5
        if self.time["minute"] >= 60:
            self.time["minute"] = 0
            self.time["hour"] += 1
            if self.time["hour"] >= 24:
                self.time["hour"] = 0
                self.time["day"] += 1

    def update_weather(self):
        weather_types = ["clear", "cloudy", "rainy", "stormy", "foggy"]
        self.weather = random.choice(weather_types)

    def interact(self):
        for npc_id, npc_data in self.npcs.items():
            if npc_data["position"] == self.agent_pos:
                self.events.append({"type": "dialogue", "content": npc_data["dialogue"]})
                return
        self.events.append({"type": "action", "content": "No one to interact with here."})

    def use_item(self):
        for item_id, item_data in list(self.items.items()):
            if item_data["position"] == self.agent_pos:
                self.events.append({"type": "item_use", "content": f"Used {item_data['type']}"})
                del self.items[item_id]
                return
        self.events.append({"type": "action", "content": "No item to use here."})

    def calculate_reward(self):
        base_reward = -1  # Default step cost
        terrain_rewards = {"grass": 0, "forest": -1, "mountain": -2, "water": -3, "desert": -2}
        terrain_type = self.terrain[self.agent_pos[0]][self.agent_pos[1]]
        return base_reward + terrain_rewards[terrain_type]

    def check_events(self):
        if random.random() < 0.05:  # 5% chance of a random event
            event_types = ["discovery", "danger", "weather_change"]
            event_type = random.choice(event_types)
            if event_type == "discovery":
                self.events.append({"type": "discovery", "content": "You found a hidden path!"})
            elif event_type == "danger":
                self.events.append({"type": "danger", "content": "A wild animal appears!"})
            elif event_type == "weather_change":
                self.update_weather()
                self.events.append({"type": "weather", "content": f"Weather changed to {self.weather}"})

    def get_possible_actions(self) -> List[str]:
        actions = ["up", "down", "left", "right", "interact", "use_item"]
        x, y = self.agent_pos
        if x == 0:
            actions.remove("up")
        if x == self.size[0] - 1:
            actions.remove("down")
        if y == 0:
            actions.remove("left")
        if y == self.size[1] - 1:
            actions.remove("right")
        return actions

    def apply_environment_changes(self):
        change_types = ["terrain", "npc", "item", "weather", "event"]
        change_type = random.choice(change_types)

        if change_type == "terrain":
            self.change_terrain()
        elif change_type == "npc":
            self.change_npcs()
        elif change_type == "item":
            self.change_items()
        elif change_type == "weather":
            self.update_weather()
        elif change_type == "event":
            self.add_random_event()

    def change_terrain(self):
        x, y = random.randint(0, self.size[0]-1), random.randint(0, self.size[1]-1)
        new_terrain = random.choice(["grass", "forest", "mountain", "water", "desert"])
        old_terrain = self.terrain[x][y]
        self.terrain[x][y] = new_terrain
        self.events.append({
            "type": "terrain_change",
            "content": f"Terrain at ({x}, {y}) changed from {old_terrain} to {new_terrain}"
        })

    def change_npcs(self):
        if random.random() < 0.5 and self.npcs:  # 50% chance to remove an NPC if there are any
            npc_id = random.choice(list(self.npcs.keys()))
            del self.npcs[npc_id]
            self.events.append({
                "type": "npc_removed",
                "content": f"NPC {npc_id} has left the area"
            })
        else:  # Add a new NPC
            npc_id = f"NPC-{len(self.npcs)}"
            self.npcs[npc_id] = {
                "position": (random.randint(0, self.size[0]-1), random.randint(0, self.size[1]-1)),
                "dialogue": f"Hello, I'm the new NPC {npc_id}!"
            }
            self.events.append({
                "type": "npc_added",
                "content": f"New NPC {npc_id} has appeared"
            })

    def change_items(self):
        if random.random() < 0.5 and self.items:  # 50% chance to remove an item if there are any
            item_id = random.choice(list(self.items.keys()))
            del self.items[item_id]
            self.events.append({
                "type": "item_removed",
                "content": f"Item {item_id} has disappeared"
            })
        else:  # Add a new item
            item_id = f"Item-{len(self.items)}"
            self.items[item_id] = {
                "position": (random.randint(0, self.size[0]-1), random.randint(0, self.size[1]-1)),
                "type": random.choice(["weapon", "potion", "key", "treasure"]),
                "value": random.randint(1, 100)
            }
            self.events.append({
                "type": "item_added",
                "content": f"New item {item_id} has appeared"
            })

    def add_random_event(self):
        event_types = ["discovery", "danger", "quest"]
        event_type = random.choice(event_types)
        if event_type == "discovery":
            self.events.append({
                "type": "discovery",
                "content": "You found a hidden path!"
            })
        elif event_type == "danger":
            self.events.append({
                "type": "danger",
                "content": "A wild animal appears!"
            })
        elif event_type == "quest":
            self.events.append({
                "type": "quest",
                "content": "A villager asks for your help to find a lost item."
            })
