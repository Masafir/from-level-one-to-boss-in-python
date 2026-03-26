# Module 12 — ETL et Data Pipelines 🚰

> **Objectif** : Apprendre à extraire, transformer et charger de la donnée (Extract, Transform, Load). Python est LE roi incontesté de ce domaine.

## 1. Qu'est-ce qu'un ETL ?

**ETL = Extract, Transform, Load**
C'est le processus de prendre de la donnée de la source A, la nettoyer/modifier, et la stocker dans la cible B.

*   **Extract (Extraction)** : Lire depuis une API, une base SQL, un CSV, scrapper un site Web, etc.
*   **Transform (Transformation)** : Nettoyer, filtrer, agréger, formater, enrichir les données.
*   **Load (Chargement)** : Écrire dans une Data Warehouse (BigQuery, Snowflake), une BDD SQL, des fichiers Parquet/CSV, etc.

*En Node.js, tu ferais ça avec des streams. En Python, on utilise des générateurs et des librairies spécialisées.*

## 2. Extraction (Extact)

### Lire du CSV (Standard Library)

```python
import csv

def extract_csv(filepath: str) -> list[dict]:
    data = []
    with open(filepath, mode="r", encoding="utf-8") as f:
        # DictReader transforme chaque ligne en dictionnaire (headers = clés)
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data
    
# output: [{"id": "1", "name": "Alice", "score": "100"}, ...]
```

### Lire depuis une API (avec httpx)

```python
# pip install httpx
import httpx

def extract_api(url: str) -> list[dict]:
    # httpx est l'équivalent moderne de requests (supporte async)
    with httpx.Client() as client:
        response = client.get(url)
        response.raise_for_status() # Lève une erreur si status != 200
        return response.json()
```

### Le problème de la RAM : Les Générateurs (Yield)

Si tu as un CSV de 10 Go, `data.append(row)` va faire exploser ta RAM !
**Solution : Les générateurs (yield)**. C'est l'équivalent des Streams en Node.

```python
def extract_csv_stream(filepath: str): # -> Generator[dict, None, None]
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row  # ⬅️ Magie ! Ne garde qu'une seule ligne en mémoire à la fois

# Utilisation
for row in extract_csv_stream("huge_file.csv"):
    process(row) # Traite une ligne à la fois, consommation RAM quasi nulle
```

## 3. Transformation (Transform)

La transformation est le "T" de ETL. Elle inclut : type casting, filtrage, calculs, etc.

```python
def transform_data(raw_data_stream):
    """Prend un générateur en entrée et retourne un générateur transformé."""
    for row in raw_data_stream:
        # 1. Type casting (typage)
        try:
            score = int(row["score"])
        except (ValueError, KeyError):
            continue # Skip les lignes invalides (filtrage)
            
        # 2. Nettoyage
        name = row.get("name", "Unknown").strip().title()
        
        # 3. Enrichissement / Calculs
        is_pro = score > 1000
        
        yield {
            "player_name": name,
            "score_val": score,
            "is_pro": is_pro
        }
```

> **Note :** On construira des pipelines où chaque étape est un générateur qui prend le générateur précédent en entrée.

## 4. Chargement (Load)

### Écrire en CSV

```python
def load_csv(data_stream, output_filepath: str):
    # Récupérer le premier élément pour avoir les headers
    try:
        first_row = next(data_stream)
    except StopIteration:
        return # Stream vide

    headers = first_row.keys()

    with open(output_filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerow(first_row)
        
        # Écrire le reste (toujours une ligne à la fois = RAM friendly)
        for row in data_stream:
            writer.writerow(row)
```

### Écrire en SQL (avec SQLAlchemy Core ou SQLite3)

```python
import sqlite3

def load_sqlite(data_stream, db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players 
        (name TEXT, score INTEGER, is_pro BOOLEAN)
    ''')
    
    # executemany est beaucoup plus rapide que des inserts individuels
    # MAIS il a besoin d'une liste (ou d'un batch), on va batcher !
    
    batch = []
    batch_size = 1000
    
    for row in data_stream:
        batch.append((row["player_name"], row["score_val"], row["is_pro"]))
        
        if len(batch) >= batch_size:
            cursor.executemany('INSERT INTO players VALUES (?, ?, ?)', batch)
            conn.commit()
            batch.clear()
            
    # Insérer ce qui reste (le reliquat)
    if batch:
        cursor.executemany('INSERT INTO players VALUES (?, ?, ?)', batch)
        conn.commit()
        
    conn.close()
```

## 5. Orchestration : Assembler le Pipeline

Le design pattern ultime en Python pour les pipelines simples : **enchainer les générateurs**.

```python
# 1. Extract
raw_stream = extract_csv_stream("raw_players.csv")

# 2. Transform 
clean_stream = transform_data(raw_stream)

# 3. Transform 2 (ex: filtrer les pro seulement)
def filter_pro(stream):
    for row in stream:
        if row["is_pro"]:
            yield row
            
pro_only_stream = filter_pro(clean_stream)

# 4. Load
load_sqlite(pro_only_stream, "analytics.db")

print("✅ Pipeline terminé avec une consommation RAM minime !")
```

## 6. Bonnes pratiques en Data Engineering

1. **Idempotence** : Si tu relances ton pipeline 2 fois, le résultat final doit être le même (pas de doublons). *Solution: utiliser des UPSERT (Update/Insert) ou nettoyer la table cible avant.*
2. **Gestion des erreurs (Dead Letter Queue)** : Que faire si une ligne sur 1 million est mal formatée ? Ne fais pas planter tout le script ! Écris la ligne défectueuse dans un fichier `errors.csv` (la Dead Letter Queue) et continue.
3. **Logs** : Loguer le début, la fin, et périodiquement (ex: "Traitement de 10 000 lignes...") pour savoir si ça tourne ou si c'est bloqué.
4. **Batching** : En base de données, faire 1000 INSERTS unitaires est ultra lent. Faire 1 gros INSERT de 1000 lignes (`executemany`) est fulgurant.

---

## 🎯 Résumé

| Concept | Explication |
|---------|-------------|
| **ETL** | Extract (lire), Transform (modifier), Load (sauvegarder) |
| **Générateurs (`yield`)** | Permet de traiter 1 ligne à la fois. Indispensable pour la RAM. (≈ Streams en Node) |
| **`csv.DictReader`** | Lit un CSV et transforme chaque ligne en Dictionnaire. |
| **Batching** | Grouper les opérations d'écriture (ex: `executemany`) pour les performances. |
| **Idempotence** | Le script produit le même résultat peu importe combien de fois il est exécuté. |

---

➡️ **Maintenant, code ton propre ETL dans les exercices !**
