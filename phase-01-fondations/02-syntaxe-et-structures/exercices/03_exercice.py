"""
Module 02 — Exercice complet #3
🎯 Thème : Parser et analyser des données de scores de jeu

Tu dois implémenter un système complet de parsing et d'analyse
de données de scores provenant d'un fichier texte.

Exécute avec : python 03_exercice.py
"""

# ============================================================
# DONNÉES BRUTES (simulant un fichier de log de jeu)
# ============================================================

RAW_GAME_LOG = """
# Game Log — Epic Arena Tournament 2024
# Format: PLAYER|GAME|SCORE|DATE|RESULT
#
Alice|Tetris|45000|2024-01-15|WIN
Bob|Space Invaders|12000|2024-01-15|LOSS
Alice|Space Invaders|18000|2024-01-16|WIN
Charlie|Tetris|52000|2024-01-16|WIN
Bob|Tetris|38000|2024-01-17|WIN
Diana|Space Invaders|25000|2024-01-17|WIN
Alice|Pac-Man|8500|2024-01-18|LOSS
Charlie|Pac-Man|9200|2024-01-18|WIN
Bob|Space Invaders|15000|2024-01-19|WIN
Diana|Tetris|41000|2024-01-19|LOSS
Eve|Tetris|60000|2024-01-20|WIN
Eve|Space Invaders|22000|2024-01-20|WIN
Alice|Tetris|55000|2024-01-21|WIN
Charlie|Space Invaders|20000|2024-01-21|LOSS
Bob|Pac-Man|7800|2024-01-22|LOSS
Diana|Pac-Man|11000|2024-01-22|WIN
Eve|Pac-Man|10500|2024-01-23|WIN
Alice|Space Invaders|21000|2024-01-23|WIN
"""


def parse_game_log(raw_data: str) -> list[dict]:
    """
    Parse le log brut et retourne une liste de dictionnaires.

    TODO: Implémente cette fonction.

    Chaque entrée doit être un dict avec les clés :
    - player (str)
    - game (str)
    - score (int)
    - date (str)
    - won (bool) — True si "WIN", False si "LOSS"

    Ignore les lignes vides et les commentaires (commençant par #).

    Hints:
    - Utilise .strip() pour nettoyer les espaces
    - Utilise .startswith("#") pour détecter les commentaires
    - Utilise .split("|") pour séparer les champs
    """
    pass  # Remplace par ton code


def get_unique_values(entries: list[dict], key: str) -> list[str]:
    """
    Retourne les valeurs uniques pour une clé donnée, triées alphabétiquement.

    TODO: Implémente cette fonction.

    Exemple : get_unique_values(entries, "player") → ["Alice", "Bob", ...]

    Hints:
    - Utilise un set comprehension pour l'unicité
    - Utilise sorted() pour trier
    """
    pass  # Remplace par ton code


def get_leaderboard(entries: list[dict], game: str | None = None) -> list[dict]:
    """
    Retourne un leaderboard : pour chaque joueur, son MEILLEUR score.

    TODO: Implémente cette fonction.

    Retourne une liste de dicts triés par score décroissant :
    [{"player": "Eve", "best_score": 60000, "games_played": 2}, ...]

    Si game est spécifié, filtre par ce jeu.

    Hints:
    - Utilise un dict pour accumuler les meilleurs scores par joueur
    - max() pour comparer les scores
    """
    pass  # Remplace par ton code


def get_game_stats(entries: list[dict]) -> dict[str, dict]:
    """
    Calcule des statistiques par jeu.

    TODO: Implémente cette fonction.

    Retourne un dict :
    {
        "Tetris": {
            "total_games": 5,
            "average_score": 47200.0,
            "highest_score": 60000,
            "lowest_score": 38000,
            "win_rate": 80.0,
            "top_player": "Eve",
        },
        ...
    }

    Hints:
    - Regroupe les entrées par jeu avec un defaultdict(list)
    - Calcule les stats pour chaque groupe
    """
    pass  # Remplace par ton code


def get_player_summary(entries: list[dict], player: str) -> dict:
    """
    Résumé complet d'un joueur.

    TODO: Implémente cette fonction.

    Retourne :
    {
        "player": "Alice",
        "total_games": 5,
        "total_wins": 4,
        "win_rate": 80.0,
        "favorite_game": "Tetris",  (le jeu le plus joué)
        "best_score": 55000,
        "best_game": "Tetris",      (le jeu du meilleur score)
        "average_score": 29500.0,
        "games_played": {"Tetris": 2, "Space Invaders": 2, "Pac-Man": 1}
    }

    Hints:
    - Filtre les entrées pour ce joueur
    - Utilise Counter (from collections) pour compter les jeux
    - .most_common(1) retourne le plus fréquent
    """
    pass  # Remplace par ton code


def display_tournament_report(entries: list[dict]) -> None:
    """
    Affiche un rapport de tournoi complet et formaté.

    TODO: Implémente cette fonction.

    Doit afficher :
    1. Header avec le nombre total de parties
    2. Leaderboard général (top 5)
    3. Stats par jeu
    4. Résumé de chaque joueur

    Exemple de format :
    ═══════════════════════════════════════
    🏆 EPIC ARENA TOURNAMENT — RAPPORT
    ═══════════════════════════════════════
    📊 18 parties analysées | 5 joueurs | 3 jeux

    🥇 LEADERBOARD GÉNÉRAL
    ───────────────────────────────────
    #1  Eve             60000 pts
    #2  Alice           55000 pts
    ...

    Hints:
    - Utilise les fonctions que tu as implémentées ci-dessus
    - f-strings avec alignement : f"{'texte':<15}" et f"{nombre:>8}"
    """
    pass  # Remplace par ton code


# ============================================================
# MAIN — Tests
# ============================================================

if __name__ == "__main__":
    entries = parse_game_log(RAW_GAME_LOG)

    if entries is None:
        print("❌ parse_game_log() n'est pas encore implémenté !")
    else:
        print(f"✅ {len(entries)} entrées parsées\n")

        # Test get_unique_values
        players = get_unique_values(entries, "player")
        games = get_unique_values(entries, "game")
        print(f"Joueurs : {players}")
        print(f"Jeux : {games}")

        # Test leaderboard
        print("\n🏆 Leaderboard Tetris :")
        lb = get_leaderboard(entries, "Tetris")
        if lb:
            for i, entry in enumerate(lb, 1):
                print(f"  #{i} {entry['player']}: {entry['best_score']}")

        # Test game stats
        stats = get_game_stats(entries)
        if stats:
            for game, st in stats.items():
                print(f"\n📊 {game}: avg={st['average_score']:.0f}, top={st['top_player']}")

        # Test player summary
        summary = get_player_summary(entries, "Alice")
        if summary:
            print(f"\n👤 Alice: {summary['total_wins']}/{summary['total_games']} wins, fav={summary['favorite_game']}")

        # Rapport complet
        print()
        display_tournament_report(entries)

        print("\n✅ Tous les tests passés !")
