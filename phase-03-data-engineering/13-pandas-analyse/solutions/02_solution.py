"""Module 13 — Solution exercice à trou #2"""

import pandas as pd
import numpy as np

PLAYERS_CSV = [
    {"id": 1, "name": "  alice ", "score": 1500, "country": "FR"},
    {"id": 2, "name": "BOB", "score": None, "country": "fr"},
    {"id": 3, "name": "Charlie", "score": -50, "country": "US"},
    {"id": 4, "name": None, "score": 100, "country": "BE"},
    {"id": 5, "name": "Eve", "score": 900, "country": "FR"}
]

SUBS_CSV = [
    {"user_id": 1, "plan": "Premium"},
    {"user_id": 3, "plan": "Basic"},
    {"user_id": 5, "plan": "VIP"}
]

def clean_and_merge():
    df_players = pd.DataFrame(PLAYERS_CSV)
    df_subs = pd.DataFrame(SUBS_CSV)
    
    print("--- 🧹 Avant nettoyage ---")
    print(df_players)
    
    df_players.dropna(subset=["name"], inplace=True)
    assert len(df_players) == 4
    
    df_players["score"] = df_players["score"].fillna(0)
    
    df_players["score"] = np.where(df_players["score"] < 0, 0, df_players["score"])
    assert df_players[df_players["id"] == 3]["score"].iloc[0] == 0
    
    df_players["name"] = df_players["name"].str.strip().str.lower()
    df_players["country"] = df_players["country"].str.upper()
    assert df_players.iloc[0]["name"] == "alice"
    assert df_players.iloc[1]["country"] == "FR"

    df_final = pd.merge(
        df_players, 
        df_subs, 
        how="left",
        left_on="id",
        right_on="user_id"
    )
    
    df_final["plan"] = df_final["plan"].fillna("Free")
    
    print("\n--- ✨ Après nettoyage et Merge ---")
    print(df_final)
    
    bob_plan = df_final[df_final["name"] == "bob"]["plan"].iloc[0]
    assert bob_plan == "Free", "Bob n'étant pas dans SUBS_CSV, son plan devrait être Free !"
    
    print("\n✅ Exercice 02 terminé ! Tu as fait de la Data Prep.")

if __name__ == "__main__":
    clean_and_merge()
