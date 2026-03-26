# 🐳 Mini-Projet : Dockerize The Catalog

## Objectif

Reprends le **Game Catalog API** (Module 07 ou Module 10), et dockerise-le entièrement pour la production !

## Mission

1. **Écris un `Dockerfile` multi-stage.**
   - Il doit utiliser `python:3.12-slim`.
   - Il doit avoir un stage builder pour le `venv`.
   - L'image finale doit exécuter l'API via `uvicorn` sous un utilisateur **non-root**.

2. **Écris un `.dockerignore`.**
   - Ton dossier `venv` Mac et les dossiers `__pycache__` ne doivent jamais atterrir dans l'image !

3. **Écris le `docker-compose.yml`.**
   - Ajoute le service API construit via le `Dockerfile`.
   - Ajoute un service PostgreSQL (sur le port 5432).
   - Fais en sorte que l'API attende que la base soit prête (`healthcheck` + `depends_on`).
   - L'API doit se connecter à cette nouvelle base de données Dockerisée et non plus à ta base locale ! (Pense à changer la constante DATABASE_URL).

## Critères de réussite ✅

- [ ] `docker-compose up -d --build` fonctionne du premier coup.
- [ ] Tu peux t'y connecter sur `http://localhost:8000/docs`.
- [ ] Créer un jeu dans l'interface Swagger sauvegarde bien le jeu dans le container PostgreSQL de Docker.
- [ ] Si tu éteins puis rallume avec `down` / `up`, les données sont gardées (Volume).
