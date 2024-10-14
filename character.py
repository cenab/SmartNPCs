from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Stats:
    strength: int = 0
    intelligence: int = 0
    charisma: int = 0
    luck: int = 0

    def increase(self, stat: str, amount: int = 1):
        if hasattr(self, stat):
            current_value = getattr(self, stat)
            setattr(self, stat, current_value + amount)
        else:
            raise AttributeError(f"Stat '{stat}' does not exist")

    def decrease(self, stat: str, amount: int = 1):
        if hasattr(self, stat):
            current_value = getattr(self, stat)
            setattr(self, stat, max(0, current_value - amount))  # Prevent negative stats
        else:
            raise AttributeError(f"Stat '{stat}' does not exist")

@dataclass
class InventoryItem:
    name: str
    quantity: int

@dataclass
class Location:
    latitude: float = 0.0
    longitude: float = 0.0

@dataclass
class Health:
    current: int = 100
    max: int = 100

@dataclass
class Equipment:
    weapon: str = ""
    armor: str = ""
    accessory: str = ""

@dataclass
class Quests:
    completed: List[str] = field(default_factory=list)
    active: List[str] = field(default_factory=list)

@dataclass
class Relationship:
    name: str
    type: str

@dataclass
class Goals:
    short: str = ""
    long: str = ""

@dataclass
class Personality:
    traits: List[str] = field(default_factory=list)
    hobbies: List[str] = field(default_factory=list)

@dataclass
class Preferences:
    color: str = ""
    food: str = ""
    activity: str = ""

class Character:
    def __init__(self, name: str, age: int, occupation: str, status: str, level: str, points: int):
        self._name = name
        self._age = age
        self._occupation = occupation
        self._status = status
        self._level = level
        self._points = points
        self._stats = Stats()
        self._inventory = []
        self._location = Location()
        self._health = Health()
        self._equipment = Equipment()
        self._quests = Quests()
        self._friends = []
        self._enemies = []
        self._goals = Goals()
        self._backstory = ""
        self._personality = Personality()
        self._preferences = Preferences()

    def __getattr__(self, name):
        if name.startswith('_'):
            return super().__getattribute__(name)
        return super().__getattribute__(f'_{name}')

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            super().__setattr__(f'_{name}', value)

    def get(self, attr: str) -> Any:
        return getattr(self, attr)

    def set(self, attr: str, value: Any) -> None:
        setattr(self, attr, value)

    def add_inventory_item(self, item: InventoryItem) -> None:
        self._inventory.append(item)

    def remove_inventory_item(self, item_name: str) -> None:
        self._inventory = [item for item in self._inventory if item.name != item_name]

    def add_quest(self, quest: str, active: bool = True) -> None:
        if active:
            self._quests.active.append(quest)
        else:
            self._quests.completed.append(quest)

    def complete_quest(self, quest: str) -> None:
        if quest in self._quests.active:
            self._quests.active.remove(quest)
            self._quests.completed.append(quest)

    def add_relationship(self, relationship: Relationship, is_friend: bool = True) -> None:
        if is_friend:
            self._friends.append(relationship)
        else:
            self._enemies.append(relationship)

    def remove_relationship(self, name: str, is_friend: bool = True) -> None:
        if is_friend:
            self._friends = [r for r in self._friends if r.name != name]
        else:
            self._enemies = [r for r in self._enemies if r.name != name]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self._name,
            'age': self._age,
            'occupation': self._occupation,
            'status': self._status,
            'level': self._level,
            'points': self._points,
            'stats': self._stats.__dict__,
            'inventory': [item.__dict__ for item in self._inventory],
            'location': self._location.__dict__,
            'health': self._health.__dict__,
            'equipment': self._equipment.__dict__,
            'quests': self._quests.__dict__,
            'friends': [friend.__dict__ for friend in self._friends],
            'enemies': [enemy.__dict__ for enemy in self._enemies],
            'goals': self._goals.__dict__,
            'backstory': self._backstory,
            'personality': self._personality.__dict__,
            'preferences': self._preferences.__dict__
        }

    def update_from_dict(self, data: Dict[str, Any]) -> None:
        for key, value in data.items():
            if hasattr(self, f'_{key}'):
                setattr(self, key, value)

    def increase_stat(self, stat: str, amount: int = 1):
        self._stats.increase(stat, amount)

    def decrease_stat(self, stat: str, amount: int = 1):
        self._stats.decrease(stat, amount)

    def level_up(self):
        self._level = str(int(self._level) + 1)  # Assuming level is stored as a string
        self._points += 5  # Award 5 points on level up, adjust as needed

    def spend_points(self, stat: str, amount: int = 1):
        if self._points >= amount:
            self._stats.increase(stat, amount)
            self._points -= amount
        else:
            raise ValueError("Not enough points to spend")

    def heal(self, amount: int):
        self._health.current = min(self._health.current + amount, self._health.max)

    def take_damage(self, amount: int):
        self._health.current = max(0, self._health.current - amount)

    def is_alive(self):
        return self._health.current > 0

