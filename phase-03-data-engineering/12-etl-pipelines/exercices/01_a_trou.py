"""
Module 12 — Exercice à trou #1
🎯 Thème : Pipeline ETL basique en RAM (Extract & Transform avec dicts)

Dans cet exercice, pas de Base de Données ni de générateurs avancés. 
On charge tout en mémoire pour comprendre l'Extract et le Transform.

Complète les ___ pour que le pipeline fonctionne.
Exécute avec : python 01_a_trou.py
"""

import json

# Voici nos données brutes "Extraites" depuis une fausse API
RAW_DATA = [
    {"user": "Alice", "points": "100", "status": "active", "date": "2023-10-01T12:00:00Z"},
    {"user": "Bob", "points": "-50", "status": "banned", "date": "2023-10-02T14:30:00Z"},
    {"user": "Charlie", "points": "500", "status": "ACTIVE", "date": "2023-10-03T09:15:00Z"},
    {"user": "invalid_user", "points": "abc", "status": "active", "date": "bad_date"},
    {"user": "    Diana   ", "points": "150", "status": "Active", "date": "2023-10-04T16:45:00Z"}
]

# ============================================================
# PARTIE 1 : Extract - Simulation
# ============================================================

def extract_data() -> list[dict]:
    """Simule l'extraction de données depuis une API."""
    print("📥 Extraction des données...")
    return RAW_DATA

# ============================================================
# PARTIE 2 : Transform - Nettoyage et typage
# ============================================================

def transform_data(raw_data: list[dict]) -> dict:
    """
    Transforme les données brutes :
    1. type casting : 'points' de string à int
    2. nettoyage : majuscule/minuscule pour 'status', trim espace pour 'user'
    3. filtrage : ignorer les scores invalides (non num) ou négatifs
    Retourne un dict avec 'valid' et 'errors'.
    """
    print("⚙️  Transformation des données...")
    valid_data = []
    errors = []

    for row in raw_data:
        try:
            # 1. Type casting
            points = ___(row["points"])  # Transforme la string en entier

            # 2. Filtrage métier
            if points < ___:  # On ne veut pas de points négatifs
                raise ValueError("Points negatifs interdits")

            # 3. Nettoyage
            user = row["user"].___()  # Retire les espaces au début et fin
            status = row["status"].___()  # Met le status tout en minuscules

            # Enrichissement : ajoutons une colonne "is_vip"
            is_vip = points >= 300

            valid_data.append({
                "user": user,
                "points": points,
                "status": status,
                "is_vip": is_vip,
                "date": row["date"]
            })

        except ___ as e:  # Quelle exception est levée si int("abc") échoue ? (ValueError)
            # Dead Letter Queue : on garde les erreurs au lieu de crasher
            errors.append({"row": row, "error": str(e)})

    return {"valid": valid_data, "errors": errors}

# ============================================================
# PARTIE 3 : Load - Sauvegarde
# ============================================================

def load_data(transformed_data: dict, output_filepath: str):
    """Charge les données transformées (valid) dans un fichier JSON."""
    print(f"📤 Chargement des données ({len(transformed_data['valid'])} lignes)..")
    
    # Écrit dans `output_filepath` au format JSON de façon lisible (indent=4)
    with ___(output_filepath, mode="w", encoding="utf-8") as f: # Ouverture standard de fichier
        json.___(transformed_data["valid"], f, indent=4) # Écrit l'objet JSON (dictionnaire) dans f

# ============================================================
# ORCHESTRATION DU PIPELINE
# ============================================================

def run_pipeline():
    print("🚀 Début du pipeline ETL")
    
    # EXTRACT
    data = ___()
    
    # TRANSFORM
    processed = ___(data)
    
    # Vérifications métier (ne modifie pas ce bloc)
    assert len(processed["valid"]) == 3, f"Attendu 3 valides, obtenu {len(processed['valid'])}"
    assert len(processed["errors"]) == 2, f"Attendu 2 erreurs, obtenu {len(processed['errors'])}"
    assert processed["valid"][2]["user"] == "Diana", "Le nom devrait être trimmé ('Diana')"
    assert processed["valid"][1]["status"] == "active", "Le status de Charlie devrait être en minuscules"
    assert processed["valid"][1]["is_vip"] is True, "Charlie (500 pts) devrait être VIP"
    
    print("📝 Erreurs rencontrées (Dead Letter Queue) :")
    for err in processed["errors"]:
        print(f"  ❌ {err['row']['user']} -> {err['error']}")
        
    # LOAD
    output_file = "users_clean.json"
    ___(processed, output_file)
    
    print("✅ Pipeline terminé avec succès !")

if __name__ == "__main__":
    run_pipeline()
