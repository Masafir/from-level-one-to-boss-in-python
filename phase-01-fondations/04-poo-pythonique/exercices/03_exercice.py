"""
Module 04 — Exercice complet #3
🎯 Thème : Modéliser un RPG complet avec la POO Python

Objectif : Créer un mini-RPG avec personnages, inventaire et combat.

Exécute avec : python 03_exercice.py
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


# ============================================================
# PARTIE 1 : Enums et Dataclasses pour le système de base
# ============================================================

class Element(Enum):
    """
    TODO: Définis les éléments du jeu.
    FIRE, WATER, EARTH, AIR, NEUTRAL
    
    Hints:
    - class Element(Enum):
    -     FIRE = "fire"
    """
    pass


@dataclass
class Stats:
    """
    TODO: Crée une dataclass pour les stats.
    Attributs : hp, max_hp, attack, defense, speed, mana, max_mana
    Tous des int avec des valeurs par défaut raisonnables.
    
    Ajoute :
    - @property power_level qui calcule la puissance totale
    - __add__ pour combiner deux Stats
    """
    pass


@dataclass
class Skill:
    """
    TODO: Crée une dataclass pour les compétences.
    Attributs : name, element (Element), mana_cost (int), 
                base_damage (int), description (str)
    
    Ajoute :
    - __str__ qui affiche le nom avec l'emoji de l'élément
    """
    pass


# ============================================================
# PARTIE 2 : Système d'inventaire
# ============================================================

@dataclass
class Item:
    """
    TODO: Crée une dataclass pour les items.
    Attributs : name, item_type (str: "weapon"/"armor"/"consumable"),
                value (int), stats_bonus (Stats, optional),
                quantity (int, default 1)
    """
    pass


class Inventory:
    """
    TODO: Crée un inventaire complet.
    
    Méthodes :
    - add(item) : ajouter un item (stack si même nom)
    - remove(item_name) : retirer un item
    - get(item_name) -> Item | None
    - __len__ : nombre d'items uniques
    - __contains__ : vérifier si un item est présent par nom
    - __iter__ : itérer sur les items
    - __getitem__ : accès par index
    - __str__ : affichage formaté
    - total_weight : property calculée
    """
    pass


# ============================================================
# PARTIE 3 : Personnages avec ABC
# ============================================================

class Character(ABC):
    """
    TODO: Classe abstraite Character.
    
    Attributs : name, stats, skills (list), inventory, element
    
    Méthodes concrètes :
    - is_alive -> bool (property)
    - take_damage(amount) -> int (retourne les dégâts réels après défense)
    - heal(amount) -> int (retourne les HP récupérés)
    - use_skill(skill_index, target) -> dict with result
    
    Méthodes abstraites :
    - special_ability() -> dict
    - level_up() -> None
    
    Dunder methods :
    - __str__, __repr__
    - __lt__ (comparer par power_level)
    """
    pass


class Warrior(Character):
    """
    TODO: Classe Warrior qui hérite de Character.
    
    - special_ability : "Rage" — double l'attaque pour 3 tours
    - level_up : +20 HP, +5 attack, +3 defense
    - Élément par défaut : EARTH
    """
    pass


class Mage(Character):
    """
    TODO: Classe Mage qui hérite de Character.
    
    - special_ability : "Arcane Shield" — double la défense pour 2 tours
    - level_up : +10 HP, +2 attack, +15 mana
    - Élément par défaut : AIR
    """
    pass


# ============================================================
# PARTIE 4 : Système de combat
# ============================================================

class BattleSystem:
    """
    TODO: Crée un système de combat tour par tour.
    
    Méthodes :
    - __init__(challenger, opponent) : initialise le combat
    - calculate_damage(attacker, skill, defender) -> int
    - execute_turn(active, passive) -> dict (résultat du tour)
    - battle() -> Character (le gagnant)
    
    Logique de dégâts :
    - base_damage = skill.base_damage + attacker.stats.attack
    - defense_reduction = defender.stats.defense * 0.5
    - element_bonus = 1.5 si avantage élémentaire, 0.75 si désavantage, 1.0 sinon
    - final_damage = max(1, (base_damage - defense_reduction) * element_bonus)
    
    Avantages élémentaires :
    - FIRE > EARTH > AIR > WATER > FIRE
    """
    pass


# ============================================================
# MAIN — Tests
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("⚔️ MINI RPG — Tests")
    print("=" * 50)
    
    # Ces tests devraient fonctionner une fois tes classes implémentées
    
    # Test 1 : Stats
    print("\n--- Stats ---")
    # stats = Stats(hp=100, max_hp=100, attack=30, defense=20, speed=15, mana=50, max_mana=50)
    # print(stats)
    # print(f"Power: {stats.power_level}")
    
    # Test 2 : Skills
    print("\n--- Skills ---")
    # fireball = Skill("Fireball", Element.FIRE, 20, 45, "A ball of fire")
    # print(fireball)
    
    # Test 3 : Characters
    print("\n--- Characters ---")
    # warrior = Warrior("Conan", Stats(...))
    # mage = Mage("Gandalf", Stats(...))
    # print(warrior)
    # print(mage)
    
    # Test 4 : Combat
    print("\n--- Battle ---")
    # battle = BattleSystem(warrior, mage)
    # winner = battle.battle()
    # print(f"\n🏆 Winner: {winner.name}")
    
    print("\n✅ Tests terminés !")
