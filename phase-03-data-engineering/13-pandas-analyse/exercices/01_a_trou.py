"""
Module 13 — Exercice à trou #1
🎯 Thème : Création de DataFrame, Masques Booléens (Filtres) et Aggrégations basiques

Complète les ___ pour que le script d'analyse fonctionne.
Exécute avec : pip install pandas
               python 01_a_trou.py
"""

import pandas as pd

# Données brutes sous forme de dictionnaire (équivalent Data JSON)
GAME_DATA = {
    "player_id": [1, 2, 3, 4, 5, 6, 7],
    "username": ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace"],
    "level": [5, 12, 42, 3, 50, 8, 20],
    "gold": [100, 500, 2000, 50, 10000, 200, 1500],
    "class": ["Warrior", "Mage", "Mage", "Rogue", "Warrior", "Rogue", "Mage"]
}

def analyze_players():
    print("--- 📊 Analyse Basique des Joueurs ---")
    
    # 1. Créer un DataFrame à partir du dictionnaire GAME_DATA
    df = pd.___(GAME_DATA)  # Quelle classe de pandas ?
    print(f"✅ DataFrame créé ! ({len(df)} lignes)")
    
    # 2. Stats globales : Trouver le niveau max
    max_level = df["level"].___()  # Quelle méthode pour le maximum ?
    print(f"🏆 Niveau max : {max_level}")
    assert max_level == 50
    
    # 3. Filtrage (Masque Booléen) : Trouver tous les joueurs niveau >= 20
    # ASTUCE : `df["col"] >= val` crée un masque de True/False, on le passe au DataFrame
    veterans = df[ df["level"] ___ 20 ]  # Quel opérateur ?
    print(f"🗡️ Nombre de Vétérans (lvl >= 20) : {len(veterans)}")
    assert len(veterans) == 3
    
    # 4. Filtrage Multiple : Vétéran (lvl >= 20) ET de classe Mage
    # ATTENTION: Il faut des parenthèses autour de chaque condition !
    pro_mages = df[ (df["level"] >= 20) ___ (df["class"] == "Mage") ] # Quel opérateur binaire ? (Le & bitwise)
    print(f"🧙‍♂️ Mages HL : {list(pro_mages['username'])}")
    assert len(pro_mages) == 2
    
    # 5. Créer une nouvelle colonne : 'is_rich' (> 1000 gold)
    df["is_rich"] = df["gold"] ___ 1000 # Expression booléenne
    assert sum(df["is_rich"]) == 3
    
    # 6. Aggrégation Basique : L'or moyen par classe
    # On groupe par la classe, on prend la colonne gold, on calcule la moyenne
    avg_gold_by_class = df.groupby("___")["gold"].mean()  # Par quelle colonne on groupe ?
    print("\n💰 Or moyen par classe :")
    print(avg_gold_by_class)
    assert avg_gold_by_class["Mage"] > 1000
    
    print("\n✅ Exercice 01 terminé ! Pandas = Magique.")

if __name__ == "__main__":
    analyze_players()
