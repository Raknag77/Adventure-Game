from typing import TypedDict, Union, List, Dict, Optional


# ================== Encounters ==============================

class Choice(TypedDict, total=False):
    text: str
    response: str
    combat: Union[str, List[str]]
    inventory_add: List[str]
    requirements: List[str]
    gold: int
    health: int
    next: str


class Encounter(TypedDict):
    description: str
    choices: Dict[str, Choice]

# =========================================================


class Stats(TypedDict, total=False):
    health: int
    attackDmg: int
    defense: int
    agility: int
    critChance: int


# ================== Enemies ==============================
class Enemy(TypedDict):
    name: str
    stats: Stats
    description: str
    attributes: Union[str, List[str]]  # change to just `str` if it doens't work with multiple attributes

class EnemyGroups(TypedDict):
    undead: Dict[str, Enemy]
    beast: Dict[str, Enemy]

# ========================================================


# ================== Items ==============================

class Item(TypedDict, total=False):
    name: str
    description: str
    stats: Stats
    rarity: str
    price: int
    attribute: Optional[str]
    skills: Optional[Union[str, List[str]]]

class Material(TypedDict):
    name: str
    description: str
    rarity: str
    price: int

class ItemGroups(TypedDict):
    weapons: Dict[str, Item]
    helmets: Dict[str, Item]
    chestpieces: Dict[str, Item]
    leggings: Dict[str, Item]
    boots: Dict[str, Item]
    charms: Dict[str, Item]
    rings: Dict[str, Item]
    materials: Dict[str, Material]

# ========================================================


# ================== Game Content ==============================

class GameContentType(TypedDict):
    encounters: Dict[str, Encounter]
    items: ItemGroups
    enemies: EnemyGroups

# ========================================================