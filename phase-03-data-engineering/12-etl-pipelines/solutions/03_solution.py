"""Module 12 — Solution exercice 3"""

import sqlite3
import csv
import io

DB_PATH = "game_stats.db"

RAW_CSV = "player_id,gold,class_type\n"
for i in range(1, 153):
    RAW_CSV += f"{i},{100 * i},warrior\n"

def extract():
    f = io.StringIO(RAW_CSV)
    reader = csv.DictReader(f)
    for row in reader:
        yield row

def transform(stream):
    for row in stream:
        yield {
            "player_id": int(row["player_id"]),
            "gold": int(row["gold"]),
            "class_type": row["class_type"].upper()
        }

def load(stream):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (player_id INT, gold INT, class_type TEXT)''')
    
    batch = []
    batch_size = 50
    for row in stream:
        batch.append((row["player_id"], row["gold"], row["class_type"]))
        if len(batch) >= batch_size:
            cursor.executemany("INSERT INTO stats VALUES (?, ?, ?)", batch)
            conn.commit()
            batch.clear()
            
    if batch:
        cursor.executemany("INSERT INTO stats VALUES (?, ?, ?)", batch)
        conn.commit()
    conn.close()

def run():
    print("🚀 Démarrage du pipeline")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS stats")
    conn.commit()
    conn.close()
    
    s1 = extract()
    s2 = transform(s1)
    load(s2)
    
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
