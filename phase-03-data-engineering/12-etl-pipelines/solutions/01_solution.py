"""Module 12 — Solution exercice à trou #1"""

import json

RAW_DATA = [
    {"user": "Alice", "points": "100", "status": "active", "date": "2023-10-01T12:00:00Z"},
    {"user": "Bob", "points": "-50", "status": "banned", "date": "2023-10-02T14:30:00Z"},
    {"user": "Charlie", "points": "500", "status": "ACTIVE", "date": "2023-10-03T09:15:00Z"},
    {"user": "invalid_user", "points": "abc", "status": "active", "date": "bad_date"},
    {"user": "    Diana   ", "points": "150", "status": "Active", "date": "2023-10-04T16:45:00Z"}
]

def extract_data() -> list[dict]:
    print("📥 Extraction des données...")
    return RAW_DATA

def transform_data(raw_data: list[dict]) -> dict:
    print("⚙️  Transformation des données...")
    valid_data = []
    errors = []

    for row in raw_data:
        try:
            points = int(row["points"])

            if points < 0:
                raise ValueError("Points negatifs interdits")

            user = row["user"].strip()
            status = row["status"].lower()
            is_vip = points >= 300

            valid_data.append({
                "user": user,
                "points": points,
                "status": status,
                "is_vip": is_vip,
                "date": row["date"]
            })

        except ValueError as e:
            errors.append({"row": row, "error": str(e)})

    return {"valid": valid_data, "errors": errors}

def load_data(transformed_data: dict, output_filepath: str):
    print(f"📤 Chargement des données ({len(transformed_data['valid'])} lignes)..")
    with open(output_filepath, mode="w", encoding="utf-8") as f:
        json.dump(transformed_data["valid"], f, indent=4)

def run_pipeline():
    print("🚀 Début du pipeline ETL")
    
    data = extract_data()
    processed = transform_data(data)
    
    assert len(processed["valid"]) == 3, f"Attendu 3 valides, obtenu {len(processed['valid'])}"
    assert len(processed["errors"]) == 2, f"Attendu 2 erreurs, obtenu {len(processed['errors'])}"
    assert processed["valid"][2]["user"] == "Diana", "Le nom devrait être trimmé ('Diana')"
    assert processed["valid"][1]["status"] == "active", "Le status de Charlie devrait être en minuscules"
    assert processed["valid"][1]["is_vip"] is True, "Charlie (500 pts) devrait être VIP"
    
    print("📝 Erreurs rencontrées (Dead Letter Queue) :")
    for err in processed["errors"]:
        print(f"  ❌ {err['row']['user']} -> {err['error']}")
        
    output_file = "users_clean.json"
    load_data(processed, "users_clean.json")
    
    print("✅ Pipeline terminé avec succès !")

if __name__ == "__main__":
    run_pipeline()
