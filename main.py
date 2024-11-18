import random
from collections import Counter
import json
from enums import ItemTypeEnum

from typing import Optional


with open('game_content.json', 'r') as file:
    game_content = json.load(file)


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
            defense=game_content["items"][self.item_type.value][self._id].get("defense", 0)
        )
        self.attribute = game_content["items"][item_type.value][item_id].get("attribute")
        self.rarity = game_content["items"][item_type.value][item_id]["rarity"]

    def __repr__(self):
        # For simplicity, you can adjust this representation to show name, rarity, and damage/defense
        if self.item_type == ItemTypeEnum.WEAPON:
            return f"{self.name} (Attack Damage: {self.stats.attackDmg}, Attribute {self.attribute}, Rarity: {self.rarity})"
        return f"{self.name} (Defense: {self.stats.defense}, Attribute {self.attribute}, Rarity: {self.rarity})"

    def get_id(self):
        return self._id


def get_item_type(item_id):
    # Check each category for the item_id
    for category, items in game_content["items"].items():
        if item_id in items:  # If item_id exists in the category
            return category  # Return the category (item_type) where the item_id was found
    # If the item is not found in any category, raise an error
    raise ValueError(f"Item ID '{item_id}' not found in any known category.")


class Enemy:
    def __init__(self,category,enemy_type):
        enemy_data = game_content["enemies"][category][enemy_type]

        self.name = enemy_data["name"]
        self.description = enemy_data["description"]
        self.stats = Stats(**enemy_data["stats"])
        self.attributes = enemy_data["attributes"]

    def __repr__(self):
        return (f"Enemy(name={self.name}, description={self.description},",
                f"stats={self.stats}, attributes={self.attributes})")

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

        self.defence: int = 0
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
        print(f"Health is now: {self.health}")



    def __str__(self):
        return (
            f"Character Info:\n"
            f"Name: {self.name}\n"
            f"Weapon: {self.weapon.name if self.weapon else 'None'}\n"  # Safe access to a weapon
            f"Head: {self.helmet}\n"
            f"Top: {self.chestpiece}\n"
            f"Bottom: {self.leggings}\n"
            f"Feet: {self.boots}\n"
            f"Charm: {self.charm}\n"
            f"Ring: {self.ring.name if self.ring else 'None'}\n"  # Safe access to ring
            f"Health: {self.health}\n"
            f"Defence: {self.defence}\n"
            f"Attack Damage: {self.attackDmg}\n"
            f"Critical Damage: {self.critDmg}\n"
            f"Critical Chance: {self.critChance * 100}%\n"
            f"Gold: {self.gold}\n"
        )

inventory = ["excalibur"]
inventory_count = Counter(inventory)

def const_choices(input_value):
    input_value = input_value.lower()

    if input_value == "i":
        print("Here is your Inventory: ")
        for item_type in game_content["items"].keys():
            for item_id in game_content["items"][item_type].keys():
                if item_id in inventory:
                    print(Item(item_id, ItemTypeEnum(item_type)))
        # for item_id in inventory:
        #     if item_id in game_content["items"]["weapons"]:
        #         item = Item(item_id, "weapons")  # Create Item object for weapons
        #         print(
        #             f"- {item.name} (Attack Damage: {item.attackDmg}, Attribute: {item.attribute}, Rarity: {item.rarity})")
        #     elif item_id in game_content["items"]["rings"]:
        #         item = Item(item_id, "rings")  # Create Item object for rings
        #         print(f"- {item.name} (Defense: {item.defense}, Attribute: {item.attribute}, Rarity: {item.rarity})")
        print()

    elif input_value == "e":
        print("This is your current equipment:\n")
        print(player)
        equip_tab = input("Press [1] to change your weapon\nPress [2] to change your ring\n")
        if equip_tab == "1":
            owned_weapons = [item for item in inventory if item in game_content["items"]["weapons"]]
            print("Owned weapons:", owned_weapons)
            equip_weapon_id = input("Select a weapon you wish to equip.\n")
            if equip_weapon_id not in owned_weapons:
                print("You do not own this weapon. Please choose again.")
                return
            else:
                # Create an Item object for the selected weapon
                equip_weapon = Item(equip_weapon_id, ItemTypeEnum.WEAPON)
                print(f"You switched {player.weapon.name} for {equip_weapon.name}.")

                # Add an old weapon back to inventory and equip new one
                inventory.append(player.weapon.get_id())
                player.weapon = equip_weapon  # Equip a new weapon (as an Item object)
                inventory.remove(equip_weapon_id)  # Remove the selected weapon from inventory
        elif equip_tab == "2":
            owned_rings = [item for item in inventory if item in game_content["items"]["rings"]]
            print("Owned rings:", owned_rings)
            equip_ring_id = input("Select a ring you wish to equip.\n")
            if equip_ring_id not in owned_rings:
                print("You do not own this ring. Please choose again.")
                return
            else:
                equip_ring = Item(equip_ring_id, ItemTypeEnum.RING)  # Create the ring object
                print(f"You switched {player.ring.name} for {equip_ring.name}.")

                # Add old ring back to inventory and equip new one
                inventory.append(player.ring.get_id())
                player.ring = equip_ring  # Equip new ring
                inventory.remove(equip_ring_id)  # Remove selected ring from inventory


    else:
        print("Invalid input. Please choose again.")
        print()


