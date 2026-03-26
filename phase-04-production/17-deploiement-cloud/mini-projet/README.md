# 🚀 Mini-Projet : Objectif Production

## Objectif

Prends ton API dockerisée du module 15, et simule un déploiement sécurisé "Production-Ready".

## Mission

1. Modifie ton `Dockerfile` (dans le Stage 2 *Runner*) pour que la ligne de commande finale soit la super commande `gunicorn` avec ses workers et non plus `uvicorn`.

2. Modifie ton `docker-compose.yml` :
   - Fais passer l'API dans un réseau privé (ex: `backend-net`) et retire ses `ports:` exposés publiquement.
   - Ajoute un service `reverse-proxy` basé sur l'image `caddy:2-alpine`.
   - Ce service caddy doit exposer les ports `80` et `443`.

3. Crée un fichier `Caddyfile` très simple qui redirige ton DNS local (ou `localhost`) vers le service interne de l'api.

## Pourquoi ce projet est important ?

C'est EXACTEMENT l'architecture que tu déploierais sur un vrai serveur Linux.
Avec cette config, ton API FastAPI est cachée derrière un serveur robuste (Caddy) et utilise toute la puissance CPU de la machine (Gunicorn).

## Critères de réussite ✅

- [ ] Lancer `docker-compose up --build -d` lance la BDD, l'API et Caddy.
- [ ] Tu peux accéder à `http://localhost/docs` (C'est Caddy qui répond sur le port 80 et redirige vers l'API en interne).
- [ ] Dans les logs `docker logs [nom_du_container_api]`, tu vois que Gunicorn a bien "booté" plusieurs workers.
