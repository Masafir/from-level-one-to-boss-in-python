# 🚰 Mini-Projet : Data Pipeline de logs de Jeu

## Objectif

Construis un ETL complet en streaming qui lit des logs d'un serveur de jeu, nettoie et enrichit les données, puis les insère dans une base SQLite. Le but est d'éviter les `MemoryError` sur des fichiers énormes.

## Les Données Source

Imagine un fichier CSV `server_logs.csv` de 5 gigaoctets (on va le simuler).

Format :
`timestamp,player_id,action,value`
Ex: `2023-10-01T10:00:00,42,login,SUCCESS`
Ex: `2023-10-01T10:05:00,42,kill,1`
Ex: `2023-10-01T10:15:00,42,death,50` (50 = points perdus)
Ex: `2023-10-01T10:20:00,invalid,NaN,foo`

## Architecture du Pipeline (Streaming)

```
[Extract: csv.reader] 
    ↓ (yield)
[Transform 1: Nettoyage et typage] -> Rejet des lignes invalides (Dead Letter Queue)
    ↓ (yield)
[Transform 2: Enrichissement] -> Ajout d'une colonne "session_date" (YYYY-MM-DD)
    ↓ (yield)
[Load: SQLite Database] -> executemany() par batch de 1000
```

## Critères de réussite ✅

- [ ] L'extraction se fait avec un générateur (yield ligne par ligne).
- [ ] Le typage est robuste (`int(value)`, gestion de dates avec `datetime`).
- [ ] Les lignes invalides sont isolées (écrites dans un `errors.log` par exemple) sans arrêter le script.
- [ ] Les données "propres" ont une nouvelle colonne dérivée du timestamp.
- [ ] Le chargement SQLite utilise des transactions massives de 1000 lignes (`executemany`).
- [ ] Consommation RAM stable.
