"""
Module 13 — Exercice complet #3
🎯 Thème : Dashboard eSport Analytics & GROUP BY 

Exécute avec : python 03_exercice.py
"""

import pandas as pd
import numpy as np
import random

# ============================================================
# INITIALISATION DES FAUSSES DONNÉES (Ne pas modifier)
# ============================================================
def generate_match_data(n_matches=2000):
    teams = ["Team Liquid", "Cloud9", "G2", "Fnatic", "T1"]
    regions = ["NA", "NA", "EU", "EU", "KR"]
    team_region_map = dict(zip(teams, regions))
    
    data = []
    for match_id in range(1, n_matches + 1):
        teamA, teamB = random.sample(teams, 2)
        winner = random.choice([teamA, teamB])
        duration_min = round(random.uniform(15.0, 55.0), 1)
        kills_teamA = random.randint(5, 30)
        kills_teamB = random.randint(5, 30)
        
        data.append({
            "match_id": match_id,
            "team": teamA,
            "region": team_region_map[teamA],
            "win": int(teamA == winner),
            "kills": kills_teamA,
            "duration": duration_min
        })
        data.append({
            "match_id": match_id,
            "team": teamB,
            "region": team_region_map[teamB],
            "win": int(teamB == winner),
            "kills": kills_teamB,
            "duration": duration_min
        })
    return pd.DataFrame(data)

df = generate_match_data()

# ============================================================
# TODO : ANALYSER LES MATCHS !
# C'est à toi d'écrire le code Pandas pour remplir les variables
# ============================================================
print("🎮 League of Pandas Analytics 🎮")
print(f"Dataset de {len(df)} lignes chargé.\n")

# 1. Kills totaux dans toute la base ?
total_kills = ... # Remplacer ... par l'opération pandas

# 2. Quels sont les 3 matchs les plus longs (top 3 "duration") ? 
# Retourner un DataFrame classé. (Utilise `.sort_values()` et `.head()`)
longest_matches = ...

# 3. Combien de victoires la "Team Liquid" a obtenu ? (Int)
liquid_wins = ...

# 4. Quelle est la moyenne de KILLS (colonnes "kills") par équipe ("team") ?
# Retourne une "Series" (Utilise groupby et mean)
avg_kills_by_team = ...

# 5. (Avancé) Le Win-Rate global par REGION ?
# Groupe par region, calcule la moyenne de la colonne 'win', puis `.sort_values(ascending=False)`
winrate_by_region = ...

# 6. Aggrégations multiples :
# Crée un nouveau DataFrame groupé par équipe qui affiche :
# Le nombre total_kills (somme) et total_wins (somme)
# ASTUCE : df.groupby("...").agg(total_kills=("...", "sum"), ...)
team_dashboard = ...


# ============================================================
# TESTS (Ne pas toucher)
# ============================================================
if __name__ == "__main__":
    try:
        assert isinstance(total_kills, (int, np.integer)) and total_kills > 10000, "1 invalide"
        assert len(longest_matches) == 3, "2 invalide (doit retourner 3 lignes)"
        assert isinstance(liquid_wins, (int, np.integer)), "3 invalide"
        assert "Cloud9" in avg_kills_by_team.index, "4 invalide"
        assert "EU" in winrate_by_region.index, "5 invalide"
        assert "total_kills" in team_dashboard.columns and "total_wins" in team_dashboard.columns, "6 invalide"
        
        print(f"🩸 Kills totaux : {total_kills}")
        print(f"🦄 Liquid Wins : {liquid_wins}")
        print("\n🏆 Win Rate par région :")
        print(round(winrate_by_region * 100, 2))
        
        print("\n📊 Dashboard global :")
        print(team_dashboard)
        
        print("\n✅ Succès complet ! Tu gères le Group By Pandas.")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        # Si KeyError, ton Dashboard généré a les mauvaises colonnes !
