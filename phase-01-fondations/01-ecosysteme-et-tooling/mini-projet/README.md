# 🎮 Mini-Projet : Game Score Tracker — Version Pro

## Objectif

Crée un **vrai projet Python structuré** qui enregistre et analyse des scores de jeux vidéo. Ce mini-projet met en pratique tout ce que tu as appris dans le Module 01.

## Cahier des charges

### Fonctionnalités

1. **Enregistrer un score** : joueur, jeu, score, date
2. **Afficher le leaderboard** : top 10 par jeu
3. **Statistiques** : moyenne, meilleur, pire, nombre de parties
4. **Export** : exporter les scores en CSV
5. **Interface CLI** : utiliser `argparse` pour les commandes

### Commandes attendues

```bash
# Ajouter un score
python -m game_tracker add --player "Alice" --game "Tetris" --score 50000

# Voir le leaderboard
python -m game_tracker leaderboard --game "Tetris" --limit 10

# Voir les stats
python -m game_tracker stats --game "Tetris"

# Exporter en CSV
python -m game_tracker export --output scores.csv
```

### Structure du projet

```
mini-projet/
├── pyproject.toml
├── src/
│   └── game_tracker/
│       ├── __init__.py
│       ├── __main__.py     # Point d'entrée CLI
│       ├── models.py       # Modèles de données
│       ├── storage.py      # Lecture/écriture JSON
│       ├── stats.py        # Calculs statistiques
│       └── cli.py          # Interface argparse
├── tests/
│   └── test_storage.py
└── data/
    └── scores.json
```

## Étapes guidées

### Étape 1 : Setup le projet

1. Crée la structure de dossiers ci-dessus
2. Crée un `pyproject.toml` avec les bonnes métadonnées
3. Crée un venv et installe le projet en mode éditable

### Étape 2 : Modèles (`models.py`)

Crée une classe `ScoreEntry` qui représente un score. Utilise un simple dict ou un `dataclass` (tu verras les dataclasses au Module 04, mais tu peux déjà essayer si tu veux).

### Étape 3 : Storage (`storage.py`)

Implémente la lecture/écriture des scores en JSON. Reprends le code de l'exercice 03 et améliore-le.

### Étape 4 : Stats (`stats.py`)

Implémente les calculs statistiques. Ajoute aussi un calcul de "win streak" (séries de victoires).

### Étape 5 : CLI (`cli.py` + `__main__.py`)

Utilise `argparse` pour créer l'interface en ligne de commande.

```python
# Exemple de démarrage pour __main__.py
from game_tracker.cli import main

if __name__ == "__main__":
    main()
```

### Étape 6 : Tests

Écris au moins 3 tests avec `pytest` pour valider tes fonctions principales.

## Bonus 🌟

- Ajoute un affichage coloré avec le package `rich`
- Ajoute un graphique ASCII des scores dans le terminal
- Gère les erreurs proprement avec des messages clairs

## Critères de réussite ✅

- [ ] Le projet a la bonne structure
- [ ] `pyproject.toml` est correctement configuré
- [ ] Le CLI fonctionne avec toutes les commandes
- [ ] Les scores sont persistés en JSON
- [ ] Les stats sont correctement calculées
- [ ] Au moins 3 tests passent
- [ ] Le code est formaté avec `ruff format`
- [ ] Le code passe `ruff check` sans erreur
