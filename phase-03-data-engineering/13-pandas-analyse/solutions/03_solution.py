"""Module 13 — Solution exercice 3"""

import pandas as pd
import numpy as np
import random

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

print("🎮 League of Pandas Analytics 🎮")
print(f"Dataset de {len(df)} lignes chargé.\n")

# 1. Kills totaux dans toute la base ?
total_kills = df["kills"].sum()

# 2. Quels sont les 3 matchs les plus longs (top 3 "duration") ? 
longest_matches = df.sort_values(by="duration", ascending=False).head(3)

# 3. Combien de victoires la "Team Liquid" a obtenu ? (Int)
liquid_wins = df[(df["team"] == "Team Liquid") & (df["win"] == 1)].shape[0]
# Ou : liquid_wins = df[df["team"] == "Team Liquid"]["win"].sum()

# 4. Quelle est la moyenne de KILLS (colonnes "kills") par équipe ("team") ?
avg_kills_by_team = df.groupby("team")["kills"].mean()

# 5. (Avancé) Le Win-Rate global par REGION ?
winrate_by_region = df.groupby("region")["win"].mean().sort_values(ascending=False)

# 6. Aggrégations multiples :
team_dashboard = df.groupby("team").agg(
    total_kills=("kills", "sum"),
    total_wins=("win", "sum")
)

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
