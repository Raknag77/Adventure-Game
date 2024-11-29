import random
from collections import Counter
import json

from game_enums import EnemyTypeLiteral, ItemTypeEnum, EnemyTypeEnum, ItemTypeLiteral
from typing import List, Optional

from game_content_typing import GameContentType

# with open('game_content.json', 'r') as file:
#     game_content: GameContentType = json.load(file)
with open('Content/encounter_data.json', 'r') as file:
    encounter_data = json.load(file)
with open('Content/item_data.json', 'r') as file:
        item_data = json.load(file)
with open('Content/enemy_data.json', 'r') as file:
    enemy_data = json.load(file)

random_encounter_count = 0
events = ["farmer_help", "haunted_mill", "silver_stag_tale", "abandoned_church","burnt_forest"]

inventory = ["excalibur"]

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

class Item:
    def __init__(self, item_id: str, item_type: ItemTypeEnum):
        self._id = item_id
        self.item_type = item_type

        item_type_value: ItemTypeLiteral = item_type.value
        self.name = item_data["items"][item_type_value][item_id]["name"]
        self.description = item_data["items"][item_type_value][item_id]["description"]
        self.stats = Stats(**item_data["items"][item_type_value][self._id].get("stats", {}))
        self.attribute = item_data["items"][item_type_value][item_id].get("attribute")
        self.rarity = item_data["items"][item_type_value][item_id]["rarity"]
        self.price = item_data["items"][item_type_value][item_id].get("price")
        self.skills = item_data["items"][item_type_value][item_id].get("skills")

    def __repr__(self):
        if self.item_type == ItemTypeEnum.WEAPON:
            return (f"{self.name}- Price: {self.price} gold\n"
                    f"      Attack Damage: {self.stats.attackDmg}\n"
                    f"      Critical Chance: {self.stats.critChance}\n"
                    f"      Attribute: {self.attribute}\n"
                    f"      Rarity: {self.rarity}\n"
                    f"      Skills: {self.skills}\n")
        if self.item_type == ItemTypeEnum.CHARM or self.item_type == ItemTypeEnum.RING:
            return (f"{self.name}- Price: {self.price} gold\n"
                    f"      Attack Damage: {self.stats.attackDmg}\n"
                    f"      Critical Chance: {self.stats.critChance}\n"
                    f"      Health: {self.stats.health}\n"
                    f"      Defense: {self.stats.defense}\n"
                    f"      Agility: {self.stats.agility}\n"
                    f"      Luck: {self.stats.luck}\n"
                    f"      Attribute: {self.attribute}\n"
                    f"      Rarity: {self.rarity}\n"
                    f"      Skills: {self.skills}\n")
        if self.item_type == ItemTypeEnum.MATERIAL:
            return (f"{self.name}- Price: {self.price} gold\n"
                    f"      Attribute: {self.attribute}\n"
                    f"      Rarity: {self.rarity}\n")
        return (f"{self.name}- Price: {self.price} gold\n"
                f"      Health: {self.stats.health}\n"
                f"      Defense: {self.stats.defense}\n"
                f"      Agility: {self.stats.agility}\n"
                f"      Attribute: {self.attribute}\n"
                f"      Rarity: {self.rarity}\n"
                f"      Skills: {self.skills}\n")

    def get_id(self):
        return self._id

def get_item_type(item_id):
    # Check each category for the item_id
    for category, items in item_data["items"].items():
        if item_id in items:  # If item_id exists in the category
            return category  # Return the category (item_type) where the item_id was found
    # If the item is not found in any category, raise an error
    raise ValueError(f"Item ID '{item_id}' not found in any known category.")

def get_enemy_type(enemy_name: str) -> Optional[EnemyTypeEnum]:
    for category, enemies in enemy_data["enemies"].items():
        if enemy_name.lower() in [key.lower() for key in enemies.keys()]:
            return EnemyTypeEnum(category)
    print(f"Enemy '{enemy_name}' not found!")
    return None

def get_random_enemy_instance():
    category_name = random.choice(list(enemy_data['enemies'].keys()))

    category = enemy_data['enemies'][category_name]
    enemy_id = random.choice(list(category.keys()))

    enemy_type_enum = EnemyTypeEnum[category_name.upper()]
    enemy_instance = Enemy(enemy_id=enemy_id, enemy_type=enemy_type_enum)

    return enemy_instance

