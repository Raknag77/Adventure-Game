from enum import Enum
from typing import Literal


class ItemTypeEnum(Enum):
    WEAPONS = "weapons"
    HELMETS = "helmets"
    CHESTPIECES = "chestpieces"
    LEGGINGS = "leggings"
    BOOTS = "boots"
    CHARMS = "charms"
    RINGS = "rings"
    MATERIALS = "materials"


    WEAPON = WEAPONS
    HELMET = HELMETS
    CHESTPIECE = CHESTPIECES
    CHARM = CHARMS
    RING = RINGS
    MATERIAL = MATERIALS

class EnemyTypeEnum(Enum):
    UNDEAD = "undead"
    BEAST = "beast"
    GOBLIN = "goblin"


#  ======================== Literals ========================

EnemyTypeLiteral = Literal[
    "undead",
    "beast"
]

ItemTypeLiteral = Literal[
    "weapons",
    "helmets",
    "chestpieces",
    "leggings",
    "boots",
    "charms",
    "rings",
    "materials"
]