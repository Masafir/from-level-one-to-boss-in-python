# 🎮 Mini-Projet : Test Suite Complète pour le Game Catalog API

## Objectif

Reprends l'API de catalogue de jeux du Module 07 et écris une **suite de tests complète** (>80% coverage).

## Tests requis

### Unit Tests
- Validation Pydantic (noms, prix, genres)
- Logique métier (calcul de stats, recherche)
- Helpers et utilitaires

### Integration Tests
- CRUD complet (games, players)
- Filtres et pagination
- Authentification (register, login, protected routes)
- Gestion d'erreurs (404, 422, 401)

### Fixtures avancées
- `conftest.py` avec fixtures partagées
- DB fixture avec seed data
- Auth fixture (token pré-généré)
- Fixtures paramétriques

## Critères de réussite ✅

- [ ] Au moins 25 tests
- [ ] Coverage > 80% (`pytest --cov`)
- [ ] Utilisation de `@pytest.mark.parametrize`
- [ ] Mocking pour les services externes
- [ ] `conftest.py` avec fixtures réutilisables
- [ ] Dependency override pour la DB
- [ ] Tests groupés en classes logiques
- [ ] Tous les tests passent en < 5s
