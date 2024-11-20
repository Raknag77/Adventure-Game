import random
from collections import Counter
import json
from operator import truediv

from game_enums import ItemTypeEnum
from game_enums import EnemyTypeEnum
from typing import Optional

with open('game_content.json', 'r') as file:
    game_content = json.load(file)

inventory = ["excalibur"]
inventory_count = Counter(inventory)

class Stats:
    def __init__(self,
                 health: int = 0,
                 defense: int = 0,
                 attackDmg: int = 0,
                 critChance: float = 0.00,
                 ):
        self.health = health
        self.defense = defense
        self.attackDmg = attackDmg
        self.critChance = critChance

class Item:
    def __init__(self, item_id: str, item_type: ItemTypeEnum):
        self._id = item_id
        self.item_type = item_type
        self.name = game_content["items"][item_type.value][item_id]["name"]
        self.description = game_content["items"][item_type.value][item_id]["description"]
        self.stats = Stats(
            attackDmg=game_content["items"][self.item_type.value][self._id].get("attackDmg", 0),
            defense=game_content["items"][self.item_type.value][self._id].get("defense", 0),
            health=game_content["items"][self.item_type.value][self._id].get("health", 0),
            critChance=game_content["items"][self.item_type.value][self._id].get("critChance", 0)
        )
        self.attribute = game_content["items"][item_type.value][item_id].get("attribute")
        self.rarity = game_content["items"][item_type.value][item_id]["rarity"]
        self.skills = game_content["items"][item_type.value][item_id].get("skills")

    def __repr__(self):
        if self.item_type == ItemTypeEnum.WEAPON:
            return f"{self.name}- (Attack Damage: {self.stats.attackDmg}, Critical Chance: {self.stats.critChance}, Attribute: {self.attribute}, Rarity: {self.rarity}, Skills: {self.skills})"
        if self.item_type == ItemTypeEnum.CHARM or self.item_type == ItemTypeEnum.RING:
            return f"{self.name}- (Attack Damage: {self.stats.attackDmg}, Critical Chance: {self.stats.critChance},Health: {self.stats.health}, Defense: {self.stats.defense}, Attribute: {self.attribute}, Rarity: {self.rarity}, Skills: {self.skills})"
        if self.item_type == ItemTypeEnum.MATERIAL:
            return f"{self.name}- Attribute: {self.attribute}, Rarity: {self.rarity})"
        return f"{self.name}- (Health: {self.stats.health}, Defense: {self.stats.defense}, Attribute: {self.attribute}, Rarity: {self.rarity}, Skills: {self.skills})"

    def get_id(self):
        return self._id

def get_item_type(item_id):
    # Check each category for the item_id
    for category, items in game_content["items"].items():
        if item_id in items:  # If item_id exists in the category
            return category  # Return the category (item_type) where the item_id was found
    # If the item is not found in any category, raise an error
    raise ValueError(f"Item ID '{item_id}' not found in any known category.")

def get_enemy_type(enemy_name: str) -> Optional[EnemyTypeEnum]:

    for category, enemies in game_content["enemies"].items():
        if enemy_name.lower() in [key.lower() for key in enemies.keys()]:
            return EnemyTypeEnum(category)
    print(f"Enemy '{enemy_name}' not found!")
    return None

class Enemy:
    def __init__(self, enemy_id: str, enemy_type: EnemyTypeEnum):
        self._id = enemy_id
        self.enemy_type = enemy_type
        self.name = game_content["enemies"][enemy_type.value][enemy_id]["name"]
        self.description = game_content["enemies"][enemy_type.value][enemy_id]["description"]
        self.stats = Stats(
            attackDmg=game_content["enemies"][self.enemy_type.value][self._id].get("stats",{}).get("attackDmg", 0),
            defense=game_content["enemies"][self.enemy_type.value][self._id].get("stats",{}).get("defense", 0),
            health=game_content["enemies"][self.enemy_type.value][self._id].get("stats",{}).get("health", 0),
            critChance=game_content["enemies"][self.enemy_type.value][self._id].get("stats",{}).get("critChance", 0)
        )
        self.attributes =  game_content["enemies"][enemy_type.value][enemy_id]["attributes"]

    def __repr__(self):
        return (
            f"  name: {self.name},\n"
            f"  description: {self.description},\n"
            f"  defense: {self.stats.defense},\n"
            f"  health: {self.stats.health},\n"
            f"  attackDmg: {self.stats.attackDmg},\n"
            f"  critChance: {self.stats.critChance},\n"
            f"  attributes: {self.attributes}\n"
        )

