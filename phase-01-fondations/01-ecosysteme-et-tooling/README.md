# Module 01 — Écosystème Python & Tooling 🛠️

> **Objectif** : Maîtriser l'environnement Python comme un pro. Quand tu sais setup un projet Python aux petits oignons, t'as déjà 20% du taf de fait.

## 🔄 Parallèle avec Node.js

Toi qui viens de Node, voici les équivalences :

| Node.js | Python | Rôle |
|---------|--------|------|
| `node` | `python3` | Runtime |
| `npm` / `yarn` | `pip` | Package manager |
| `package.json` | `pyproject.toml` | Config projet |
| `node_modules/` | `venv/` (ou `.venv/`) | Dépendances locales |
| `npx` | `pipx` | Exécuter des CLI tools |
| `nvm` | `pyenv` | Gérer les versions |
| `eslint` / `prettier` | `ruff` | Linter + formatter |
| TypeScript | `mypy` + type hints | Typage statique |
| `.nvmrc` | `.python-version` | Version lock |

## 1. Python : le runtime

### Installation

```bash
# macOS — avec Homebrew (recommandé)
brew install python@3.12

# Vérifier
python3 --version   # Python 3.12.x
which python3       # /opt/homebrew/bin/python3
```

### L'interpréteur interactif (REPL)

```python
# Lance le REPL
python3

>>> 2 + 2
4
>>> "hello" * 3
'hellohellohello'
>>> exit()
```

> 💡 **Tip** : Utilise `ipython` pour un REPL boosté (autocomplétion, couleurs...) :
> ```bash
> pip install ipython
> ipython
> ```

## 2. Environnements virtuels (venv)

### Pourquoi ?

En Node, chaque projet a son `node_modules/`. En Python, sans venv, **tous les packages s'installent globalement**. C'est le chaos assuré. Le `venv` isole les dépendances par projet.

### Créer et activer un venv

```bash
# Créer un venv (convention : .venv dans le projet)
python3 -m venv .venv

# Activer le venv
source .venv/bin/activate    # macOS / Linux

# Ton prompt change :
(.venv) $ python --version   # Plus besoin de python3 !
(.venv) $ which python        # Pointe vers .venv/bin/python

# Désactiver
deactivate
```

### ⚠️ Règle d'or

**TOUJOURS** travailler dans un venv. Point final. Ajoute `.venv/` dans ton `.gitignore`.

```gitignore
# .gitignore
.venv/
__pycache__/
*.pyc
.mypy_cache/
.ruff_cache/
```

## 3. pip — Le package manager

```bash
# Installer un package
pip install requests

# Installer une version spécifique
pip install requests==2.31.0

# Lister les packages installés
pip list

# Geler les dépendances (comme npm freeze)
pip freeze > requirements.txt

# Installer depuis un fichier requirements
pip install -r requirements.txt

# Désinstaller
pip uninstall requests
```

### requirements.txt vs package.json

```text
# requirements.txt — équivalent de package.json (mais plus basique)
requests==2.31.0
fastapi>=0.100.0,<1.0.0
pandas~=2.1.0
```

| Notation | Signification |
|----------|--------------|
| `==2.31.0` | Version exacte (comme `"2.31.0"` dans package.json) |
| `>=2.0,<3.0` | Range (comme `"^2.0.0"`) |
| `~=2.1.0` | Compatible (comme `"~2.1.0"`) |

## 4. pyproject.toml — Le vrai package.json de Python

`requirements.txt` c'est le passé. En 2024+, on utilise `pyproject.toml` :

```toml
[project]
name = "game-score-tracker"
version = "0.1.0"
description = "Track and analyze game scores"
requires-python = ">=3.12"
dependencies = [
    "requests>=2.31.0",
    "rich>=13.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.3.0",
    "mypy>=1.8.0",
]

[project.scripts]
tracker = "game_score_tracker.cli:main"

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.12"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### Installer un projet avec pyproject.toml

```bash
# Installer le projet + dépendances
pip install -e .          # -e = mode éditable (comme npm link)

# Installer avec les deps de dev
pip install -e ".[dev]"
```

## 5. Ruff — Linter + Formatter (le ESLint + Prettier de Python)

Ruff c'est le game changer. Ultra rapide (écrit en Rust), il remplace `flake8`, `isort`, `black` en un seul outil.

```bash
pip install ruff

# Linter (check les erreurs)
ruff check .

# Formatter (comme prettier)
ruff format .

# Fix automatique
ruff check --fix .
```

### Configurer dans pyproject.toml

```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort (import sorting)
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
]
```

## 6. mypy — Le TypeScript de Python

Python est dynamiquement typé, mais avec les **type hints** + **mypy**, tu retrouves le confort de TypeScript.

```python
# Sans type hints (ça marche, mais c'est flou)
def calculate_damage(base, multiplier):
    return base * multiplier

# Avec type hints (c'est clair, et mypy vérifie)
def calculate_damage(base: int, multiplier: float) -> float:
    return base * multiplier
```

```bash
pip install mypy

# Vérifier les types
mypy src/
```

## 7. Structure d'un projet Python pro

```
game-score-tracker/
├── pyproject.toml          # Config projet
├── README.md
├── .gitignore
├── .python-version         # Version Python (pour pyenv)
├── src/
│   └── game_score_tracker/ # Le package principal
│       ├── __init__.py     # Marque le dossier comme package
│       ├── models.py       # Modèles de données
│       ├── tracker.py      # Logique principale
│       └── cli.py          # Interface CLI
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   └── test_tracker.py
└── .venv/                  # Ignoré par git
```

### Le fichier `__init__.py`

```python
# src/game_score_tracker/__init__.py
"""Game Score Tracker — Track and analyze your gaming sessions."""

__version__ = "0.1.0"
```

> 💡 En Node, chaque fichier est un module automatiquement. En Python, `__init__.py` transforme un dossier en **package** importable. Depuis Python 3.3, ce fichier est optionnel pour les "namespace packages", mais c'est une **bonne pratique** de toujours l'inclure.

## 8. pyenv — Gérer les versions Python (comme nvm)

```bash
# Installer pyenv
brew install pyenv

# Lister les versions dispo
pyenv install --list | grep "3.12"

# Installer une version
pyenv install 3.12.2

# Définir la version pour un projet
cd mon-projet/
pyenv local 3.12.2    # Crée .python-version

# Définir la version globale
pyenv global 3.12.2
```

## 9. Commandes essentielles — Cheat Sheet

```bash
# === SETUP ===
python3 -m venv .venv          # Créer un venv
source .venv/bin/activate      # Activer
pip install -e ".[dev]"        # Installer le projet

# === DEV ===
python src/main.py             # Exécuter un script
python -m game_score_tracker   # Exécuter un package
python -c "print('hello')"    # One-liner

# === QUALITÉ ===
ruff check .                   # Linter
ruff format .                  # Formatter
mypy src/                      # Type checker
pytest                         # Tests

# === DEBUG ===
python -i script.py            # Exécuter puis ouvrir le REPL
python -m pdb script.py        # Debugger intégré
```

---

## 🎯 Résumé

| Concept | Ce qu'il faut retenir |
|---------|----------------------|
| **venv** | TOUJOURS travailler dans un venv. Toujours. |
| **pyproject.toml** | Le vrai fichier de config moderne (pas requirements.txt) |
| **ruff** | Linter + formatter en un seul outil. Configure-le d'entrée. |
| **mypy** | Type checker. Utilise les type hints dès le début. |
| **structure** | `src/package_name/` + `tests/` + `pyproject.toml` |

---

➡️ **Maintenant, passe aux exercices dans `exercices/` !**
