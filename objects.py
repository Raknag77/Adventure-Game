from typing import Optional

class Stats:
    def __init__(self,
                 health: int = 0,
                 defense: int = 0,
                 agility: int = 0,
                 attackDmg: int = 0,
                 critChance: float = 0.00,
                 luck:int = 0
                 ):
        self.health = health
        self.defense = defense
        self.agility = agility
        self.attackDmg = attackDmg
        self.critChance = critChance
        self.luck = luck

    def __str__(self):
        return (
            f"Health: {self.health}\n"
            f"Defense: {self.defense}\n"
            f"Agility: {self.agility}\n"
            f"Attack Damage: {self.attackDmg}\n"
            f"Critical Chance: {self.critChance * 100}%\n"
            f"Luck: {self.luck}\n"
        )


class ItemInfo:
    def __init__(self, name: str, description: str, rarity: str, price: int):
        self.name: str = name
        self.description: str = description
        self.rarity: str = rarity
        self.price: int = price


class EquippableMixin:
    def __init__(self, stats: Stats, attribute: str, traits: Optional[list[str]] = None):
        self.stats: Stats = stats
        self.attribute: str = attribute
        self.traits: Optional[list[str]] = traits


class Weapon(EquippableMixin):
    def __init__(self, info: ItemInfo, data: dict):
        super().__init__(Stats(**data.get("stats", {})), data["attribute"], data.get("traits", []))
        self.info: ItemInfo = info

