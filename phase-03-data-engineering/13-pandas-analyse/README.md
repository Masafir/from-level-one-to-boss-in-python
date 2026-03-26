# Module 13 — Pandas et Analyse de Données 🐼

> **Objectif** : Apprendre `pandas`, la librairie d'analyse de données la plus utilisée au monde. C'est l'équivalent de "Excel sous stéroïdes avec du code".

## 1. Pourquoi Pandas ?

Dans le module précédent (12), on a vu comment traiter de gros volumes de données en streaming (1 ligne à la fois) pour économiser la RAM.
**Pandas fait l'inverse !** Il charge toutes les données en RAM dans une structure optimisée en C.

*   **Avantages** : Ultra-rapide pour des calculs complexes, aggrégations, jointures, et manipulation de tableaux (DataFrames). C'est le standard de l'industrie (Data Science, ML, Analytics).
*   **Inconvénients** : Gourmand en RAM. Si le fichier fait 10 Go, tu as besoin d'au moins 20-30 Go de RAM.

```bash
pip install pandas
```

## 2. Series et DataFrames

Les deux structures fondamentales de Pandas.

*   `Series` : L'équivalent d'une colonne (un tableau 1D typé).
*   `DataFrame` : L'équivalent d'un tableau Excel (plusieurs Series attachées ensemble).

```python
import pandas as pd

# Créer un DataFrame depuis un dictionnaire
data = {
    "player": ["Alice", "Bob", "Charlie", "Diana"],
    "score": [1500, 800, 2100, 1100],
    "is_pro": [True, False, True, False]
}

df = pd.DataFrame(data)

print(df.head()) # Affiche les 5 premières lignes
print(df.info()) # Affiche les types de données et la conso RAM
```

## 3. Lecture et Écriture

`pandas` lit et écrit presque n'importe quoi très facilement en 1 ligne.

```python
# Lecture
df_csv = pd.read_csv("players.csv")
df_json = pd.read_json("data.json")
df_parquet = pd.read_parquet("data.parquet") # Format compressé super rapide (Standard Big Data)
df_sql = pd.read_sql("SELECT * FROM players", con=connexion_db)

# Écriture
df.to_csv("clean_data.csv", index=False)
df.to_parquet("clean_data.parquet")
```

## 4. Exploration et Filtrage

Pandas est magique pour filtrer et nettoyer. Le filtrage (Masques Booléens) peut sembler bizarre au début.

```python
# Sélection de colonnes (retourne une Series)
scores = df["score"]

# Filtrage (Masque Booléen)
# "Garde les lignes du dataframe où la colonne score > 1000"
pros_df = df[df["score"] > 1000]

# Filtres multiples (utiliser & pour AND, | pour OR. Toujours mettre des parenthèses !)
top_amateurs = df[ (df["score"] > 1000) & (df["is_pro"] == False) ]

# Méthodes utiles
print(df["score"].max())  # Score max
print(df["score"].mean()) # Moyenne
print(df["score"].describe()) # Stats basiques (min, max, %iles, etc)
```

## 5. Création et Modification de données

```python
# Ajouter une nouvelle colonne
df["level"] = df["score"] // 100

# Modifier conditionnellement avec np.where (Numpy)
import numpy as np
df["status"] = np.where(df["score"] > 1000, "Veteran", "Noob")

# Remplacer les valeurs manquantes (NaN / Null)
# En Data Science, on déteste les cases vides !
df.fillna({"score": 0, "status": "Unknown"}, inplace=True)

# Supprimer les lignes incomplètes
df.dropna(inplace=True)
```

## 6. Aggrégation (Le fameux `GROUP BY`)

Comme en SQL, l'aggrégation est la clé de l'analyse.

```python
# Stats des joueurs regroupées par status (Veteran / Noob)
# On calcule la moyenne de leurs scores, et le nombre de joueurs ("size")
stats = df.groupby("status").agg(
    avg_score=("score", "mean"),
    max_score=("score", "max"),
    player_count=("player", "count")
)

print(stats)
```

## 7. Jointures (`merge` et `concat`)

*   `concat` : Empile des DataFrames (l'un au dessus de l'autre). (Comme `UNION` en SQL)
*   `merge` : Joint 2 DataFrames horizontalement sur une clé commune. (Comme `JOIN` en SQL)

```python
df1 = pd.DataFrame({"id": [1, 2], "name": ["A", "B"]})
df2 = pd.DataFrame({"id": [3, 4], "name": ["C", "D"]})

# Empiler :
all_users = pd.concat([df1, df2]) 

df_scores = pd.DataFrame({"user_id": [1, 2], "points": [100, 200]})
# Joindre :
merged = pd.merge(df1, df_scores, left_on="id", right_on="user_id", how="left")
```

---

## 🎯 Résumé

| Concept | Ce qu'il faut retenir |
|---------|----------------------|
| **DataFrame** | La structure de base de `pandas` (une table 2D). |
| **`read_csv` / `read_parquet`** | L'intégration de données est magique et rapide. Parquet est le boss du format Data Engineering. |
| **Masques booléens** | `df[ df["col"] > 10 ]` pour filtrer des lignes. (Pas de boucles `for` !) |
| **`.groupby().agg()`** | Le moteur analytique de Pandas (Moyenne, Sum, Count par catégorie). |

> ⚠️ **LA RÈGLE D'OR DE PANDAS** : NE FAIS JAMAIS DE BOUCLES `for row in df:`. 
> Pandas est optimisé en C pour des opérations *vectorisées* sur la colonne entière. Une itération ligne par ligne sera 1000x plus lente !

---

➡️ **Passe aux exercices dans `exercices/` !**
