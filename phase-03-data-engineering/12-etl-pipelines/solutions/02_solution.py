"""Module 12 — Solution exercice à trou #2"""

import csv
import io

CSV_DATA = """id,score,name
1,300,Alice
2,invalid,Bob
3,500,Charlie
4,-10,Diana
5,800,Eve
"""

def extract_stream():
    f = io.StringIO(CSV_DATA)
    reader = csv.DictReader(f)
    for row in reader:
        yield row

def parse_scores(stream):
    for row in stream:
        try:
            val = int(row["score"])
            if val < 0:
                continue
            row["score_int"] = val
            yield row
        except ValueError:
            pass

def filter_top_players(stream, threshold: int = 400):
    for row in stream:
        if row["score_int"] >= threshold:
            yield row

def load_to_console(stream):
    count = 0
    print("🔥 Début du traitement streaming...")
    for row in stream:
        print(f"✅ Sauvegardé : {row['name']} (Score: {row['score_int']})")
        count += 1
    return count

if __name__ == "__main__":
    raw_stream = extract_stream()
    parsed_stream = parse_scores(raw_stream)
    top_stream = filter_top_players(parsed_stream, threshold=400)
    total_saved = load_to_console(top_stream)
    
    assert total_saved == 2, f"Attendu 2, obtenu {total_saved}"
    print("🎉 Pipeline de streaming exécuté avec succès !")
