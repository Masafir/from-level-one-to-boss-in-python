"""Module 02 — Solution exercice complet #3 — Tournament Data Parser"""

from collections import Counter, defaultdict

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
    entries = []
    for line in raw_data.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|")
        entries.append({
            "player": parts[0],
            "game": parts[1],
            "score": int(parts[2]),
            "date": parts[3],
            "won": parts[4] == "WIN",
        })
    return entries


def get_unique_values(entries: list[dict], key: str) -> list[str]:
    return sorted({entry[key] for entry in entries})


def get_leaderboard(entries: list[dict], game: str | None = None) -> list[dict]:
    filtered = [e for e in entries if e["game"] == game] if game else entries

    player_data: dict[str, dict] = {}
    for entry in filtered:
        player = entry["player"]
        if player not in player_data:
            player_data[player] = {"player": player, "best_score": 0, "games_played": 0}
        player_data[player]["games_played"] += 1
        player_data[player]["best_score"] = max(
            player_data[player]["best_score"], entry["score"]
        )

    return sorted(player_data.values(), key=lambda p: p["best_score"], reverse=True)


def get_game_stats(entries: list[dict]) -> dict[str, dict]:
    by_game = defaultdict(list)
    for entry in entries:
        by_game[entry["game"]].append(entry)

    stats = {}
    for game, game_entries in by_game.items():
        scores = [e["score"] for e in game_entries]
        wins = sum(1 for e in game_entries if e["won"])
        top_entry = max(game_entries, key=lambda e: e["score"])

        stats[game] = {
            "total_games": len(game_entries),
            "average_score": round(sum(scores) / len(scores), 1),
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "win_rate": round(wins / len(game_entries) * 100, 1),
            "top_player": top_entry["player"],
        }

    return stats


def get_player_summary(entries: list[dict], player: str) -> dict:
    player_entries = [e for e in entries if e["player"] == player]
    if not player_entries:
        return {}

    scores = [e["score"] for e in player_entries]
    wins = sum(1 for e in player_entries if e["won"])
    game_counts = Counter(e["game"] for e in player_entries)
    best_entry = max(player_entries, key=lambda e: e["score"])

    return {
        "player": player,
        "total_games": len(player_entries),
        "total_wins": wins,
        "win_rate": round(wins / len(player_entries) * 100, 1),
        "favorite_game": game_counts.most_common(1)[0][0],
        "best_score": max(scores),
        "best_game": best_entry["game"],
        "average_score": round(sum(scores) / len(scores), 1),
        "games_played": dict(game_counts),
    }


def display_tournament_report(entries: list[dict]) -> None:
    players = get_unique_values(entries, "player")
    games = get_unique_values(entries, "game")

    print("═" * 45)
    print("🏆 EPIC ARENA TOURNAMENT — RAPPORT")
    print("═" * 45)
    print(f"📊 {len(entries)} parties | {len(players)} joueurs | {len(games)} jeux\n")

    print("🥇 LEADERBOARD GÉNÉRAL")
    print("─" * 40)
    for i, entry in enumerate(get_leaderboard(entries)[:5], 1):
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, "  ")
        print(f" {medal} #{i}  {entry['player']:<15} {entry['best_score']:>8} pts")
    print("─" * 40)

    print("\n📊 STATS PAR JEU")
    for game, st in get_game_stats(entries).items():
        print(f"\n  🎮 {game}")
        print(f"     Parties: {st['total_games']} | Moy: {st['average_score']:.0f}")
        print(f"     Best: {st['highest_score']} | Win rate: {st['win_rate']}%")
        print(f"     Top player: {st['top_player']}")

    print(f"\n👤 RÉSUMÉS JOUEURS")
    for player in players:
        s = get_player_summary(entries, player)
        print(f"  {s['player']}: {s['total_wins']}/{s['total_games']} wins "
              f"({s['win_rate']}%) | Fav: {s['favorite_game']} | Best: {s['best_score']}")


if __name__ == "__main__":
    entries = parse_game_log(RAW_GAME_LOG)
    print(f"✅ {len(entries)} entrées parsées\n")

    players = get_unique_values(entries, "player")
    games = get_unique_values(entries, "game")
    print(f"Joueurs : {players}")
    print(f"Jeux : {games}")

    print("\n🏆 Leaderboard Tetris :")
    for i, entry in enumerate(get_leaderboard(entries, "Tetris"), 1):
        print(f"  #{i} {entry['player']}: {entry['best_score']}")

    stats = get_game_stats(entries)
    for game, st in stats.items():
        print(f"\n📊 {game}: avg={st['average_score']:.0f}, top={st['top_player']}")

    summary = get_player_summary(entries, "Alice")
    print(f"\n👤 Alice: {summary['total_wins']}/{summary['total_games']} wins, fav={summary['favorite_game']}")

    print()
    display_tournament_report(entries)
    print("\n✅ Tous les tests passés !")
