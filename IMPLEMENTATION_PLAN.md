# 🐍 From Level One to Boss in Python — Curriculum Plan

Programme d'apprentissage intensif Python pour un développeur React/Node.js expérimenté (6 ans d'XP), ciblant des postes **Fullstack Python** en 3-6 mois.

## Philosophie

- **Tout en français** 🇫🇷 pour le cours, commentaires de code en anglais (convention pro)
- **Codes à trou** (fill-in-the-blank) dans chaque module pour apprendre en faisant
- **Projets thématiques** : data + jeux vidéo combinés autant que possible
- **Progression rapide** : on skip les bases JS-like, on focus sur ce qui est spécifique à Python
- Chaque module contient : cours théorique → exercices à trou → exercices complets → mini-projet

---

## Structure du Projet

```
from-level-one-to-boss-in-python/
├── README.md                          # Guide principal + roadmap
├── PROGRESSION.md                     # Tracker de progression personnel
│
├── phase-01-fondations/              # Mois 1 — Python Core
│   ├── 01-ecosysteme-et-tooling/     # Env, pip, venv, pyproject.toml
│   ├── 02-syntaxe-et-structures/     # Syntax, types, data structures
│   ├── 03-fonctions-avancees/        # Decorators, generators, closures
│   ├── 04-poo-pythonique/            # OOP, dunder methods, ABC
│   └── 05-gestion-erreurs-typing/    # Exceptions, context managers, typing
│
├── phase-02-api-et-backend/          # Mois 2 — Backend Python
│   ├── 06-modules-et-packages/       # Project structure, imports
│   ├── 07-fastapi-fondamentaux/      # REST API avec FastAPI
│   ├── 08-bases-de-donnees/          # SQLAlchemy, Alembic, migrations
│   ├── 09-auth-et-patterns/          # JWT, middleware, dependency injection
│   └── 10-testing-pytest/            # pytest, fixtures, mocking, TDD
│
├── phase-03-data-engineering/        # Mois 3 — Data & Async
│   ├── 11-pandas-numpy/             # Data manipulation
│   ├── 12-etl-pipelines/            # Extract, Transform, Load
│   ├── 13-validation-donnees/       # Pydantic, data quality
│   └── 14-async-python/             # asyncio, event loops, concurrency
│
├── phase-04-production/             # Mois 4 — Patterns avancés
│   ├── 15-message-queues/           # Redis, Celery, RabbitMQ
│   ├── 16-event-processing/         # Complex event processing, CQRS
│   ├── 17-websockets-realtime/      # WebSockets, SSE, real-time
│   └── 18-docker-deploy/            # Docker, CI/CD, monitoring
│
└── phase-05-boss-projects/          # Mois 5-6 — Projets portfolio
    ├── projet-01-game-analytics/    # Plateforme analytics pour jeux vidéo
    ├── projet-02-realtime-leaderboard/ # Leaderboard temps réel
    └── projet-03-etl-game-data/     # Pipeline ETL données de jeu
```

### Structure de chaque module

```
XX-nom-du-module/
├── README.md              # Cours théorique complet
├── exercices/
│   ├── 01_a_trou.py       # Code à trou (fill-in-the-blank)
│   ├── 02_a_trou.py       # Code à trou (suite)
│   └── 03_exercice.py     # Exercice complet guidé
├── solutions/
│   ├── 01_solution.py
│   ├── 02_solution.py
│   └── 03_solution.py
└── mini-projet/           # Mini-projet thématique (data + jeux)
    ├── README.md           # Énoncé du mini-projet
    ├── starter.py          # Code de départ
    └── solution.py         # Solution complète
```

---

## Détail des Modules

### Phase 1 — Fondations Python (Mois 1)

