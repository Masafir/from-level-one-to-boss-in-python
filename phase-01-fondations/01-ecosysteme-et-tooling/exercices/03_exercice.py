"""
Module 01 — Exercice complet #3
🎯 Thème : Créer un CLI "Game Score Tracker"

Objectif : Créer un petit outil CLI qui :
1. Enregistre des scores de jeu dans un fichier JSON
2. Affiche les meilleurs scores
3. Calcule des statistiques

Tu dois implémenter TOUTES les fonctions marquées TODO.
Exécute avec : python 03_exercice.py
"""

import json
from datetime import datetime
from pathlib import Path


# Le fichier où on stocke les scores
SCORES_FILE = Path(__file__).parent / "scores.json"


def load_scores() -> list[dict]:
    """
    Charge les scores depuis le fichier JSON.
    Si le fichier n'existe pas, retourne une liste vide.
    
    TODO: Implémente cette fonction.
    
    Hints:
    - Utilise SCORES_FILE.exists() pour vérifier si le fichier existe
    - Utilise json.loads() pour parser du JSON
    - Utilise Path.read_text() pour lire le contenu
    """
    pass  # Remplace par ton code


def save_scores(scores: list[dict]) -> None:
    """
    Sauvegarde les scores dans le fichier JSON.
    
    TODO: Implémente cette fonction.
    
    Hints:
    - Utilise json.dumps() avec indent=2 pour un joli format
    - Utilise Path.write_text() pour écrire
    """
    pass  # Remplace par ton code


def add_score(player: str, game: str, score: int) -> dict:
    """
    Ajoute un nouveau score.
    
    TODO: Implémente cette fonction.
    
    Doit:
    1. Charger les scores existants
    2. Créer un nouveau dict avec : player, game, score, timestamp (ISO format)
    3. Ajouter à la liste
    4. Sauvegarder
    5. Retourner le nouveau score entry
    
    Hints:
    - datetime.now().isoformat() pour le timestamp
    """
    pass  # Remplace par ton code


def get_top_scores(game: str | None = None, limit: int = 5) -> list[dict]:
    """
    Retourne les meilleurs scores, optionnellement filtrés par jeu.
    
    TODO: Implémente cette fonction.
    
    Doit:
    1. Charger les scores
    2. Si 'game' est fourni, filtrer par ce jeu
    3. Trier par score décroissant
    4. Retourner les 'limit' premiers
    
    Hints:
    - sorted() avec key=lambda x: x["score"], reverse=True
    - List comprehension pour filtrer : [s for s in scores if condition]
    """
    pass  # Remplace par ton code


def get_stats(game: str | None = None) -> dict:
    """
    Calcule des statistiques sur les scores.
    
    TODO: Implémente cette fonction.
    
    Doit retourner un dict avec :
    - total_games: nombre total de parties
    - average_score: score moyen (arrondi à 2 décimales)
    - best_score: meilleur score
    - worst_score: pire score
    - unique_players: nombre de joueurs uniques
    
    Si aucun score, retourne des valeurs à 0.
    
    Hints:
    - sum() pour la somme
    - len() pour le nombre
    - max() et min()
    - round(value, 2) pour arrondir
    - set() pour les valeurs uniques : {s["player"] for s in scores}
    """
    pass  # Remplace par ton code


def display_leaderboard(game: str | None = None) -> None:
    """
    Affiche un leaderboard formaté dans le terminal.
    
    TODO: Implémente cette fonction.
    
    Exemple de sortie attendue :
    
    🏆 LEADERBOARD — Space Invaders
    ================================
    #1  Alice      15000 pts
    #2  Bob        12000 pts
    #3  Charlie     9500 pts
    ================================
    📊 Stats: 10 parties | Moy: 11500.00 | 5 joueurs
    
    Hints:
    - Utilise f-strings avec alignement : f"{'texte':<15}" (aligne à gauche, 15 chars)
    - Utilise get_top_scores() et get_stats()
    """
    pass  # Remplace par ton code


# ============================================================
# MAIN — Tests de tes implémentations
# ============================================================

if __name__ == "__main__":
    # Nettoyer les anciens scores pour un test propre
    if SCORES_FILE.exists():
        SCORES_FILE.unlink()
    
    print("🎮 Game Score Tracker — Test\n")
    
    # Ajouter des scores
    test_data = [
        ("Alice", "Space Invaders", 15000),
        ("Bob", "Space Invaders", 12000),
        ("Charlie", "Space Invaders", 9500),
        ("Alice", "Space Invaders", 18000),
        ("Diana", "Pac-Man", 25000),
        ("Bob", "Pac-Man", 20000),
        ("Eve", "Pac-Man", 30000),
        ("Alice", "Tetris", 50000),
    ]
    
    print("📝 Enregistrement des scores...")
    for player, game, score in test_data:
        entry = add_score(player, game, score)
        if entry:
            print(f"  ✅ {player} — {game}: {score}")
    
    print()
    
    # Afficher les leaderboards
    display_leaderboard("Space Invaders")
    print()
    display_leaderboard("Pac-Man")
    print()
    display_leaderboard()  # Tous les jeux
    
    # Nettoyer
    if SCORES_FILE.exists():
        SCORES_FILE.unlink()
    
    print("\n✅ Tous les tests passés !")