def create_character() -> Character:
    character = Character(
        name="John Doe",
        age=30,
        occupation="Software Engineer",
        status="active",
        level="1",
        points=100
    )
    character.stats = Stats(strength=10, intelligence=8, charisma=6, luck=4)
    character.inventory = [
        InventoryItem(name="sword", quantity=1),
        InventoryItem(name="potion", quantity=3),
        InventoryItem(name="scroll", quantity=1),
    ]
    character.location = Location(latitude=40.7128, longitude=-74.006)
    character.health = Health(current=100, max=100)
    character.equipment = Equipment(weapon="sword", armor="leather", accessory="ring")
    character.quests = Quests(
        completed=["kill the dragon", "save the princess"],
        active=["find the lost treasure"]
    )
    character.friends = [Relationship(name="Jane Doe", type="npc")]
    character.enemies = [Relationship(name="Dragon", type="enemy")]
    character.goals = Goals(short="save the princess", long="defeat the evil sorcerer")
    character.backstory = "John Doe is a software engineer who travels the world in search of the perfect cup of coffee."
    character.personality = Personality(
        traits=["hardworking", "determined", "creative"],
        hobbies=["photography", "hiking", "reading"]
    )
    character.preferences = Preferences(
        color="blue",
        food="pizza",
        activity="reading a book"
    )
    return character

# Example usage
if __name__ == "__main__":
    char = create_character()
    print(f"Initial strength: {char.get('stats').strength}")
    
    char.increase_stat('strength', 2)
    print(f"After increase: {char.get('stats').strength}")
    
    char.decrease_stat('strength')
    print(f"After decrease: {char.get('stats').strength}")
    
    print(f"Initial level: {char.get('level')}, Points: {char.get('points')}")
    char.level_up()
    print(f"After level up: {char.get('level')}, Points: {char.get('points')}")
    
    char.spend_points('intelligence', 3)
    print(f"Intelligence after spending points: {char.get('stats').intelligence}")
    print(f"Remaining points: {char.get('points')}")
    
    print(f"Initial health: {char.get('health').current}")
    char.take_damage(30)
    print(f"Health after damage: {char.get('health').current}")
    char.heal(20)
    print(f"Health after healing: {char.get('health').current}")
    
    print(f"Is character alive? {char.is_alive()}")
    
    char.add_inventory_item(InventoryItem("axe", 1))
    print(f"Inventory: {[item.name for item in char.get('inventory')]}")
    
    char.complete_quest("find the lost treasure")
    print(f"Completed quests: {char.get('quests').completed}")
    
    char_dict = char.to_dict()
    print(f"Character dict: {char_dict}")
    
    char.update_from_dict({'age': 31, 'occupation': 'Data Scientist'})
    print(f"Updated age: {char.get('age')}, occupation: {char.get('occupation')}")