class Character:
    def __init__(self):
        self.name: Optional[str] = None
        self.weapon: Optional[Item] = None
        self.helmet: Optional[Item] = None
        self.chestpiece: Optional[Item] = None
        self.leggings: Optional[Item] = None
        self.boots: Optional[Item] = None
        self.charm: Optional[Item] = None
        self.ring: Optional[Item] = None

        self.defense: int = 0
        self._health: int = 50
        self.base_health: int = 50
        self.attackDmg: int = 10
        self.critDmg: int = self.attackDmg * 2
        self.critChance: float = 0.01
        self.gold: int = 0

    @property
    def health(self):
        bonus_health = 0
        if self.helmet:
            bonus_health += self.helmet.stats.health
        if self.chestpiece:
            bonus_health += self.chestpiece.stats.health
        if self.leggings:
            bonus_health += self.leggings.stats.health
        if self.boots:
            bonus_health += self.boots.stats.health
        if self.charm:
            bonus_health += self.charm.stats.health
        if self.ring:
            bonus_health += self.ring.stats.health
        return self._health + bonus_health

    @health.setter
    def health(self, new_health: int):
        self._health = new_health
        print(f"Health is now: {self._health}")





    def __str__(self):
        return (
            f"Character Info:\n"
            f"Name: {self.name}\n"
            f"Weapon: {self.weapon.name if self.weapon else 'None'}\n"  
            f"Head: {self.helmet.name if self.helmet else 'None'}\n"
            f"Top: {self.chestpiece.name if self.chestpiece else 'None'}\n"
            f"Bottom: {self.leggings.name if self.leggings else 'None'}\n"
            f"Feet: {self.boots.name if self.boots else 'None'}\n"
            f"Charm: {self.charm.name if self.charm else 'None'}\n"
            f"Ring: {self.ring.name if self.ring else 'None'}\n"
            f"Health: {self.health}\n"
            f"defense: {self.defense}\n"
            f"Attack Damage: {self.attackDmg}\n"
            f"Critical Damage: {self.critDmg}\n"
            f"Critical Chance: {self.critChance * 100}%\n"
            f"Gold: {self.gold}\n"
        )

player = Character()

