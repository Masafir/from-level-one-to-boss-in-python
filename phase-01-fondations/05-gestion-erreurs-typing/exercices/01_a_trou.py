"""
Module 05 — Exercice à trou #1
🎯 Thème : Exceptions et exceptions custom

Complète les ___ pour que le code fonctionne.
Exécute avec : python 01_a_trou.py
"""

# ============================================================
# PARTIE 1 : Hiérarchie d'exceptions custom
# ============================================================

class GameError(___):  # De quelle built-in hériter pour une exception custom ?
    """Base exception pour les erreurs du jeu."""
    pass


class InvalidActionError(___):  # De quelle classe de notre hiérarchie hériter ?
    """Action invalide."""
    def __init__(self, action: str, reason: str) -> None:
        self.action = action
        self.reason = reason
        super().__init__(f"Action '{action}' invalide : {reason}")


class InsufficientResourceError(GameError):
    """Ressource insuffisante."""
    def __init__(self, resource: str, required: int, available: int) -> None:
        self.resource = resource
        self.required = required
        self.available = available
        ___.__init__(  # Comment appeler le constructeur parent ?
            f"{resource} insuffisant : {available}/{required}"
        )


class CooldownError(GameError):
    """Abilité en cooldown."""
    def __init__(self, ability: str, remaining: float) -> None:
        self.ability = ability
        self.remaining = remaining
        super().__init__(f"'{ability}' en cooldown ({remaining:.1f}s)")


# ============================================================
# PARTIE 2 : Utiliser les exceptions
# ============================================================

def use_ability(player: dict, ability: dict) -> dict:
    """
    Utilise une abilité avec validation complète.
    """
    # Vérification 1 : le joueur est-il en vie ?
    if player["hp"] <= 0:
        ___ InvalidActionError(  # Quel mot-clé pour lever une exception ?
            ability["name"], 
            "joueur mort"
        )
    
    # Vérification 2 : assez de mana ?
    if player["mana"] < ability["mana_cost"]:
        raise ___(  # Quelle exception custom ?
            "mana",
            ability["mana_cost"],
            player["mana"]
        )
    
    # Vérification 3 : cooldown ?
    import time
    if "last_used" in ability:
        elapsed = time.time() - ability["last_used"]
        if elapsed < ability.get("cooldown", 0):
            remaining = ability.get("cooldown", 0) - elapsed
            raise CooldownError(ability["name"], remaining)
    
    # Tout est OK, utiliser l'abilité
    player["mana"] -= ability["mana_cost"]
    ability["last_used"] = time.time()
    
    return {
        "ability": ability["name"],
        "damage": ability["base_damage"],
        "mana_remaining": player["mana"],
    }


# Test avec try/except/else/finally
print("🎮 Test des exceptions :\n")

player = {"name": "Alice", "hp": 100, "mana": 25}
abilities = [
    {"name": "Fireball", "mana_cost": 30, "base_damage": 50, "cooldown": 2.0},
    {"name": "Slash", "mana_cost": 10, "base_damage": 25, "cooldown": 0.5},
    {"name": "Heal", "mana_cost": 20, "base_damage": 0, "cooldown": 3.0},
]

for ability in abilities:
    ___:  # Quel mot-clé pour commencer un bloc try ?
        result = use_ability(player, ability)
    except InsufficientResourceError ___ e:  # Capturer l'exception dans une variable
        print(f"  ❌ {ability['name']}: {e}")
        print(f"     Il manque {e.required - e.available} {e.resource}")
    except InvalidActionError as e:
        print(f"  ❌ {e}")
    ___ CooldownError as e:  # Quel mot-clé pour un autre catch ?
        print(f"  ⏳ {e}")
    ___:  # Quel bloc s'exécute s'il n'y a PAS d'erreur ?
        print(f"  ✅ {ability['name']} utilisé ! Dégâts: {result['damage']}")
    ___:  # Quel bloc s'exécute TOUJOURS ?
        print(f"  → Mana restant: {player['mana']}")


# ============================================================
# PARTIE 3 : Pattern EAFP
# ============================================================

def get_player_stat(player: dict, stat: str, default: int = 0) -> int:
    """
    Récupère une stat avec le pattern EAFP.
    """
    ___:
        return player[stat]
    ___ KeyError:
        return default


# Test EAFP
player_data = {"hp": 100, "attack": 30}
print(f"\nHP: {get_player_stat(player_data, 'hp')}")
print(f"Mana: {get_player_stat(player_data, 'mana', 50)}")  # Default


# ============================================================
# PARTIE 4 : Exception chaining
# ============================================================

def load_game_config(filepath: str) -> dict:
    """Charge la config du jeu avec exception chaining."""
    import json
    try:
        with open(filepath) as f:
            return json.load(f)
    except FileNotFoundError as e:
        # 'raise X from Y' : chaîne les exceptions pour garder le contexte
        raise GameError(f"Fichier de config manquant: {filepath}") ___ e
    except json.JSONDecodeError as e:
        raise GameError(f"Config invalide: {filepath}") from e

try:
    config = load_game_config("nonexistent.json")
except GameError as e:
    print(f"\n❌ {e}")
    if e.___:  # Quel attribut contient l'exception originale ?
        print(f"   Cause: {e.__cause__}")


# ============================================================
# CHECK FINAL
# ============================================================

if __name__ == "__main__":
    print("\n✅ Exercice terminé avec succès !")
