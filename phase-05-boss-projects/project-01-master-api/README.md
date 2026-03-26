# 👑 Boss Project 1 : "RetroTracker" (SaaS MVP Fullstack)

> **Technologies** : FastAPI (Python), PostgreSQL, React/Next.js (Front), IGDB API (Real Data), Docker, Sentry, Caddy (HTTPS).
> **Objectif** : Shiper un vrai produit SaaS de Collection de Jeux sur ton VPS avec de vraies métadonnées Twitch/IGDB.

## Le Produit : RetroTracker

Tu vas construire une plateforme web utilisable où les utilisateurs peuvent se créer un compte, chercher de vrais jeux vidéo, et les ajouter à leur collection personnelle avec un statut ("À faire", "En cours", "Terminé", "100%").

## Fonctionnalités (Real World MVP)

### 1. Backend (Le Cerveau Python)
- **Authentification Sécurisée** : Inscription, Connexion, et génération de JWT.
- **Proxy Externe (Real Data)** : Le frontend ne parle jamais à l'API IGDB (Twitch) directement pour ne pas fuiter tes clés API. C'est ton backend FastAPI qui fait les requêtes HTTP (avec `httpx`) vers l'API IGDB pour chercher les jeux, et renvoie le JSON propre à ton Front.
- **Base de Données relationnelle** : 
  - Utilisateurs (`id`, `email`, `password_hash`)
  - User_Games (`user_id`, `game_id_igdb`, `status`, `rating`, `added_at`)
- **Logging & Monitoring** : Intégration de Sentry pour traquer les crashs en production. Logs formatés des requêtes vers l'API de Twitch.

### 2. Frontend (React / Vue / Ce que tu veux)
- **UI Propre** : Une barre de recherche (Debounced) qui tape l'API FastAPI pour afficher les jaquettes (via IGDB) en direct.
- **Dashboard** : La liste des jeux de l'utilisateur avec filtres (ex: "Mes jeux terminés").
- **Design Analytics** : Affiche un petit camembert ou des stats (ex: "Temps de jeu total estimé", "Pourcentage de jeux finis").

## Architecture de Déploiement (Sur ton VPS)

- Tout doit tenir dans un seul `docker-compose.yml`.
- `db` : PostgreSQL.
- `api` : FastAPI géré par Gunicorn (4 workers).
- `front` : L'app React buildée et servie en statique (via Nginx ou un simple Caddy interne).
- `caddy` : Le reverse proxy frontal qui prend le port 80/443, génère les certificats SSL, et redirige `/api` vers FastAPI et le reste vers le Front.

## Le Défi Boss 🌟

La doc de l'API IGDB est dense. Tu vas devoir gérer l'authentification OAuth2 (Client Credentials) côté backend pour obtenir le token Twitch avant de pouvoir requêter les jeux. Ton backend devra mettre ce token en cache (en mémoire ou Redis) pendant 60 jours pour ne pas spammer Twitch à chaque recherche de ton Front.
