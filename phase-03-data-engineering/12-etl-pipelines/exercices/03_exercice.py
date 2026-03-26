"""
Module 12 — Exercice complet #3
🎯 Thème : Bâtir un pipeline SQLite + CSV (Générateurs + Batch)

Crée un pipeline ETL complet qui fait l'aller-retour :
1. Crée un CSV géant (simulé en mémoire ou avec une boucle),
2. L'extrait avec un générateur `csv.reader` (ou DictReader).
3. Le transforme : majuscule sur un champ string, casting d'un entier.
4. L'insère dans SQLite avec des batchs de 50 lignes (`cursor.executemany`).

Exécute avec : python 03_exercice.py
"""

import sqlite3
import csv
import io

DB_PATH = "game_stats.db"

# 1. On crée d'abord des données brutes
RAW_CSV = "player_id,gold,class_type\n"
for i in range(1, 153): # 152 lignes
    RAW_CSV += f"{i},{100 * i},warrior\n"


# ============================================================
# TODO : Implémenter le pipeline de bout en bout
# ============================================================

def extract():
    """Doit yield chaque ligne du CSV via un csv.DictReader."""
    pass

def transform(stream):
    """Doit yield : un int pour l'id et gold. class_type en MAJUSCULE."""
    pass

def load(stream):
    """
    Doit créer une table stats(player_id INT, gold INT, class_type TEXT)
    Puis insérer les données par batch de 50 avec `executemany`.
    Gérer le reliquat < 50 à la fin !
    """
    pass

def run():
    print("🚀 Démarrage du pipeline")
    
    # Connexion à SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Nettoyage pour idempontence
    cursor.execute("DROP TABLE IF EXISTS stats")
    conn.commit()
    conn.close()
    
    # TODO : Lancer la chaîne !
    # s1 = extract()
    # s2 = transform(s1)
    # load(s2)
    
    # --- Tests automatisés (ne pas changer) ---
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM stats")
    count = cur.fetchone()[0]
    
    cur.execute("SELECT player_id, gold, class_type FROM stats LIMIT 1")
    first = cur.fetchone()
    
    assert count == 152, f"La BDD devrait avoir 152 lignes, elle en a {count}."
    assert first[2] == "WARRIOR", f"Les classes doivent être uppercase (obtenu {first[2]})."
    assert isinstance(first[1], int), "L'or doit être un entier."
    
    print(f"✅ Succès ! {count} lignes insérées par batchs.")
    conn.close()

if __name__ == "__main__":
    run()