def equipment_tab():
    print("This is your current equipment:\n")
    print(player)
    equip_tab = input("Press [1] to change your weapon\n"
                      "Press [2] to change your helmet\n"
                      "Press [3] to change your chestpiece\n"
                      "Press [4] to change your leggings\n"
                      "Press [5] to change your boots\n"
                      "Press [6] to change your charm\n"
                      "Press [7] to change your ring\n"
                      )
    if equip_tab == "1":
        owned_weapons = [item for item in inventory if item in game_content["items"]["weapons"]]
        print("Owned weapons:", owned_weapons)
        equip_weapon_id = input("Select a weapon you wish to equip.\n")
        if equip_weapon_id not in owned_weapons:
            print("You do not own this weapon. Please choose again.")
            return
        else:
            equip_weapon = Item(equip_weapon_id, ItemTypeEnum.WEAPON)
            print(f"You switched {player.weapon.name} for {equip_weapon.name}.")

            inventory.append(player.weapon.get_id())
            player.weapon = equip_weapon
            inventory.remove(equip_weapon_id)
    elif equip_tab == "2":
        owned_helmets = [item for item in inventory if item in game_content["items"]["helmets"]]
        print("Owned helmets:", owned_helmets)
        equip_helmets_id = input("Select a helmet you wish to equip.\n")
        if equip_helmets_id not in owned_helmets:
            print("You do not own this helmet. Please choose again.")
            return
        else:
            equip_helmet = Item(equip_helmets_id, ItemTypeEnum.HELMET)
            print(f"You switched {player.helmet.name} for {equip_helmet.name}.")

            inventory.append(player.helmet.get_id())
            player.helmet = equip_helmet
            inventory.remove(equip_helmets_id)
    elif equip_tab == "3":
        owned_chestpieces = [item for item in inventory if item in game_content["items"]["chestpieces"]]
        print("Owned chestpieces:", owned_chestpieces)
        equip_chestpiece_id = input("Select a chestpiece you wish to equip.\n")
        if equip_chestpiece_id not in owned_chestpieces:
            print("You do not own this chestpiece. Please choose again.")
            return
        else:
            equip_chestpiece = Item(equip_chestpiece_id, ItemTypeEnum.CHESTPIECE)
            print(f"You switched {player.chestpiece.name} for {equip_chestpiece.name}.")

            inventory.append(player.chestpiece.get_id())
            player.chestpiece = equip_chestpiece
            inventory.remove(equip_chestpiece_id)
    elif equip_tab == "4":
        owned_leggings = [item for item in inventory if item in game_content["items"]["leggings"]]
        print("Owned leggings:", owned_leggings)
        equip_leggings_id = input("Select a legging you wish to equip.\n")
        if equip_leggings_id not in owned_leggings:
            print("You do not own this legging. Please choose again.")
            return
        else:
            equip_leggings = Item(equip_leggings_id, ItemTypeEnum.LEGGINGS)
            print(f"You switched {player.leggings.name} for {equip_leggings.name}.")

            inventory.append(player.leggings.get_id())
            player.leggings = equip_leggings
            inventory.remove(equip_leggings_id)
    elif equip_tab == "5":
        owned_boots = [item for item in inventory if item in game_content["items"]["boots"]]
        print("Owned boots:", owned_boots)
        equip_boots_id = input("Select a pair of boots you wish to equip.\n")
        if equip_boots_id not in owned_boots:
            print("You do not own this pair of boots. Please choose again.")
            return
        else:
            equip_boots = Item(equip_boots_id, ItemTypeEnum.BOOTS)
            print(f"You switched {player.boots.name} for {equip_boots.name}.")

            inventory.append(player.boots.get_id())
            player.boots = equip_boots
            inventory.remove(equip_boots_id)
    elif equip_tab == "6":
        owned_charms = [item for item in inventory if item in game_content["items"]["charms"]]
        print("Owned charms:", owned_charms)
        equip_charm_id = input("Select a charm you wish to equip.\n")
        if equip_charm_id not in owned_charms:
            print("You do not own this charm. Please choose again.")
            return
        else:
            equip_charm = Item(equip_charm_id, ItemTypeEnum.CHARM)
            print(f"You switched {player.charm.name} for {equip_charm.name}.")

            inventory.append(player.charm.get_id())
            player.charm = equip_charm
            inventory.remove(equip_charm_id)
    elif equip_tab == "7":
        owned_rings = [item for item in inventory if item in game_content["items"]["rings"]]
        print("Owned rings:", owned_rings)
        equip_ring_id = input("Select a ring you wish to equip.\n")
        if equip_ring_id not in owned_rings:
            print("You do not own this ring. Please choose again.")
            return
        else:
            equip_ring = Item(equip_ring_id, ItemTypeEnum.RING)
            print(f"You switched {player.ring.name} for {equip_ring.name}.")

            inventory.append(player.ring.get_id())
            player.ring = equip_ring
            inventory.remove(equip_ring_id)
    else:
        print("Invalid input, returning.")
        return

