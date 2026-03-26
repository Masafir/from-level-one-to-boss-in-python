"""
Module 02 — Exercice à trou #2
🎯 Thème : Dictionnaires, sets et itération avancée

Complète les ___ pour que le code fonctionne.
Exécute avec : python 02_a_trou.py
"""

# ============================================================
# PARTIE 1 : Dictionnaires — Gestion d'inventaire RPG
# ============================================================

inventory = {
    "sword": {"damage": 25, "weight": 3.5, "rarity": "common"},
    "fire_staff": {"damage": 40, "weight": 2.0, "rarity": "rare"},
    "shield": {"damage": 0, "weight": 5.0, "rarity": "common"},
    "dragon_amulet": {"damage": 100, "weight": 0.5, "rarity": "legendary"},
}

# Accès safe avec .get() (retourne None si clé absente, ou une valeur par défaut)
potion = inventory.___(  "potion", {"damage": 0, "weight": 0.1, "rarity": "common"})
print(f"Potion : {potion}")

# L'arme avec le plus de dégâts
# Utilise max() avec une key function
strongest = max(inventory.___(), key=lambda item: item[1]["damage"])
# items() retourne des tuples (clé, valeur)
print(f"Arme la plus forte : {strongest[0]} ({strongest[1]['damage']} dégâts)")

# Dict comprehension — filtrer les items rares ou légendaires
rare_items = {
    name: stats
    for name, stats in inventory.___()
    ___ stats["rarity"] in ("rare", "legendary")
}
print(f"Items rares : {list(rare_items.___)}")  # Juste les noms

# Calculer le poids total
total_weight = ___(item["weight"] for item in inventory.___())
print(f"Poids total : {total_weight} kg")


# ============================================================
# PARTIE 2 : Sets — Gestion des compétences
# ============================================================

warrior_skills = {"slash", "block", "charge", "war_cry"}
mage_skills = {"fireball", "ice_bolt", "block", "teleport"}
rogue_skills = {"backstab", "dodge", "block", "stealth"}

# Union — toutes les compétences possibles
all_skills = warrior_skills ___ mage_skills ___ rogue_skills  # Quel opérateur ?
print(f"\nToutes les compétences ({len(all_skills)}) : {all_skills}")

# Intersection — compétences communes à tous
common_skills = warrior_skills ___ mage_skills ___ rogue_skills  # Quel opérateur ?
print(f"Compétences communes : {common_skills}")  # {"block"}

# Différence — compétences exclusives au guerrier
warrior_exclusive = warrior_skills ___ (mage_skills ___ rogue_skills)
print(f"Exclusif guerrier : {warrior_exclusive}")

# Vérifier si un set est un sous-ensemble d'un autre
basic_skills = {"block"}
is_subset = basic_skills.___( warrior_skills)  # Quelle méthode ?
print(f"Basic est sous-ensemble de warrior : {is_subset}")  # True

# Set comprehension — skills qui contiennent la lettre 'a'
skills_with_a = {skill for skill in all_skills ___ "a" in skill}
print(f"Skills avec 'a' : {skills_with_a}")


# ============================================================
# PARTIE 3 : Combinaison — Analyse de données de jeu
# ============================================================

# Données de parties jouées
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

# Joueurs uniques (utilise un set !)
unique_players = {entry[___] for entry in game_log}
print(f"\nJoueurs : {unique_players}")

# Jeux uniques
unique_games = {entry[___] for entry in game_log}
print(f"Jeux : {unique_games}")

# Score moyen par joueur — utilise un dict pour accumuler
from collections import ___  # Importer le bon type

# defaultdict crée automatiquement une valeur par défaut pour les clés manquantes
player_scores = defaultdict(___)  # Quel type par défaut ? (une liste vide)

for entry in game_log:
    player_scores[entry["player"]].___(entry["score"])

# Calculer la moyenne pour chaque joueur
averages = {
    player: ___( scores) / len(scores)
    for player, scores in player_scores.items()
}
print(f"Moyennes : {averages}")

# Qui a le meilleur score moyen ?
best_player = ___(averages, key=averages.get)  # max sur les clés du dict
print(f"Meilleur joueur : {best_player} ({averages[best_player]:.0f} pts)")

# Taux de victoire par joueur
wins = defaultdict(int)  # int() retourne 0 par défaut
total = defaultdict(int)

for entry in game_log:
    total[entry["player"]] += 1
    if entry[___]:  # Quelle clé pour savoir si le joueur a gagné ?
        wins[entry["player"]] += 1

win_rates = {
    player: ___(wins[player] / total[player] * 100, 1)  # Arrondir à 1 décimale
    for player in total
}
print(f"Taux de victoire : {win_rates}")


# ============================================================
# CHECK FINAL
# ============================================================

if __name__ == "__main__":
    print("\n✅ Exercice terminé avec succès !")
