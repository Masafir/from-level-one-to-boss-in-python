"""Module 02 — Solution exercice à trou #1"""

game_scores = [150, 300, 75, 420, 200, 90, 500, 180, 350, 60]

last_score = game_scores[-1]
print(f"Dernier score : {last_score}")

top_three = game_scores[:3]
print(f"3 premiers : {top_three}")

middle = game_scores[2:6]
print(f"Du 3ème au 6ème : {middle}")

every_other = game_scores[::2]
print(f"Un sur deux : {every_other}")

reversed_scores = game_scores[::-1]
print(f"Inversé : {reversed_scores}")

doubled = [s * 2 for s in game_scores]
print(f"\nDoublés : {doubled}")

high_scores = [s for s in game_scores if s > 200]
print(f"Scores > 200 : {high_scores}")

labels = ["🔥 high" if s > 200 else "💧 low" for s in game_scores]
print(f"Labels : {labels}")

ranked = [(rank, score) for rank, score in enumerate(game_scores, start=1)]
print(f"Classement : {ranked[:3]}")

inventory = ["sword", "shield", "potion"]
inventory.append("bow")
inventory.insert(0, "helmet")

has_sword = "sword" in inventory
print(f"A une épée : {has_sword}")

sword_index = inventory.index("sword")
print(f"Index de l'épée : {sword_index}")

total = len(inventory)
print(f"Total items : {total}")

players = [
    {"name": "Alice", "score": 1500, "level": 12},
    {"name": "Bob", "score": 3000, "level": 8},
    {"name": "Charlie", "score": 2200, "level": 15},
    {"name": "Diana", "score": 1800, "level": 10},
]

by_score = sorted(players, key=lambda p: p["score"], reverse=True)
print(f"\nPar score : {[p['name'] for p in by_score]}")

by_level = sorted(players, key=lambda p: p["level"])
print(f"Par level : {[p['name'] for p in by_level]}")

high_level_names = [p["name"] for p in players if p["level"] > 10]
print(f"Haut level : {high_level_names}")

position = (100, 250)
x, y = position
print(f"Position : x={x}, y={y}")

first, *rest = [1, 2, 3, 4, 5]
print(f"First: {first}, Rest: {rest}")

player_names = ["Alice", "Bob", "Charlie"]
player_scores = [1500, 3000, 2200]

scores_dict = dict(zip(player_names, player_scores))
print(f"\nScores dict : {scores_dict}")

for name, score in zip(player_names, player_scores):
    print(f"  {name}: {score} pts")

print("\n✅ Exercice terminé avec succès !")