def const_choices(input_value):
    input_value = input_value.lower()

    if input_value == "i":
        print("Here is your Inventory: ")
        for item_type in game_content["items"].keys():
            for item_id in game_content["items"][item_type].keys():
                if item_id in inventory:
                    print(Item(item_id, ItemTypeEnum(item_type)))
        print()

    elif input_value == "e":
        equipment_tab()

    else:
        print("Invalid input. Please choose again.")
        print()

def display_encounter(encounter_name):
    encounters = game_content["encounters"]
    if encounter_name not in encounters:
        print("No such encounter found!")
        return

    encounter = encounters[encounter_name]
    print(encounter["description"])
    print("\nChoices:")

    for key, _choice in encounter["choices"].items():
        print(f"[{key}] {_choice['text']}")

    while True:
        player_choice = input("What do you do? ")
        if player_choice in ["i", "e"]:
            const_choices(player_choice)
            continue

        if player_choice in encounter["choices"]:
            choice_details = encounter["choices"][player_choice]
            print("\n" + choice_details["response"])

            if "inventory_add" in choice_details:
                new_items = choice_details["inventory_add"]
                for item_id in new_items:
                    inventory.append(item_id)
                    print(
                        f"Added {', '.join([str(Item(item_id, ItemTypeEnum(get_item_type(item_id)))) for item_id in inventory[-len(new_items):]])} to inventory.")

            if "requirements" in choice_details:
                required_items = choice_details["requirements"]
                missing_items = [item for item in required_items if item not in inventory]

                if missing_items:
                    print(f"You do not have {', '.join(missing_items)} in your inventory.")
                    continue

                for item in required_items:
                    print(f"Lost {item} from inventory.")
                    inventory.remove(item)

            if "combat" in choice_details:
                enemy_name = choice_details["combat"]
                enemy_type = get_enemy_type(enemy_name)

                enemy = Enemy(enemy_name, enemy_type)

                if enemy:
                    combat(player, enemy)
                else:
                    print(f"Enemy {enemy_name} not found!")
                break

            if "health" in choice_details:
                player.health += choice_details["health"]
                if player.health <= 0:
                    print("You have died.")
                    break

            if "gold" in choice_details:
                player.gold += choice_details["gold"]
                print(f"You have gained {choice_details['gold']} gold.")


            if "next" in choice_details:
                display_encounter(choice_details["next"])
                break
        else:
            print("Invalid choice. Please try again.")

random_encounter_count = 0
events = ["farmer_help", "haunted_mill", "silver_stag_tale", "abandoned_church"]

def random_event():
    global random_encounter_count
    while random_encounter_count < 15:
        random_encounter = random.choice(events)
        events.remove(random_encounter)
        display_encounter(random_encounter)
        random_encounter_count += 1

    # anchor_event_1()
    #
    # while random_encounter_count < 30:
    #     random_encounter = random.choice(events)
    #     events.remove(random_encounter)
    #     display_encounter(random_encounter)
    #     random_encounter_count += 1


def crit_hit(character) -> bool:
    critChance = (character.critChance +
                  character.weapon.stats.critChance if character.weapon is not None else 0 +
                  character.charm.stats.critChance if character.charm is not None else 0 +
                  character.ring.stats.critChance if character.ring is not None else 0
                  )
    n = random.randint(1, 100)
    if n < critChance * 100:
        return True
    return False
def crit_enemy_hit(enemy) -> bool:
    n = random.randint(1, 100)
    if n < enemy.stats.critChance * 100:
        return True
    return False

def check_pierce(character: Character):
    if character.weapon is not None and character.weapon.skills == "pierce":
        return True
    elif character.charm is not None and character.charm.skills == "pierce":
        return True
    elif character.ring is not None and character.ring.skills == "pierce":
        return True
    return False

def check_doublehit(character: Character):
    if character.weapon is not None and character.weapon.skills == "doublehit":
        return True
    elif character.charm is not None and character.charm.skills == "doublehit":
        return True
    elif character.ring is not None and character.ring.skills == "doublehit":
        return True
    return False

