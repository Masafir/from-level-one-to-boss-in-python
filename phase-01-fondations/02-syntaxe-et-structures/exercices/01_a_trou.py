"""
Module 02 — Exercice à trou #1
🎯 Thème : Listes, slicing et list comprehensions

Complète les ___ pour que le code fonctionne.
Exécute avec : python 01_a_trou.py
"""

# ============================================================
# PARTIE 1 : Manipuler des listes de scores
# ============================================================

game_scores = [150, 300, 75, 420, 200, 90, 500, 180, 350, 60]

# Récupère le dernier score avec un index négatif
last_score = game_scores[___]
print(f"Dernier score : {last_score}")  # 60

# Slicing : les 3 premiers scores
top_three = game_scores[:___]
print(f"3 premiers : {top_three}")  # [150, 300, 75]

# Slicing : les scores du 3ème au 6ème (index 2 à 5 inclus)
middle = game_scores[___:___]
print(f"Du 3ème au 6ème : {middle}")  # [75, 420, 200, 90]

# Slicing : un score sur deux
every_other = game_scores[::___]
print(f"Un sur deux : {every_other}")  # [150, 75, 200, 500, 350]

# Inverser la liste avec le slicing
reversed_scores = game_scores[::___]
print(f"Inversé : {reversed_scores}")


# ============================================================
# PARTIE 2 : List Comprehensions
# ============================================================

# Doubler chaque score (équivalent de .map(s => s * 2))
doubled = [s * ___ for s in game_scores]
print(f"\nDoublés : {doubled}")

# Garder seulement les scores > 200 (équivalent de .filter(s => s > 200))
high_scores = [s for s in game_scores ___ s > 200]
print(f"Scores > 200 : {high_scores}")  # [300, 420, 500, 350]

# Labelliser chaque score "🔥 high" ou "💧 low" (ternaire dans comprehension)
labels = [___ if s > 200 ___ "💧 low" for s in game_scores]
print(f"Labels : {labels}")

# Créer une liste de tuples (rang, score) avec enumerate
# enumerate(liste, start=1) donne des tuples (index, valeur)
ranked = [(rank, score) for rank, score in ___(game_scores, start=___)]
print(f"Classement : {ranked[:3]}")


# ============================================================
# PARTIE 3 : Opérations sur les listes
# ============================================================

inventory = ["sword", "shield", "potion"]

# Ajouter un item à la fin
inventory.___(  "bow")  # Quel méthode ? (comme .push() en JS)

# Ajouter un item au début (index 0)
inventory.___(0, "helmet")  # Quelle méthode ?

# Vérifier si un item est dans la liste
has_sword = "sword" ___ inventory  # Quel opérateur ?
print(f"A une épée : {has_sword}")  # True

# Trouver l'index d'un item
sword_index = inventory.___(  "sword")  # Quelle méthode ?
print(f"Index de l'épée : {sword_index}")

# Nombre d'items
total = ___(inventory)  # Quelle fonction built-in ?
print(f"Total items : {total}")


# ============================================================
# PARTIE 4 : Trier des données
# ============================================================

players = [
    {"name": "Alice", "score": 1500, "level": 12},
    {"name": "Bob", "score": 3000, "level": 8},
    {"name": "Charlie", "score": 2200, "level": 15},
    {"name": "Diana", "score": 1800, "level": 10},
]

# Trier par score décroissant (sans modifier l'original)
by_score = sorted(players, key=___ p: p["score"], reverse=___)
print(f"\nPar score : {[p['name'] for p in by_score]}")
# ["Bob", "Charlie", "Diana", "Alice"]

# Trier par level ascendant
by_level = sorted(players, key=lambda p: p[___])
print(f"Par level : {[p['name'] for p in by_level]}")
# ["Bob", "Diana", "Alice", "Charlie"]

# Extraire seulement les noms des joueurs level > 10
high_level_names = [p[___] for p in players if p[___] > 10]
print(f"Haut level : {high_level_names}")  # ["Alice", "Charlie"]


# ============================================================
# PARTIE 5 : Unpacking et zip
# ============================================================

# Unpacking (destructuring)
position = (100, 250)
x, y = ___
print(f"Position : x={x}, y={y}")

# Unpacking avec * (rest operator, comme ...rest en JS)
first, *rest = [1, 2, 3, 4, 5]
print(f"First: {first}, Rest: {___}")  # First: 1, Rest: [2, 3, 4, 5]

# Zip : combiner deux listes
player_names = ["Alice", "Bob", "Charlie"]
player_scores = [1500, 3000, 2200]

# Créer un dictionnaire à partir de deux listes
scores_dict = ___(zip(player_names, player_scores))
print(f"\nScores dict : {scores_dict}")
# {"Alice": 1500, "Bob": 3000, "Charlie": 2200}

# Itérer sur deux listes en parallèle
for name, score in ___(player_names, player_scores):
    print(f"  {name}: {score} pts")


# ============================================================
# CHECK FINAL
# ============================================================

if __name__ == "__main__":
    print("\n✅ Exercice terminé avec succès !")
