"""Module 05 — Solution exercice à trou #1"""

import time


class GameError(Exception):
    pass


class InvalidActionError(GameError):
    def __init__(self, action: str, reason: str) -> None:
        self.action = action
        self.reason = reason
        super().__init__(f"Action '{action}' invalide : {reason}")


class InsufficientResourceError(GameError):
    def __init__(self, resource: str, required: int, available: int) -> None:
        self.resource = resource
        self.required = required
        self.available = available
        super().__init__(f"{resource} insuffisant : {available}/{required}")


class CooldownError(GameError):
    def __init__(self, ability: str, remaining: float) -> None:
        self.ability = ability
        self.remaining = remaining
        super().__init__(f"'{ability}' en cooldown ({remaining:.1f}s)")


def use_ability(player: dict, ability: dict) -> dict:
    if player["hp"] <= 0:
        raise InvalidActionError(ability["name"], "joueur mort")
    if player["mana"] < ability["mana_cost"]:
        raise InsufficientResourceError("mana", ability["mana_cost"], player["mana"])

    if "last_used" in ability:
        elapsed = time.time() - ability["last_used"]
        if elapsed < ability.get("cooldown", 0):
            remaining = ability.get("cooldown", 0) - elapsed
            raise CooldownError(ability["name"], remaining)

    player["mana"] -= ability["mana_cost"]
    ability["last_used"] = time.time()
    return {
        "ability": ability["name"],
        "damage": ability["base_damage"],
        "mana_remaining": player["mana"],
    }


print("🎮 Test des exceptions :\n")

player = {"name": "Alice", "hp": 100, "mana": 25}
abilities = [
    {"name": "Fireball", "mana_cost": 30, "base_damage": 50, "cooldown": 2.0},
    {"name": "Slash", "mana_cost": 10, "base_damage": 25, "cooldown": 0.5},
    {"name": "Heal", "mana_cost": 20, "base_damage": 0, "cooldown": 3.0},
]

for ability in abilities:
    try:
        result = use_ability(player, ability)
    except InsufficientResourceError as e:
        print(f"  ❌ {ability['name']}: {e}")
        print(f"     Il manque {e.required - e.available} {e.resource}")
    except InvalidActionError as e:
        print(f"  ❌ {e}")
    except CooldownError as e:
        print(f"  ⏳ {e}")
    else:
        print(f"  ✅ {ability['name']} utilisé ! Dégâts: {result['damage']}")
    finally:
        print(f"  → Mana restant: {player['mana']}")


def get_player_stat(player: dict, stat: str, default: int = 0) -> int:
    try:
        return player[stat]
    except KeyError:
        return default


player_data = {"hp": 100, "attack": 30}
print(f"\nHP: {get_player_stat(player_data, 'hp')}")
print(f"Mana: {get_player_stat(player_data, 'mana', 50)}")

import json

def load_game_config(filepath: str) -> dict:
    try:
        with open(filepath) as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise GameError(f"Fichier de config manquant: {filepath}") from e
    except json.JSONDecodeError as e:
        raise GameError(f"Config invalide: {filepath}") from e

try:
    config = load_game_config("nonexistent.json")
except GameError as e:
    print(f"\n❌ {e}")
    if e.__cause__:
        print(f"   Cause: {e.__cause__}")

print("\n✅ Exercice terminé avec succès !")
