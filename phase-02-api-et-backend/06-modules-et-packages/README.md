# Module 06 — Modules, Packages & Structure de Projet 📦

> **Objectif** : Structurer un projet Python comme un pro. En Node tu as `require`/`import`, `package.json` et `node_modules`. En Python, le système est différent — et le maîtriser c'est essentiel.

## 1. Le système d'import Python

### Import basique

```python
# === Import un module entier ===
import json
data = json.loads('{"hp": 100}')

# === Import spécifique (comme le destructuring en JS) ===
from json import loads, dumps
data = loads('{"hp": 100}')

# === Import avec alias ===
import numpy as np  # Convention commune
from pathlib import Path as P

# === Import tout (ÉVITE ÇA en prod, comme import * en JS) ===
from json import *  # ❌ Pollue le namespace
```

### Parallèle avec Node.js

```javascript
// Node.js
const json = require('json');           // → import json
const { loads } = require('json');      // → from json import loads
const np = require('numpy');            // → import numpy as np
```

## 2. Modules vs Packages

```
# MODULE = un fichier .py
game_utils.py          # C'est un module

# PACKAGE = un dossier avec __init__.py
game_engine/           # C'est un package
├── __init__.py        # Obligatoire (marque le dossier comme package)
├── player.py          # Module dans le package
├── enemies.py
└── items/             # Sous-package
    ├── __init__.py
    └── weapons.py
```

### Le fichier `__init__.py`

```python
# game_engine/__init__.py
"""Game Engine — Moteur de jeu RPG."""

# Définit ce qui est accessible avec "from game_engine import ..."
from game_engine.player import Player
from game_engine.enemies import Enemy

# __all__ contrôle ce qui est exporté avec "from package import *"
__all__ = ["Player", "Enemy"]

# C'est comme le index.js qui re-exporte :
# export { Player } from './player';
# export { Enemy } from './enemies';
```

### Types d'imports

```python
# === Import absolu (recommandé) ===
from game_engine.player import Player
from game_engine.items.weapons import Sword

# === Import relatif (dans un package) ===
# Dans game_engine/enemies.py :
from .player import Player       # . = même package
from .items.weapons import Sword # .items = sous-package
from ..utils import helpers      # .. = package parent (à éviter)
```

> 💡 **Règle d'or** : Utilise les imports absolus sauf dans les `__init__.py` des packages où les imports relatifs sont OK.

## 3. Le `PYTHONPATH` et la résolution des imports

```python
# Python cherche les modules dans cet ordre :
# 1. Le dossier du script exécuté
# 2. Les dossiers dans PYTHONPATH (variable d'environnement)
# 3. Les dossiers d'installation (site-packages = node_modules)
# 4. Les dossiers de la lib standard

import sys
print(sys.path)  # Liste tous les chemins de recherche
```

### Le problème du "module not found"

```bash
# ❌ Erreur classique : ModuleNotFoundError
python src/game_engine/player.py
# → ImportError: No module named 'game_engine'

# ✅ Solution 1 : Exécuter comme un module
python -m game_engine.player

# ✅ Solution 2 : Installer en mode éditable
pip install -e .  # Avec un pyproject.toml correct

# ✅ Solution 3 : Ajouter au PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:src"
```

## 4. Structure de projet professionnelle

### Layout "src"  (recommandé)

```
my-project/
├── pyproject.toml
├── README.md
├── .gitignore
├── src/                          # ← Tout le code source ici
│   └── game_engine/              # ← Le package principal
│       ├── __init__.py
│       ├── __main__.py           # python -m game_engine
│       ├── config.py             # Configuration
│       ├── models/               # Modèles de données
│       │   ├── __init__.py
│       │   ├── player.py
│       │   └── item.py
│       ├── services/             # Logique métier
│       │   ├── __init__.py
│       │   ├── combat.py
│       │   └── inventory.py
│       ├── api/                  # Routes API (si applicable)
│       │   ├── __init__.py
│       │   └── routes.py
│       └── utils/                # Utilitaires
│           ├── __init__.py
│           └── helpers.py
├── tests/                        # Tests (hors de src/)
│   ├── __init__.py
│   ├── conftest.py               # Fixtures partagées pytest
│   ├── test_player.py
│   └── test_combat.py
├── scripts/                      # Scripts utilitaires
│   └── seed_data.py
└── docs/
    └── api.md
```

