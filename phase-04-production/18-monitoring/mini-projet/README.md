# 🔭 Mini-Projet : Observabilité Totale

## Objectif

Met en place un système de Logging professionnel et une mesure de performance (Metrics) dans une API simulée.

## Mission

1. **Remplacement des `print()`**. 
   - Crée un fichier `main.py` avec une route FastAPI "/play" qui simule une action de jeu très lente (utilise `time.sleep()`).
   - Configure globalement `logging` et un objet `logger = logging.getLogger(...)`.
   - Lance l'API avec Uvicorn et vérifie que ça affiche bien tes logs. (Niv INFO).

2. **Instrumenter Prometheus**.
   - Dans ce même fichier `main.py`, installe `prometheus-fastapi-instrumentator`.
   - Ajoute les 2 lignes magiques pour exposer le end-point `/metrics`.
   
3. **Tester comme un DevOps**.
   - Fais quelques requêtes `GET /play`.
   - Fais une requête `GET /metrics`.
   - Tu devrais voir un gros texte effrayant généré par Prometheus, avec le compte exact du nombre de requêtes HTTP entrantes envoyées vers ton API et la latence moyenne de tes routes de jeu !

## Critères de réussite ✅

- [ ] L'API boot.
- [ ] Tu as un beau message de log standardisé à l'appel de tes fonctions.
- [ ] Les métriques Prometheus sont disponibles sur `/metrics` de manière transparente.
