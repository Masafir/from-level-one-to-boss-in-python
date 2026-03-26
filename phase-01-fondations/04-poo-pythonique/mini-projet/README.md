# 🎮 Mini-Projet : RPG Engine — Personnages, Inventaire & Combat

## Objectif

Crée un **moteur RPG complet** en Python avec le système OOP appris. Ce projet doit être structuré comme un vrai package Python.

## Cahier des charges

### Système de personnages

```python
@dataclass
class Stats:
    hp: int = 100
    max_hp: int = 100
    attack: int = 10
    defense: int = 10
    speed: int = 10
    mana: int = 50
    max_mana: int = 50

class Character(ABC):
    # Classe abstraite avec stats, inventaire, skills, element

class Warrior(Character):
    # Spécialisation tank/DPS, compétences physiques

class Mage(Character):
    # Spécialisation mana/sorts, compétences magiques

class Rogue(Character):
    # Spécialisation vitesse/crits, compétences furtives
```

### Système d'inventaire

- Items empilables (potions x5), non-empilables (armes)
- Équipement avec slots (weapon, armor, helmet, boots, accessory)
- Bonus de stats appliqués dynamiquement via `@property`
- Limite de poids basée sur les stats du personnage

### Système de combat

- Tour par tour basé sur la vitesse
- Éléments avec avantages/désavantages (triangle)
- Compétences avec coût en mana
- Coups critiques (basés sur la vitesse)
- Système de XP et level up

### Sauvegarde/Chargement

- Sérialiser l'état du jeu en JSON
- Charger depuis un fichier JSON
- Utiliser des dataclasses pour faciliter la (dé)sérialisation

## Structure attendue

```
mini-projet/
├── rpg/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── stats.py        # Stats dataclass
│   │   ├── item.py          # Item, Equipment dataclasses
│   │   └── skill.py         # Skill dataclass
│   ├── characters/
│   │   ├── __init__.py
│   │   ├── base.py          # Character ABC
│   │   ├── warrior.py
│   │   ├── mage.py
│   │   └── rogue.py
│   ├── systems/
│   │   ├── __init__.py
│   │   ├── inventory.py     # Inventory class
│   │   ├── combat.py        # BattleSystem
│   │   └── save.py          # Save/Load
│   └── game.py              # Game loop
└── main.py                   # Point d'entrée
```

## Critères de réussite ✅

- [ ] Au moins 3 classes de personnages
- [ ] Système de stats avec dataclasses
- [ ] Inventaire itérable et indexable (dunder methods)
- [ ] Système d'équipement avec bonus dynamiques
- [ ] Combat tour par tour fonctionnel
- [ ] Utilisation d'ABC pour les classes abstraites
- [ ] Utilisation de Protocols pour le duck typing
- [ ] Sauvegarde/chargement JSON
- [ ] Code typé (type hints partout)

## Bonus 🌟

- Système de quêtes
- Boutique pour acheter/vendre des items
- Ennemis générés procéduralement
- Système d'enchantements sur les armes
