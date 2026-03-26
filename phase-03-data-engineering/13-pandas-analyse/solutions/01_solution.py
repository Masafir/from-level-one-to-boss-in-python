"""Module 13 — Solution exercice à trou #1"""

import pandas as pd

GAME_DATA = {
    "player_id": [1, 2, 3, 4, 5, 6, 7],
    "username": ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace"],
    "level": [5, 12, 42, 3, 50, 8, 20],
    "gold": [100, 500, 2000, 50, 10000, 200, 1500],
    "class": ["Warrior", "Mage", "Mage", "Rogue", "Warrior", "Rogue", "Mage"]
}

def analyze_players():
    print("--- 📊 Analyse Basique des Joueurs ---")
    
    df = pd.DataFrame(GAME_DATA)
    print(f"✅ DataFrame créé ! ({len(df)} lignes)")
    
    max_level = df["level"].max()
    print(f"🏆 Niveau max : {max_level}")
    assert max_level == 50
    
    veterans = df[ df["level"] >= 20 ]
    print(f"🗡️ Nombre de Vétérans (lvl >= 20) : {len(veterans)}")
    assert len(veterans) == 3
    
    pro_mages = df[ (df["level"] >= 20) & (df["class"] == "Mage") ]
    print(f"🧙‍♂️ Mages HL : {list(pro_mages['username'])}")
    assert len(pro_mages) == 2
    
    df["is_rich"] = df["gold"] > 1000
    assert sum(df["is_rich"]) == 3
    
    avg_gold_by_class = df.groupby("class")["gold"].mean()
    print("\n💰 Or moyen par classe :")
    print(avg_gold_by_class)
    assert avg_gold_by_class["Mage"] > 1000
    
    print("\n✅ Exercice 01 terminé ! Pandas = Magique.")

if __name__ == "__main__":
    analyze_players()
