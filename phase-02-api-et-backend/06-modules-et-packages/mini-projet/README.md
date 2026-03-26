# 🎮 Mini-Projet : Restructurer le RPG en package Python

## Objectif

Prends le code du mini-projet du Module 04 (RPG Engine) et restructure-le en un **vrai package Python** installable avec `pip install -e .`.

## Résultat attendu

```
rpg-engine/
├── pyproject.toml
├── README.md
├── src/
│   └── rpg_engine/
│       ├── __init__.py
│       ├── __main__.py
│       ├── config.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── stats.py
│       │   ├── item.py
│       │   ├── player.py
│       │   └── enemy.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── combat.py
│       │   ├── inventory.py
│       │   └── persistence.py
│       └── cli.py
├── tests/
│   ├── conftest.py
│   ├── test_combat.py
│   └── test_inventory.py
└── .gitignore
```

## Critères de réussite ✅

- [ ] `pip install -e .` fonctionne
- [ ] `python -m rpg_engine` lance le jeu
- [ ] `rpg-engine` (CLI) lance le jeu
- [ ] Les imports absolus sont utilisés partout
- [ ] Chaque `__init__.py` re-exporte les classes publiques
- [ ] `ruff check .` passe sans erreur
- [ ] Les tests passent avec `pytest`
