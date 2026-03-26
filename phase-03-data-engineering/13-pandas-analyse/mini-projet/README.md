# 🏆 Mini-Projet : Data Scientist RPG

## Objectif

Tu viens de récupérer un énorme dump d'une base de données de MMORPG (format CSV). Il contient l'or des joueurs, leur classe, leur niveau, et leur activité récente. 

Ta mission : Construire un Dashboard de l'économie du jeu en utilisant `pandas`.

## Les fichiers

Tu devras simuler 2 fichiers ou générer les DataFrames directement dans le code :
1. `players.csv` : `player_id, name, class, level, gold`
2. `transactions.csv` : `transaction_id, player_id, amount, item_type`

## Analyses à réaliser ✅

- [ ] Join : Regrouper les joueurs avec leurs transactions.
- [ ] Nettoyage : Certains joueurs ont des niveaux négatifs (tricheurs), filtre-les.
- [ ] GroupBy 1 : Quelle classe est la plus riche en moyenne ? (Moyenne de l'or par classe).
- [ ] Mappe : Ajoute une colonne "Whale" (True si un joueur a plus de 100_000 gold, False sinon).
- [ ] Analyse : Quel `item_type` génère le plus gros volume financier total (`sum` de `amount`) ?
- [ ] (Optionnel) Sortie : Exporte le résultat des Whale (les joueurs > 100k) dans un fichier `whales_report.csv`.