| Module | Thème | Mini-projet |
|--------|-------|-------------|
| 01 | Écosystème Python (venv, pip, pyproject.toml, ruff, mypy) | Setup d'un projet "Game Score Tracker" |
| 02 | Syntaxe, types, compréhensions, dicts, sets, tuples | Parser des données de scores de jeu |
| 03 | Fonctions avancées, decorators, generators, closures | Système de buffs/debuffs avec decorators |
| 04 | POO : classes, dunder, ABC, dataclasses, protocols | Modéliser un RPG (personnages, inventaire) |
| 05 | Exceptions custom, context managers, type hints avancés | Système de sauvegarde de jeu avec context managers |

### Phase 2 — API & Backend (Mois 2)

| Module | Thème | Mini-projet |
|--------|-------|-------------|
| 06 | Modules, packages, structure de projet pro | Restructurer le RPG en package Python |
| 07 | FastAPI : routes, validation, docs auto, CORS | API REST pour un catalogue de jeux vidéo |
| 08 | SQLAlchemy ORM, Alembic, relations, requêtes | BDD de jeux + scores avec relations |
| 09 | Auth JWT, middleware custom, dependency injection | Système de login pour joueurs |
| 10 | pytest, fixtures, parametrize, mocking, coverage | Tests complets du catalogue de jeux |

### Phase 3 — Data Engineering (Mois 3)

| Module | Thème | Mini-projet |
|--------|-------|-------------|
| 11 | Pandas/NumPy : Series, DataFrame, aggregations | Analyser des données de ventes de jeux vidéo |
| 12 | ETL : extraction, transformation, chargement | Pipeline ETL de données Steam/IGDB |
| 13 | Pydantic v2, validation avancée, data contracts | Valider des flux de données de jeu |
| 14 | asyncio, event loop, aiohttp, tasks, gather | Scraper async de données de jeux |

### Phase 4 — Production (Mois 4)

| Module | Thème | Mini-projet |
|--------|-------|-------------|
| 15 | Redis, Celery, task queues, workers | File d'attente de matchmaking |
| 16 | Event-driven architecture, pub/sub, CQRS | Système d'événements de jeu en temps réel |
| 17 | WebSockets avec FastAPI, SSE, broadcasting | Chat + notifications in-game |
| 18 | Docker, docker-compose, CI/CD, logging | Déployer le stack complet |

### Phase 5 — Boss Projects (Mois 5-6)

3 projets portfolio-worthy qui combinent tout :

1. **🎮 Game Analytics Platform** — FastAPI + Pandas + React dashboard
2. **🏆 Real-time Leaderboard** — WebSockets + Redis + Event processing
3. **🔄 Game Data ETL Pipeline** — Celery + Pandas + API externe

---

## Proposed Changes

### Fichiers à créer dans cette session initiale

Vu la taille du programme, je propose de créer la **Phase 1 complète** (5 modules) + le README principal + le tracker de progression.

#### [NEW] [README.md](file:///Users/amiralack/Dev/from-level-one-to-boss-in-python/README.md)
Guide principal du programme avec roadmap visuelle et instructions.

#### [NEW] [PROGRESSION.md](file:///Users/amiralack/Dev/from-level-one-to-boss-in-python/PROGRESSION.md)
Tracker de progression personnel avec checklist.

#### [NEW] Phase 1 — Modules 01 à 05
Chaque module avec : `README.md` (cours), `exercices/` (codes à trou + exercices), `solutions/`, `mini-projet/`.

> [!IMPORTANT]
> **Je créerai les phases 2-5 dans des sessions suivantes** pour garder chaque session focalisée et permettre de construire les modules suivants en intégrant ton feedback sur la phase 1.

---

## Verification Plan

### Manual Verification
1. **Structure** : Vérifier que l'arborescence de fichiers est correcte avec `find`
2. **Codes à trou** : Vérifier que les fichiers d'exercices sont exécutables (avec les trous marqués par `___`)
3. **Solutions** : Vérifier que les fichiers de solutions s'exécutent sans erreur avec `python3`
4. **Cohérence** : Relire le README et la progression pour vérifier la cohérence du parcours
