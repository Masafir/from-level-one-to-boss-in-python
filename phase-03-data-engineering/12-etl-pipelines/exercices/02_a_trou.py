"""
Module 12 — Exercice à trou #2
🎯 Thème : Pipeline avec des Générateurs (Streaming)

Ceci est le VRAI secret du Data Engineering en Python.
On ne charge pas tout en mémoire ! On utilise le mot clé `yield`.

Complète les ___ pour que le pipeline de streaming fonctionne.
"""

import csv
import io

CSV_DATA = """id,score,name
1,300,Alice
2,invalid,Bob
3,500,Charlie
4,-10,Diana
5,800,Eve
"""

# ============================================================
# EXTRACT STREAM
# ============================================================

def extract_stream():
    """Simule la lecture ligne par ligne d'un gros fichier CSV."""
    # On simule un fichier avec un StringIO (pour ne pas créer un vrai fichier)
    f = io.StringIO(CSV_DATA)
    reader = csv.DictReader(f)
    
    for row in reader:
        ___ row  # Quel mot clé pour faire de cette fonction un générateur ?

# ============================================================
# TRANSFORM STREAMS
# ============================================================

def parse_scores(stream):
    """
    Transform Stream #1 : Convertit le score en entier.
    Ignore les lignes invalides ou négatives.
    """
    for row in stream:
        try:
            val = int(row["score"])
            if val < 0:
                continue # Ignore les scores négatifs
            row["score_int"] = val
            ___ row  # On envoie la ligne modifiée à l'étape suivante !
        except ValueError:
            pass # Ignore les ValueError

def filter_top_players(stream, threshold: int = 400):
    """
    Transform Stream #2 : Ne garde que les joueurs au dessus du threshold.
    """
    for row in ___: # On itère sur le générateur reçu en entrée
        if row["score_int"] >= threshold:
            yield row

# ============================================================
# LOAD STREAM
# ============================================================

def load_to_console(stream):
    """
    Load Stream : Point de terminaison (consommateur final).
    Il n'y a pas de yield ici. C'est lui qui "tire" la donnée.
    """
    count = 0
    print("🔥 Début du traitement streaming...")
    for row in stream:
        print(f"✅ Sauvegardé : {row['name']} (Score: {row['score_int']})")
        count += 1
    return count

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    # 1. On initie le générateur d'extraction
    raw_stream = ___()
    
    # 2. On enchaîne avec le premier transformateur
    parsed_stream = ___(raw_stream)
    
    # 3. On filtre (seulement les >= 400)
    top_stream = filter_top_players(___, threshold=400)
    
    # 4. On lance l'exécution en consommant le générateur final !
    total_saved = load_to_console(___)
    
    assert total_saved == 2, f"Attendu 2, obtenu {total_saved}"
    print("🎉 Pipeline de streaming exécuté avec succès !")
