"""
Module 01 — Solution exercice complet #3
🎯 Game Score Tracker CLI
"""

import json
from datetime import datetime
from pathlib import Path

SCORES_FILE = Path(__file__).parent / "scores.json"


def load_scores() -> list[dict]:
    """Charge les scores depuis le fichier JSON."""
    if not SCORES_FILE.exists():
        return []
    content = SCORES_FILE.read_text()
    return json.loads(content)


def save_scores(scores: list[dict]) -> None:
    """Sauvegarde les scores dans le fichier JSON."""
    content = json.dumps(scores, indent=2, ensure_ascii=False)
    SCORES_FILE.write_text(content)


def add_score(player: str, game: str, score: int) -> dict:
    """Ajoute un nouveau score."""
    scores = load_scores()

    entry = {
        "player": player,
        "game": game,
        "score": score,
        "timestamp": datetime.now().isoformat(),
    }

    scores.append(entry)
    save_scores(scores)
    return entry


def get_top_scores(game: str | None = None, limit: int = 5) -> list[dict]:
    """Retourne les meilleurs scores."""
    scores = load_scores()

    if game:
        scores = [s for s in scores if s["game"] == game]

    return sorted(scores, key=lambda x: x["score"], reverse=True)[:limit]


def get_stats(game: str | None = None) -> dict:
    """Calcule des statistiques sur les scores."""
    scores = load_scores()

    if game:
        scores = [s for s in scores if s["game"] == game]

    if not scores:
        return {
            "total_games": 0,
            "average_score": 0,
            "best_score": 0,
            "worst_score": 0,
            "unique_players": 0,
        }

    all_scores = [s["score"] for s in scores]

    return {
        "total_games": len(scores),
        "average_score": round(sum(all_scores) / len(all_scores), 2),
        "best_score": max(all_scores),
        "worst_score": min(all_scores),
        "unique_players": len({s["player"] for s in scores}),
    }


def display_leaderboard(game: str | None = None) -> None:
    """Affiche un leaderboard formaté."""
    title = game if game else "Tous les jeux"
    top = get_top_scores(game)
    stats = get_stats(game)

    print(f"🏆 LEADERBOARD — {title}")
    print("=" * 40)

    for i, entry in enumerate(top, 1):
        player = entry["player"]
        score = entry["score"]
        game_name = f" ({entry['game']})" if not game else ""
        print(f"  #{i}  {player:<15} {score:>8} pts{game_name}")

    print("=" * 40)
    print(
        f"📊 Stats: {stats['total_games']} parties | "
        f"Moy: {stats['average_score']:.2f} | "
        f"{stats['unique_players']} joueurs"
    )


if __name__ == "__main__":
    if SCORES_FILE.exists():
        SCORES_FILE.unlink()

    print("🎮 Game Score Tracker — Test\n")

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
    display_leaderboard("Space Invaders")
    print()
    display_leaderboard("Pac-Man")
    print()
    display_leaderboard()

    if SCORES_FILE.exists():
        SCORES_FILE.unlink()

    print("\n✅ Tous les tests passés !")
