"""Module 02 — Solution exercice à trou #2"""

from collections import defaultdict

inventory = {
    "sword": {"damage": 25, "weight": 3.5, "rarity": "common"},
    "fire_staff": {"damage": 40, "weight": 2.0, "rarity": "rare"},
    "shield": {"damage": 0, "weight": 5.0, "rarity": "common"},
    "dragon_amulet": {"damage": 100, "weight": 0.5, "rarity": "legendary"},
}

potion = inventory.get("potion", {"damage": 0, "weight": 0.1, "rarity": "common"})
print(f"Potion : {potion}")

strongest = max(inventory.items(), key=lambda item: item[1]["damage"])
print(f"Arme la plus forte : {strongest[0]} ({strongest[1]['damage']} dégâts)")

rare_items = {
    name: stats
    for name, stats in inventory.items()
    if stats["rarity"] in ("rare", "legendary")
}
print(f"Items rares : {list(rare_items.keys())}")

total_weight = sum(item["weight"] for item in inventory.values())
print(f"Poids total : {total_weight} kg")

warrior_skills = {"slash", "block", "charge", "war_cry"}
mage_skills = {"fireball", "ice_bolt", "block", "teleport"}
rogue_skills = {"backstab", "dodge", "block", "stealth"}

all_skills = warrior_skills | mage_skills | rogue_skills
print(f"\nToutes les compétences ({len(all_skills)}) : {all_skills}")

common_skills = warrior_skills & mage_skills & rogue_skills
print(f"Compétences communes : {common_skills}")

warrior_exclusive = warrior_skills - (mage_skills | rogue_skills)
print(f"Exclusif guerrier : {warrior_exclusive}")

basic_skills = {"block"}
is_subset = basic_skills.issubset(warrior_skills)
print(f"Basic est sous-ensemble de warrior : {is_subset}")

skills_with_a = {skill for skill in all_skills if "a" in skill}
print(f"Skills avec 'a' : {skills_with_a}")

game_log = [
    {"player": "Alice", "game": "RPG", "score": 1500, "won": True},
    {"player": "Bob", "game": "FPS", "score": 3000, "won": False},
    {"player": "Alice", "game": "FPS", "score": 2200, "won": True},
    {"player": "Charlie", "game": "RPG", "score": 1800, "won": True},
    {"player": "Bob", "game": "RPG", "score": 900, "won": False},
    {"player": "Alice", "game": "RPG", "score": 2500, "won": True},
    {"player": "Diana", "game": "FPS", "score": 4000, "won": True},
    {"player": "Charlie", "game": "FPS", "score": 3500, "won": True},
]

unique_players = {entry["player"] for entry in game_log}
print(f"\nJoueurs : {unique_players}")

unique_games = {entry["game"] for entry in game_log}
print(f"Jeux : {unique_games}")

player_scores = defaultdict(list)
for entry in game_log:
    player_scores[entry["player"]].append(entry["score"])

averages = {
    player: sum(scores) / len(scores)
    for player, scores in player_scores.items()
}
print(f"Moyennes : {averages}")

best_player = max(averages, key=averages.get)
print(f"Meilleur joueur : {best_player} ({averages[best_player]:.0f} pts)")

wins = defaultdict(int)
total = defaultdict(int)
for entry in game_log:
    total[entry["player"]] += 1
    if entry["won"]:
        wins[entry["player"]] += 1

win_rates = {
    player: round(wins[player] / total[player] * 100, 1)
    for player in total
}
print(f"Taux de victoire : {win_rates}")

print("\n✅ Exercice terminé avec succès !")
