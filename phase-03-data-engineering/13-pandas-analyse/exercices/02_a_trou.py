"""
Module 13 — Exercice à trou #2
🎯 Thème : Nettoyage de données (Cleaning), Merge et Fonctions Vectorisées

Dans la vraie vie, la donnée est TOUJOURS sale. Pandas brille ici.

Complète les ___ pour nettoyer cette liste de joueurs et d'abonnements.
"""

import pandas as pd
import numpy as np

# Table Joueurs (Sale)
PLAYERS_CSV = [
    {"id": 1, "name": "  alice ", "score": 1500, "country": "FR"},
    {"id": 2, "name": "BOB", "score": None, "country": "fr"}, # Score manquant, fr miniscule
    {"id": 3, "name": "Charlie", "score": -50, "country": "US"}, # Score négatif ?
    {"id": 4, "name": None, "score": 100, "country": "BE"}, # Nom manquant
    {"id": 5, "name": "Eve", "score": 900, "country": "FR"}
]

# Table Abonnements (A lier via l'ID)
SUBS_CSV = [
    {"user_id": 1, "plan": "Premium"},
    {"user_id": 3, "plan": "Basic"},
    {"user_id": 5, "plan": "VIP"}
    # Bob (2) et l'ID 4 n'ont pas d'abonnements !
]

def clean_and_merge():
    # Création des DataFrames
    df_players = pd.DataFrame(PLAYERS_CSV)
    df_subs = pd.DataFrame(SUBS_CSV)
    
    print("--- 🧹 Avant nettoyage ---")
    print(df_players)
    
    # 1. Retirer les lignes où le NOM est manquant (NaN)
    # df.dropna(subset=[...]) supprime les lignes si une colonne spécifique est vide
    df_players.dropna(subset=["___"], inplace=True) # Quelle colonne ne doit pas être vide ?
    assert len(df_players) == 4
    
    # 2. Remplacer les scores manquants (NaN) par 0
    df_players["score"] = df_players["score"].___(0) # Quelle méthode ("fill not available") ?
    
    # 3. Remplacer les scores négatifs par 0 en utilisant np.where
    # Si condition_vrai, alors A, sinon B
    df_players["score"] = np.___(df_players["score"] < 0, 0, df_players["score"]) # Equivalent du if/else sur une colonne !
    assert df_players[df_players["id"] == 3]["score"].iloc[0] == 0  # Charlie devrait être à 0
    
    # 4. Standardiser les strings (noms trimmés lowercase, country uppercase)
    # En pandas, df["col"].str.method() permet d'appliquer une méthode de string sur toute la colonne !
    df_players["name"] = df_players["name"].str.strip().str.___() # Quelle méthode de string pour lowercase ?
    df_players["country"] = df_players["country"].str.upper()
    assert df_players.iloc[0]["name"] == "alice"
    assert df_players.iloc[1]["country"] == "FR"

    # 5. Joindre (Merge) avec df_subs !
    # On fait un LEFT JOIN : on garde tous les joueurs, et on ajoute l'abonnement s'il existe
    df_final = pd.___( # Quelle fonction pandas pour joindre 2 DF ?
        df_players, 
        df_subs, 
        ___="left",  # Quel type de join ? (left)
        left_on="___", # Quelle colonne côté joueur ?
        right_on="user_id" # Côté abonnement
    )
    
    # 6. Remplir les abonnements manquants créés par le Join
    df_final["plan"] = df_final["plan"].fillna("Free")
    
    print("\n--- ✨ Après nettoyage et Merge ---")
    print(df_final)
    
    # Vérifications finales
    bob_plan = df_final[df_final["name"] == "bob"]["plan"].iloc[0]
    assert bob_plan == "Free", "Bob n'étant pas dans SUBS_CSV, son plan devrait être Free !"
    
    print("\n✅ Exercice 02 terminé ! Tu as fait de la Data Prep.")

if __name__ == "__main__":
    clean_and_merge()