class Enemy:
    def __init__(self, enemy_id: str, enemy_type: EnemyTypeEnum):
        self._id = enemy_id
        self.enemy_type = enemy_type

        enemy_type_value: EnemyTypeLiteral = enemy_type.value
        self.name = enemy_data["enemies"][enemy_type_value][enemy_id]["name"]
        self.description = enemy_data["enemies"][enemy_type_value][enemy_id]["description"]
        self.stats = Stats(**enemy_data["enemies"][enemy_type_value][enemy_id].get("stats", {}))
        self.attributes = enemy_data["enemies"][enemy_type_value][enemy_id]["attributes"]

    def __repr__(self):
        return (
            f"  name: {self.name},\n"
            f"  description: {self.description},\n"
            f"  defense: {self.stats.defense},\n"
            f"  agility: {self.stats.agility},\n"
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

        self.stats = Stats(
            50, 0, 1, 10, 0.01,0
        )
        self.base_health: int = 50
        self.gold: int = 1000

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
        return self.stats.health + bonus_health

    @health.setter
    def health(self, new_health: int):
        self.stats.health = new_health
        print(f"Base Health (without bonuses) is now: {self.stats.health}")

    def reset_health(self):
        self.current_health = self.health

    def __str__(self):
        temp_health = self.stats.health
        self.stats.health = self.health
        return_string = (
            f"Character Info:\n"
            f"Name: {self.name}\n"
            f"Weapon: {self.weapon.name if self.weapon else 'None'}\n"
            f"Head: {self.helmet.name if self.helmet else 'None'}\n"
            f"Top: {self.chestpiece.name if self.chestpiece else 'None'}\n"
            f"Bottom: {self.leggings.name if self.leggings else 'None'}\n"
            f"Feet: {self.boots.name if self.boots else 'None'}\n"
            f"Charm: {self.charm.name if self.charm else 'None'}\n"
            f"Ring: {self.ring.name if self.ring else 'None'}\n"
            f"{self.stats}\n"
            f"Gold: {self.gold}\n"
        )
        self.stats.health = temp_health
        return return_string

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
        owned_weapons = [item for item in inventory if item in item_data["items"]["weapons"]]
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
        owned_helmets = [item for item in inventory if item in item_data["items"]["helmets"]]
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
        owned_chestpieces = [item for item in inventory if item in item_data["items"]["chestpieces"]]
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
        owned_leggings = [item for item in inventory if item in item_data["items"]["leggings"]]
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
        owned_boots = [item for item in inventory if item in item_data["items"]["boots"]]
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
        owned_charms = [item for item in inventory if item in item_data["items"]["charms"]]
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
        owned_rings = [item for item in inventory if item in item_data["items"]["rings"]]
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
        print("Here is your Inventory:")

        inventory_counts = Counter(inventory)

        for item_type in item_data["items"].keys():
            for item_id, item_data_entry in item_data["items"][item_type].items():
                if item_id in inventory_counts:
                    item_instance = Item(item_id, ItemTypeEnum(item_type))
                    count = inventory_counts[item_id]
                    print(f"{item_instance} (x{count})")

        if not inventory_counts:
            print("Your inventory is empty.")
        print()

    elif input_value == "e":
        equipment_tab()

    else:
        print("Invalid input. Please choose again.")
        print()

def loot(character, enemy):
    loot_data = None
    for category in enemy_data['enemies'].values():
        if enemy in category:
            loot_data = category[enemy].get('loot', None)
            break

    if loot_data:
        for item in loot_data:
            item_name = item['item']
            item_rarity = item['rarity']

            if item_rarity == "common":
                common_loot_chance = random.randint(1, 100)
                if common_loot_chance < 75 + character.stats.luck:
                    inventory.append(item_name)
                    print(f"Loot added: {item_name}")
                else:
                    print(f"No loot found on {item_name}.")
            elif item_rarity == "rare":
                rare_loot_chance = random.randint(1, 100)
                if rare_loot_chance < 40 + character.stats.luck:
                    inventory.append(item_name)
                    print(f"Loot added: {item_name}")
                else:
                    print(f"No loot found on {item_name}.")
            elif item_rarity == "exquisite":
                exquisite_loot_chance = random.randint(1, 100)
                if exquisite_loot_chance < 15 + character.stats.luck:
                    inventory.append(item_name)
                    print(f"Loot added: {item_name}")
                else:
                    print(f"No loot found on {item_name}.")
            elif item_rarity == "legendary":
                legendary_loot_chance = random.randint(1, 100)
                if legendary_loot_chance < 1 + character.stats.luck:
                    inventory.append(item_name)
                    print(f"Loot added: {item_name}")
                else:
                    print(f"No loot found on {item_name}.")
            else:
                print(f"No loot found on {item_name}.")

    else:
        print(f"No loot found on {enemy}")

def shop(character: Character):
    shop_items: List[Item] = []

    for i in range(3):
        random_item_category: ItemTypeLiteral = random.choice(list(item_data["items"].keys()))
        random_item_id = random.choice(
            list(item_data["items"][random_item_category].keys()))
        item_type_value = get_item_type(random_item_id)
        shop_item = Item(random_item_id, ItemTypeEnum(item_type_value))
        shop_items.append(shop_item)

        print(shop_item)

    purchase = input("Select an item you wish to purchase!\n")

    if purchase.strip().lower() not in ["1", "2", "3"]:
        print("Invalid input, returning.")
        return

    purchase_number = int(purchase) - 1
    selected_shop_item = shop_items[purchase_number]

    if character.gold > selected_shop_item.price:
        print(f"You have purchased {selected_shop_item}!")
        character.gold -= selected_shop_item.price
        inventory.append(selected_shop_item.get_id())
    else:
        print("You do not have enough money to purchase this item!")

def job_board():
    enemy_instance = get_random_enemy_instance()
    print(f"Nearby village is being attacked by \n{enemy_instance.name}.")
    combat_result = combat(player, enemy_instance)

    if not combat_result:  # Player lost
        print("Game over! Reload your save or try again.")
        # Add logic for game-over scenario here (e.g., restart, quit, or reload).
    else:  # Player won
        print("Searching for loot...")
        loot(player,enemy_instance)
        if loot:
            print(f"You found: {loot}")
        else:
            print(f"No loot found on {enemy_instance.name}.")

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



def evasion(character) -> bool:
    agility = (
            character.stats.agility +
            (character.weapon.stats.agility if character.weapon is not None else 0) +
            (character.charm.stats.agility if character.charm is not None else 0) +
            (character.ring.stats.agility if character.ring is not None else 0)
            )
    n = random.randint(1, 100)
    if n < agility:
        return True
    return False

def crit_hit(character) -> bool:
    critChance = (
            character.stats.critChance +
            (character.weapon.stats.critChance if character.weapon is not None else 0) +
            (character.charm.stats.critChance if character.charm is not None else 0) +
            (character.ring.stats.critChance if character.ring is not None else 0)
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
        "ice": ["fire", "arcane"],
        "holy": ["arcane"],
        "water": ["lightning", "natural", "undead"],
        "lightning": ["ice"],
        "cursed": ["holy"],
        "necrotic": ["arcane", "holy"],
        "physical": ["arcane", "natural"],
        "natural": ["fire", "arcane", "undead", "ice"],
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
    attackDmg = (
            character.stats.attackDmg +
            (character.weapon.stats.attackDmg if character.weapon is not None else 0) +
            (character.charm.stats.attackDmg if character.charm is not None else 0) +
            (character.ring.stats.attackDmg if character.ring is not None else 0)
    )
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
        damage = (enemy.stats.attackDmg * 2) - character.stats.defense
    else:
        damage = enemy.stats.attackDmg - character.stats.defense
    damage = max(damage, 0)
    return damage


def combat(character, enemy):
    # Ensure combat starts with current health initialized
    character.current_health = character.health
    print(f"{character.name}'s starting health: {character.current_health}")

    while character.current_health > 0 and enemy.stats.health > 0:
        dodge = evasion(character)
        damage_taken = calculate_damage_taken(enemy, character)
        if dodge:
            damage_taken = 0

        damage_dealt = calculate_damage_dealt(character, enemy)
        enemy.stats.health -= damage_dealt
        print(f"Damage dealt to {enemy.name}: {damage_dealt}")
        print(f"{enemy.name}'s remaining health: {max(enemy.stats.health, 0)}")

        if enemy.stats.health <= 0:
            print(f"{enemy.name} is dead.")
            break

        character.current_health -= damage_taken
        print(f"Damage taken: {damage_taken}")
        print(f"{character.name}'s remaining health: {max(character.current_health, 0)}")

        if character.current_health <= 0:
            print(f"{character.name} is dead.")
            break

    # Post-combat handling
    if character.current_health <= 0:
        print("Game over! Reload your save or try again.")
        return False
    else:
        character.reset_health()
        print("You have won the battle!")
        return True


# if "excalibur" in inventory:
#     print(\n"ACHIEVEMENT: You have found the legendary sword Excalibur!\n")
#     print("You have gained 1000 gold.")
#     player.gold += 1000

def display_encounter(encounter_name):
    encounters = encounter_data["encounters"]
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
                if isinstance(choice_details["combat"], list):
                    for enemy_name in choice_details["combat"]:
                        combat_result = combat(player, Enemy(enemy_name, get_enemy_type(enemy_name)))
                        if combat_result:  # Player won the combat
                            loot(player, enemy_name)
                        else:
                            if "dmessage" in choice_details:
                                print("dmessage")
                                print("Game over! Reload your save or try again.")
                                exit()
                            else:
                                print("Game over! Reload your save or try again.")
                                exit()
                else:
                    enemy_name = choice_details["combat"]
                    combat_result = combat(player, Enemy(enemy_name, get_enemy_type(enemy_name)))
                    if not combat_result:
                        print("Game over.")
                        exit()
                    loot(player, enemy_name)

            if "shop" in choice_details:
                shop(player)

            if "job" in choice_details:
                job_board()

            if "health" in choice_details:
                player.stats.health += choice_details["health"]
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

def main():
    starting_story_1 = """
You stood before the Adventurers' Guild, heart racing with excitement. The guild, a symbol of unity in a world divided by kingdoms and races, was a beacon of hope for many. 
The heavy wooden doors creaked as you pushed them open, revealing a room bathed in warm, amber light. The air smelled of leather and firewood, and a crackling fireplace to your right cast shadows across walls lined with banners of past conquests.

To your left, a towering job board was covered in parchment quests: some humble tasks, others calling for brave souls to confront ancient threats. Scribbled across one quest was mention of "The Abyssal Horde," and another spoke of tensions brewing in the Eternal Grove of the Wildkin.

"New here, are you?" a calm, melodic voice said from behind you.

You turned to see an elf with silver hair and piercing green eyes. Her smile was warm yet guarded, carrying the wisdom of someone who had seen much of the world. 
"Welcome to the Adventurers' Guild," she said, extending a slender hand. 
"I am Elara Caelindra, your guide. And if that name sounds familiar, it’s because my family still rules in the Eternal Grove. But today, I serve all who wish to rise above the chaos."

Her voice grew softer as she studied your face. "Many come here seeking glory. But beyond these walls, there is a world on the brink of breaking. Tell me... what is your name?"\n
"""

    starting_story_2 = """
"A fine name," Elara replied, her smile widening slightly. "Follow me, and I’ll show you where your journey begins."

Elara led you through the guild, passing rows of adventurers hunched over maps and scribbled plans. As you descended a narrow stairway, the sounds of the guild faded, replaced by the clinking of metal and the hiss of sharpening stones. The armory lay ahead, a room lined with racks of swords, shields, bows, and staves, each gleaming in the warm glow of wall sconces.

"Every adventurer needs a weapon they can trust," Elara said, gesturing to the selection. 
"Whether you dream of battling demons in the Abyssal Bastion, seeking ancient relics in the Stoneforged Halls, or forging peace among the Wildkin tribes, your journey begins here."

You examined the weapons carefully, running your fingers along the edges of blades and the hafts of staves. Elara watched with a knowing expression. 
"Choose wisely," she said. "For this weapon will be more than a tool—it will be a reflection of the strength within you. Remember, the true battle lies not in the steel you wield, but in the choices you make."

Two weapons caught your eye: a sword, balanced and precise, and a lance, long and steadfast. You felt that your journey should begin with this first choice.\n
"""

    player.ring = Item("copper_ring",ItemTypeEnum.RING)
    print(starting_story_1)
    player.name = input("What is your name? ").lower().title()
    print(player)

    print(starting_story_2)

    while True:
        starting_weapon_choice = input("Do you choose the sword or the lance? ").lower()

        if starting_weapon_choice == "sword":
            print(item_data["items"]["weapons"]["iron_sword"]["description"])

            while True:
                choice = input("Do you pick up this weapon? (yes/no) ").lower()
                if choice == "yes":
                    player.weapon = Item("iron_sword", ItemTypeEnum.WEAPON)
                    print(f"You have picked up the Sword. Player's weapon: {player.weapon}")
                    exit_choice = True  # Flag to break the outer loop
                    break  # Exit the inner loop
                elif choice == "no":
                    print("You decide not to pick up the Sword. Choose again.")
                    break  # Exit the inner loop and return to weapon selection
                else:
                    print("Invalid input, please choose 'yes' or 'no'.")

            if "exit_choice" in locals() and exit_choice:
                break  # Exit the outer loop after choosing a weapon

        elif starting_weapon_choice == "lance":
            print(item_data["items"]["weapons"]["iron_lance"]["description"])

            while True:
                choice = input("Do you pick up this weapon? (yes/no) ").lower()
                if choice == "yes":
                    player.weapon = Item("iron_lance", ItemTypeEnum.WEAPON)
                    print(f"You have picked up the Lance. Player's weapon: {player.weapon}")
                    exit_choice = True  # Flag to break the outer loop
                    break  # Exit the inner loop
                elif choice == "no":
                    print("You decide not to pick up the Lance. Choose again.")
                    break  # Exit the inner loop and return to weapon selection
                else:
                    print("Invalid input, please choose 'yes' or 'no'.")

            if "exit_choice" in locals() and exit_choice:
                break  # Exit the outer loop after choosing a weapon

        else:
            print("Invalid input, please choose 'sword' or 'lance'.")

    while player.stats.health>0:
        random_event()
    print("You have died!!")
    return



main()