def display_encounter(encounter_name):
    encounters = game_content["encounters"]
    if encounter_name not in encounters:
        print("No such encounter found!")
        return

    # Load the encounter details
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

                    # Add the item ID to the inventory (not the Item object)
                    inventory.append(item_id)

                    # Print the added items
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

            #### Handle combat or progress ####

            # if "combat" in choice_details:
            # print(choice_details["combat"]) # Combat logic here
            # break # Return to encounter after combat
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

player = Character()
skeleton = Enemy("enemies", "undead")

def crit_hit(character: Character) -> bool:
    n = random.randint(1, 100)
    if n < character.critChance * 100:
        return True
    return False

def attribute_hit(character: Character, enemy: Enemy):
    if character.weapon.attribute == "fire" and enemy.attributes == "ice":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "fire" and enemy.attributes == "undead":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "fire" and enemy.attributes == "natural":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "fire" and enemy.attributes == "cursed":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "fire" and enemy.attributes == "water":
        character.attackDmg = character.attackDmg * 0.5
    elif character.weapon.attribute == "ice" and enemy.attributes == "natural":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "ice" and enemy.attributes == "water":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "ice" and enemy.attributes == "fire":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "ice" and enemy.attributes == "lightning":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "ice" and enemy.attributes == "arcane":
        character.attackDmg = character.attackDmg * 0.5
    elif character.weapon.attribute == "holy" and enemy.attributes == "undead":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "holy" and enemy.attributes == "cursed":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "holy" and enemy.attributes == "arcane":
        character.attackDmg = character.attackDmg * 0.5
    elif character.weapon.attribute == "water" and enemy.attributes == "fire":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "water" and enemy.attributes == "ice":
        character.attackDmg = character.attackDmg * 0.5
    elif character.weapon.attribute == "water" and enemy.attributes == "natural":
        character.attackDmg = character.attackDmg * 0.5
    elif character.weapon.attribute == "water" and enemy.attributes == "lightning":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "lightning" and enemy.attributes == "water":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "lightning" and enemy.attributes == "ice":
        character.attackDmg = character.attackDmg * 0.5
    elif character.weapon.attribute == "lightning" and enemy.attributes == "natural":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "lightning" and enemy.attributes == "arcane":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "cursed" and enemy.attributes == "natural":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "cursed" and enemy.attributes == "holy":
        character.attackDmg = character.attackDmg * 0.5
    elif character.weapon.attribute == "cursed" and enemy.attributes == "arcane":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "necrotic" and enemy.attributes == "natural":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "necrotic" and enemy.attributes == "arcane":
        character.attackDmg = character.attackDmg * 0.5
    elif character.weapon.attribute == "necrotic" and enemy.attributes == "holy":
        character.attackDmg = character.attackDmg * 0.5
    elif character.weapon.attribute == "physical" and enemy.attributes == "arcane":
        character.attackDmg = character.attackDmg * 0.5
    elif character.weapon.attribute == "physical" and enemy.attributes == "natural":
        character.attackDmg = character.attackDmg * 0.5
    elif character.weapon.attribute == "physical" and enemy.attributes == "lightning":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "natural" and enemy.attributes == "water":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "natural" and enemy.attributes == "fire":
        character.attackDmg = character.attackDmg * 0.5
    elif character.weapon.attribute == "natural" and enemy.attributes == "physical":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "natural" and enemy.attributes == "arcane":
        character.attackDmg = character.attackDmg * 0.5
    elif character.weapon.attribute == "arcane" and enemy.attributes == "physical":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "arcane" and enemy.attributes == "natural":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "arcane" and enemy.attributes == "undead":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "arcane" and enemy.attributes == "ice":
        character.attackDmg = character.attackDmg * 2
    elif character.weapon.attribute == "arcane" and enemy.attributes == "holy":
        character.attackDmg = character.attackDmg * 0.5
    elif character.weapon.attribute == "arcane" and enemy.attributes == "lightning":
        character.attackDmg = character.attackDmg * 0.5
    elif character.weapon.attribute == "arcane" and enemy.attributes == "cursed":
        character.attackDmg = character.attackDmg * 0.5




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

    common_sword_description = """ 
A versatile weapon, the sword offers a balance of speed and power.
It excels in close combat with quick strikes, effective parries, and swift counters. 
Ideal for players who prefer agility and adaptability, 
the sword is perfect for fast, fluid combat where precision and reaction are key.
"""

    common_lance_description = """ 
The lance is a long-reaching weapon designed for powerful thrusts and charging attacks. 
While slower in close combat, its extended reach lets you control distance and strike from afar. 
Ideal for players who value strength and tactical positioning, 
the lance excels in keeping enemies at bay and delivering powerful blows from a safe range.
"""
    print(starting_story_1)
    player.name = input("What is your name? ").lower().title()

    print(player)

    print(starting_story_2)
    starting_weapon_choice = input("Choose your weapon: sword or lance? ").lower()

    if starting_weapon_choice == "sword":
        print(common_sword_description)
        choice = input("Do you pick up this weapon? ")
        if choice == "yes":
            # Assign a weapon as an Item object
            player.weapon = Item("common_sword", ItemTypeEnum.WEAPON)  # Use the 'Item' class to handle a weapon
        elif choice == "no":
            print()
        else:
            print("Invalid input, defaulting to sword.")
            player.weapon = Item("common_sword", ItemTypeEnum.WEAPON)
            print()

    elif starting_weapon_choice == "lance":
        print(common_lance_description)
        choice = input("Do you pick up this weapon? ")
        if choice == "yes":
            # Assign a weapon as an Item object
            player.weapon = Item("common_lance", ItemTypeEnum.WEAPON)
        elif choice == "no":
            print()
        else:
            print("Invalid input, please choose again.")
            print()

    random_event()

main()