def is_attribute_strong(character: Character, enemy: Enemy) -> bool:
    if character.weapon is None or character.weapon.attribute is None:
        return False

    strong_combinations = {
        "fire": ["ice", "undead", "natural", "cursed"],
        "ice": ["natural", "lightning"],
        "holy": ["undead", "cursed"],
        "water": ["fire"],
        "lightning": ["water", "natural", "arcane"],
        "cursed": ["natural", "arcane"],
        "necrotic": ["natural", "water"],
        "physical": ["lightning"],
        "natural": ["water", "physical"],
        "arcane": ["physical", "natural", "undead", "ice"]
    }

    if isinstance(enemy.attributes, (list, set)):
        result = any(attr in strong_combinations.get(character.weapon.attribute, []) for attr in enemy.attributes)
    else:
        result = enemy.attributes in strong_combinations.get(character.weapon.attribute, [])

    print(f"is_attribute_strong result: {result}")
    return result

def is_attribute_weak(character: Character, enemy: Enemy) -> bool:
    if character.weapon is None or character.weapon.attribute is None:
        return False
    weak_combinations = {
        "fire": ["water"],
        "ice": ["fire","arcane"],
        "holy": ["arcane"],
        "water": ["lightning", "natural","undead"],
        "lightning": ["ice"],
        "cursed": ["holy"],
        "necrotic": ["arcane", "holy"],
        "physical": ["arcane", "natural"],
        "natural": ["fire", "arcane","undead","ice"],
        "arcane": ["holy", "lightning", "cursed"]
    }
    if isinstance(enemy.attributes, (list, set)):
        result = any(attr in weak_combinations.get(character.weapon.attribute, []) for attr in enemy.attributes)
    else:
        result = enemy.attributes in weak_combinations.get(character.weapon.attribute, [])

    print(f"is_attribute_weak result: {result}")
    return result

def apply_weapon_attribute_effect(character: Character, enemy: Enemy):
    if character.weapon is None or character.weapon.attribute is None:
        return 1

    is_strong = is_attribute_strong(character, enemy)
    is_weak = is_attribute_weak(character, enemy)

    if is_strong:
        return 2
    elif is_weak:
        return 0.5
    return 1

def calculate_damage_dealt(character: Character, enemy: Enemy):
    pierce = check_pierce(character)
    doublehit = check_doublehit(character)
    modifier = apply_weapon_attribute_effect(character, enemy)
    crit_modifier = crit_hit(character)
    attackDmg = (character.attackDmg +
                 character.weapon.stats.attackDmg if character.weapon is not None else 0 +
                 character.ring.stats.attackDmg if character.charm is not None else 0  +
                 character.charm.stats.attackDmg if character.ring is not None else 0
                 )

    # print(f"Character weapon attribute: {character.weapon.attribute}")
    # print(f"Enemy attributes: {enemy.attributes}")
    # print(f"Base attack damage: {attackDmg}")
    # print(f"Crit modifier: {crit_modifier}")
    # print(f"Attribute modifier: {modifier}")
    # print(f"Pierce check: {pierce}")
    # print(f"Enemy defense: {enemy.stats.defense}")



    if crit_modifier:
        damage = (modifier * attackDmg * 2) - enemy.stats.defense
    elif crit_modifier and pierce:
        damage = (modifier * attackDmg * 2)
    elif pierce:
        damage = (modifier * attackDmg)
    elif crit_modifier and doublehit:
        damage = ((modifier * attackDmg * 2) - enemy.stats.defense) * 2
    elif pierce and doublehit:
        damage = (modifier * attackDmg) * 2
    elif doublehit:
        damage = ((modifier * attackDmg) - enemy.stats.defense) * 2
    elif crit_modifier and pierce and doublehit:
        damage = (modifier * attackDmg * 2) * 2
    else:
        damage = (modifier * attackDmg) - enemy.stats.defense
    damage = max(damage, 0)
    return damage