### Le `pyproject.toml` pour le layout src

```toml
[project]
name = "game-engine"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "rich>=13.0",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "ruff>=0.3", "mypy>=1.8"]

[project.scripts]
game = "game_engine.cli:main"   # Crée une commande 'game'

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/game_engine"]   # Dit à hatch où trouver le package
```

### Le fichier `__main__.py`

```python
# src/game_engine/__main__.py
"""Point d'entrée quand on fait : python -m game_engine"""

from game_engine.cli import main

if __name__ == "__main__":
    main()
```

## 5. Patterns d'organisation avancés

### Le pattern "Service Layer"

```python
# Séparer la logique métier des modèles et de l'API
# Comme dans Express.js : routes → controllers → services → models

# models/player.py — Données pures
@dataclass
class Player:
    name: str
    hp: int
    inventory: list[str]

# services/player_service.py — Logique métier
class PlayerService:
    def __init__(self, repository: PlayerRepository):
        self.repo = repository
    
    def take_damage(self, player_id: int, amount: int) -> Player:
        player = self.repo.get(player_id)
        player.hp = max(0, player.hp - amount)
        self.repo.save(player)
        return player

# api/routes.py — Routes HTTP (FastAPI)
@router.post("/players/{id}/damage")
def damage_player(id: int, amount: int):
    return player_service.take_damage(id, amount)
```

### Le pattern "Configuration"

```python
# config.py
from dataclasses import dataclass, field
from pathlib import Path
import os

@dataclass
class Config:
    """Configuration centralisée (comme .env + config en JS)."""
    
    database_url: str = "sqlite:///game.db"
    debug: bool = False
    secret_key: str = "change-me"
    max_players: int = 100
    
    @classmethod
    def from_env(cls) -> "Config":
        """Charge depuis les variables d'environnement."""
        return cls(
            database_url=os.getenv("DATABASE_URL", "sqlite:///game.db"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            secret_key=os.getenv("SECRET_KEY", "change-me"),
            max_players=int(os.getenv("MAX_PLAYERS", "100")),
        )

# Utilisation
config = Config.from_env()
```

### Le pattern "Registry" / "Plugin"

```python
# Enregistrer des composants dynamiquement (comme les middlewares Express)

class EntityRegistry:
    """Registre d'entités — pattern très courant en Python."""
    
    _registry: dict[str, type] = {}
    
    @classmethod
    def register(cls, name: str):
        """Decorator pour enregistrer une entité."""
        def decorator(entity_class):
            cls._registry[name] = entity_class
            return entity_class
        return decorator
    
    @classmethod
    def create(cls, name: str, **kwargs):
        """Factory — crée une entité par son nom."""
        if name not in cls._registry:
            raise KeyError(f"Entité inconnue : {name}")
        return cls._registry[name](**kwargs)

@EntityRegistry.register("goblin")
class Goblin:
    def __init__(self, level: int = 1):
        self.level = level

@EntityRegistry.register("dragon")  
class Dragon:
    def __init__(self, level: int = 10):
        self.level = level

# Factory usage
enemy = EntityRegistry.create("goblin", level=5)
```

## 6. Dependency Injection (DI) simple

```python
# En JS/TS tu utilises NestJS ou inversify pour la DI.
# En Python, on peut faire simple avec des constructeurs.

# ❌ Couplé (dur à tester)
class GameService:
    def __init__(self):
        self.db = Database("prod_connection")  # Hardcodé !

# ✅ Injection de dépendances (facile à tester)
class GameService:
    def __init__(self, db: Database):
        self.db = db  # On reçoit la dépendance

# En prod
service = GameService(db=Database("prod_connection"))

# En test
service = GameService(db=MockDatabase())
```

---

## 🎯 Résumé

| Concept | Ce qu'il faut retenir |
|---------|----------------------|
| **Module** | Un fichier `.py` |
| **Package** | Un dossier avec `__init__.py` |
| **Import absolu** | `from package.module import X` (préféré) |
| **Import relatif** | `from .module import X` (pour `__init__.py`) |
| **`__init__.py`** | Définit l'API publique du package |
| **`__main__.py`** | Point d'entrée pour `python -m package` |
| **Layout src** | `src/package/` + `tests/` + `pyproject.toml` |
| **`pip install -e .`** | Installe en mode dev (résout les imports) |

---

➡️ **Maintenant, passe aux exercices dans `exercices/` !**
