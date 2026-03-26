"""
Module 06 — Exercice complet #3
🎯 Thème : Restructurer un RPG en package Python professionnel

Tu as un "monolithe" de RPG (tout dans un seul fichier).
Ton job est de le restructurer en un package propre.

Cet exercice est conceptuel : tu vas créer les fichiers d'un package
et vérifier que la structure est correcte.

Exécute avec : python 03_exercice.py
"""

import tempfile
from pathlib import Path


# ============================================================
# LE MONOLITHE — Tout dans un seul fichier (le AVANT)
# ============================================================

MONOLITH_CODE = '''
import json
import random
from dataclasses import dataclass

# --- Models ---
@dataclass
class Stats:
    hp: int = 100
    attack: int = 10
    defense: int = 10

@dataclass  
class Item:
    name: str
    value: int
    item_type: str  # weapon, armor, potion

class Player:
    def __init__(self, name, stats=None):
        self.name = name
        self.stats = stats or Stats()
        self.inventory = []
    
    def take_damage(self, amount):
        actual = max(0, amount - self.stats.defense)
        self.stats.hp -= actual
        return actual

class Enemy:
    def __init__(self, name, stats=None, xp=10):
        self.name = name
        self.stats = stats or Stats(hp=30, attack=5, defense=3)
        self.xp = xp

# --- Services ---
def calculate_damage(attacker_stats, defender_stats):
    base = attacker_stats.attack
    reduction = defender_stats.defense * 0.5
    return max(1, int(base - reduction))

def battle(player, enemy):
    while player.stats.hp > 0 and enemy.stats.hp > 0:
        dmg = calculate_damage(player.stats, enemy.stats)
        enemy.stats.hp -= dmg
        if enemy.stats.hp <= 0:
            return "player_wins"
        dmg = calculate_damage(enemy.stats, player.stats)
        player.take_damage(dmg)
    return "enemy_wins"

def save_game(player, filepath):
    data = {"name": player.name, "hp": player.stats.hp}
    with open(filepath, "w") as f:
        json.dump(data, f)

def load_game(filepath):
    with open(filepath) as f:
        return json.load(f)
'''


# ============================================================
# TON TRAVAIL : Restructurer en package
# ============================================================

def create_package_structure(base_dir: Path) -> dict[str, str]:
    """
    TODO: Crée la structure de fichiers pour le package restructuré.
    
    Structure attendue :
    base_dir/
    ├── pyproject.toml
    ├── src/
    │   └── rpg_engine/
    │       ├── __init__.py          # Exports publics
    │       ├── __main__.py          # python -m rpg_engine
    │       ├── models/
    │       │   ├── __init__.py      # Re-export Stats, Item, Player, Enemy
    │       │   ├── stats.py         # Stats dataclass
    │       │   ├── item.py          # Item dataclass
    │       │   ├── player.py        # Player class (importe Stats, Item)
    │       │   └── enemy.py         # Enemy class (importe Stats)
    │       ├── services/
    │       │   ├── __init__.py      # Re-export services
    │       │   ├── combat.py        # calculate_damage, battle
    │       │   └── persistence.py   # save_game, load_game
    │       └── config.py            # Configuration
    └── tests/
        ├── __init__.py
        └── test_combat.py
    
    Retourne un dict {filepath_relative: file_content}
    
    IMPORTANT:
    - Les imports doivent être corrects (absolus depuis rpg_engine)
    - Chaque __init__.py doit re-exporter les classes importantes
    - Le pyproject.toml doit être valide
    - Le __main__.py doit avoir un point d'entrée fonctionnel
    
    Hints:
    - models/stats.py ne dépend de rien d'autre
    - models/item.py ne dépend de rien d'autre
    - models/player.py dépend de stats et item
    - models/enemy.py dépend de stats
    - services/combat.py dépend de models
    - services/persistence.py dépend de models
    """
    pass  # Remplace par ton implémentation


def validate_structure(base_dir: Path) -> list[str]:
    """
    TODO: Valide que la structure du package est correcte.
    
    Vérifie :
    1. Tous les fichiers requis existent
    2. Tous les __init__.py existent
    3. pyproject.toml contient les bonnes clés
    4. Les imports dans chaque fichier sont corrects (pas de "import *")
    
    Retourne une liste d'erreurs (vide si tout est OK).
    """
    pass  # Remplace par ton implémentation


def generate_dependency_report(base_dir: Path) -> str:
    """
    TODO: Génère un rapport des dépendances entre modules.
    
    Analyse les fichiers .py et extrait les imports pour créer
    un rapport de dépendances :
    
    📦 RPG Engine — Dependency Report
    ═══════════════════════════════════
    models/stats.py      → (aucune dépendance)
    models/item.py       → (aucune dépendance)
    models/player.py     → models.stats, models.item
    models/enemy.py      → models.stats
    services/combat.py   → models.player, models.enemy
    services/persistence.py → models.player
    
    Hint: utilise l'exercice 01 (analyze_imports) comme base
    """
    pass  # Remplace par ton implémentation


# ============================================================
# MAIN — Tests
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("📦 RESTRUCTURATION RPG — Tests")
    print("=" * 50)
    
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        
        # Test 1 : Créer la structure
        print("\n--- Création de la structure ---")
        files = create_package_structure(base)
        if files:
            for filepath, content in sorted(files.items()):
                full_path = base / filepath
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content)
                print(f"  📄 {filepath}")
        
        # Test 2 : Valider
        print("\n--- Validation ---")
        errors = validate_structure(base)
        if errors is not None:
            if errors:
                for err in errors:
                    print(f"  ❌ {err}")
            else:
                print("  ✅ Structure valide !")
        
        # Test 3 : Rapport
        print("\n--- Rapport de dépendances ---")
        report = generate_dependency_report(base)
        if report:
            print(report)
    
    print("\n✅ Tests terminés !")