def calculate_damage_taken(enemy: Enemy, character: Character):
    crit_modifier = crit_enemy_hit(enemy)
    if crit_modifier:
        damage = (enemy.stats.attackDmg * 2) - character.defense
    else:
        damage = enemy.stats.attackDmg - character.defense
    damage = max(damage,0)
    return damage

def combat(character: Character, enemy: Enemy) -> None:
    while character.health > 0 and enemy.stats.health > 0:
        damage_taken = calculate_damage_taken(enemy, character)
        damage_dealt = calculate_damage_dealt(character, enemy)

        enemy.stats.health -= damage_dealt
        print(f"Damage dealt: {damage_dealt}")
        print(f"Enemy's remaining health: {enemy.stats.health}")
        if enemy.stats.health < 0:
            enemy.stats.health = 0
            break

        character.health -= damage_taken
        print(f"Damage taken: {damage_taken}")
        if character.health < 0:
            character.health = 0
            break

    if character.health <= 0:
        print(f"{character.name} is dead.")
    else:
        character._health = character.base_health
        print(f"{enemy.name} is dead.")

# if "excalibur" in inventory:
#     print(\n"ACHIEVEMENT: You have found the legendary sword Excalibur!\n")
#     print("You have gained 1000 gold.")
#     player.gold += 1000


def main():
    starting_story_1 = """
You stood before the Adventurers' Guild, heart racing with excitement. 
You pushed open the heavy wooden doors and stepped into a room bathed in warm, amber light. 
The air smelled of leather and firewood, and a crackling fireplace to your right cast shadows across the walls. 
To your left, a job board was covered in parchment quests, from humble tasks to mysterious adventures.

"New here, are you?" a calm, melodic voice said from behind you.

You turned to see an elf with silver hair and piercing green eyes. Her smile was warm yet graceful. 
"Welcome to the Adventurers' Guild," she said, extending a slender hand. 
"I am Elara, and it’s my pleasure to greet those who are taking their first steps toward adventure. May I ask for your name?"

You introduced yourself, feeling a surge of excitement.
"""

    starting_story_2 = """
"A fine name," she replied. "Follow me, and I’ll show you where your journey begins."

Elara led you down a narrow stairway, the sounds of the guild fading behind them. 
At the bottom, you entered the armory, a room lined with racks of swords, shields, bows, and staves, 
each weapon catching the warm glow of wall sconces.

"Every adventurer needs a weapon they can trust," Elara said, gesturing to the selection. 
"Take your time, look around, and choose what speaks to you."

You examined each weapon carefully, feeling their weight and balance, while Elara watched with a gentle smile. 
"Whatever you choose," she said, "remember that this weapon is only an extension of your spirit. 
The true strength lies within."

Two weapons stole your eyes however, a sword and a lance. You felt that your journey should begin with this first choice.
"""

    common_sword_description = game_content["items"]["weapons"]["common_sword"]["description"]
    common_lance_description = game_content["items"]["weapons"]["common_lance"]["description"]

    print(starting_story_1)
    player.name = input("What is your name? ").lower().title()

    print(player)

    print(starting_story_2)
    starting_weapon_choice = input("Choose your weapon: sword or lance? ").lower()

    if starting_weapon_choice == "sword":
        print(common_sword_description)
        choice = input("Do you pick up this weapon? ")
        if choice == "yes":
            player.weapon = Item("common_sword", ItemTypeEnum.WEAPON)
            print(f"You have picked up the Sword. Player's weapon: {player.weapon}")
        elif choice == "no":
            return
        else:
            print("Invalid input, please choose again.")
            return

    elif starting_weapon_choice == "lance":
        print(common_lance_description)
        choice = input("Do you pick up this weapon? ")
        if choice == "yes":
            player.weapon = Item("common_lance", ItemTypeEnum.WEAPON)
            print(f"You have picked up the Lance. Player's weapon: {player.weapon}")
        elif choice == "no":
            return
        else:
            print("Invalid input, please choose again.")
            return
    else:
        print("Invalid input, please choose again.")
        return

    random_event()

main()