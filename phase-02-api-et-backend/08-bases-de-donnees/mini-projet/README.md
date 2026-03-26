# 🎮 Mini-Projet : API Leaderboard Multijoueur

## Objectif

Construis une **API de leaderboard complète** avec FastAPI + SQLAlchemy, déployable.

## Fonctionnalités

- CRUD Joueurs (inscription, profil, stats)
- CRUD Jeux (catalogue)
- Soumission de scores avec validation
- Leaderboards par jeu (top 100)
- Leaderboard global (meilleur score moyen)
- Stats par joueur (jeux joués, progression)
- Historique des scores avec pagination

## Stack

- FastAPI + Pydantic v2
- SQLAlchemy 2.0 (sync, avec SQLite)
- Alembic pour les migrations

## Critères de réussite ✅

- [ ] Modèles SQLAlchemy : Player, Game, Score (avec relations)
- [ ] CRUD complet sur les 3 ressources
- [ ] Leaderboard avec requête JOIN + GROUP BY + ORDER BY
- [ ] Pagination sur tous les endpoints de liste
- [ ] Validation : score <= game.max_score
- [ ] Alembic initialisé avec migration initiale
- [ ] Au moins 8 tests avec TestClient
