# 🎮 Mini-Projet : API Catalogue de Jeux (FastAPI) + Admin Django

## Objectif

Construis deux versions d'une API de catalogue de jeux pour comparer FastAPI et Django en pratique.

## Partie 1 — FastAPI (principal)

Crée une API complète avec :

```
game-catalog-api/
├── pyproject.toml
├── src/
│   └── game_catalog/
│       ├── __init__.py
│       ├── main.py           # App FastAPI
│       ├── config.py          # Settings
│       ├── models/
│       │   ├── schemas.py     # Pydantic models
│       │   └── database.py    # Simulated DB
│       ├── routes/
│       │   ├── games.py       # CRUD jeux
│       │   ├── players.py     # CRUD joueurs
│       │   └── stats.py       # Statistiques
│       ├── services/
│       │   ├── game_service.py
│       │   └── stats_service.py
│       └── middleware/
│           ├── timing.py
│           └── logging.py
└── tests/
    └── test_games.py
```

### Endpoints requis

- `POST /games` — CRUD
- `GET /games` — Liste avec filtres, tri, pagination
- `GET /games/{id}` — Détail
- `PATCH /games/{id}` — Update partiel
- `DELETE /games/{id}`
- `GET /games/search?q=` — Full-text search
- `GET /stats/overview` — Stats globales
- `GET /stats/by-genre` — Stats par genre
- `GET /stats/price-distribution` — Distribution des prix

## Partie 2 — Django (découverte)

Crée un projet Django simple avec :
- Un modèle `Game` avec l'ORM Django
- L'admin Django configuré
- Un ViewSet DRF basique

```bash
django-admin startproject gameadmin
cd gameadmin
python manage.py startapp games
```

Le but est de voir la différence d'approche, pas de maîtriser Django.

## Critères de réussite ✅

### FastAPI
- [ ] CRUD complet avec validation Pydantic
- [ ] Filtres, tri et pagination
- [ ] Recherche full-text
- [ ] Statistiques par genre
- [ ] Dependency Injection (DB, auth)
- [ ] Middleware timing
- [ ] APIRouter pour organiser les routes
- [ ] Tests avec TestClient (au moins 10 tests)
- [ ] Documentation Swagger auto

### Django
- [ ] Modèle Game avec l'ORM
- [ ] Admin configuré avec filtres et recherche
- [ ] API basique avec DRF
- [ ] Migrations appliquées

## Bonus 🌟

- Comparaison de performance (temps de réponse FastAPI vs Django)
- Docker compose avec les deux APIs
- Frontend React qui consomme l'API FastAPI
