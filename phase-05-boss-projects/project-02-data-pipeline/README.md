# 👑 Boss Project 2 : "RiotWatcher" (The Data Pipeline MVP)

> **Technologies** : Python (Requests/Httpx), Pandas, SQLite, Streamlit (ou Dash/React), cron/task scheduling.
> **Objectif** : Shiper un vrai Dashboard Data Analytics sur ton VPS basé sur des données réelles récupérées via l'API officielle de Riot Games (League of Legends).

## Le Produit : RiotWatcher Analytics

Tu vas construire une plateforme de monitoring personnel (ou pour l'eSport). Ton script Python va régulièrement récupérer l'historique de matchs de toi-même ou de joueurs Pro, nettoyer cette data, la stocker, et un Frontend va afficher tes statistiques d'évolution sous forme de de Dashboard interactif.

## Fonctionnalités (Real World MVP)

### 1. Extraction Automatisée (Le Worker Python)
- **API Riot Games** : Inscris-toi sur le portail dev de Riot et crée une clé API.
- Laisse tourner un script Python (via `crontab` Linux ou `Celery` ou juste un worker `asyncio` bouclé) sur ton VPS.
- Ce script tire toutes les heures (ou jours) les 10 derniers matchs de plusieurs Invocateurs ciblés.
- Les données brutes JSON (qui sont immenses) sont "aplaties" et extraites (Yield / Générateurs).

### 2. Transformation & Chargement (Le "T" et le "L")
- **Pandas** : Le worker nettoie les données et extrait précisément : La durée de la partie, l'or accumulé, la vision, l'issue (Win/Loss), le champion joué.
- Stockage batch des matchs uniques (Idempotence) dans une base de données **SQLite** (Super légère et parfaite pour ce genre d'Analytics personnel).

### 3. Le Dashboard Frontend (Streamlit)
Tu n'as pas envie de refaire du React complet juste pour de la Data ?
- Utilise **Streamlit** (librairie Python magique pour la Data).
- Tu écris tout en Python : Streamlit génère le Frontend (Graphiques interactifs, Tableaux, Sélecteurs).
- Connecte Streamlit à ta base SQLite pour afficher :
  - Un Graphique d'évolution du Gold/Minute au fil des jours.
  - Taux de victoire par Champion avec une Datatable triable.
  - Heatmap ou Histogramme des durées de match.

## Architecture de Déploiement (Sur ton VPS)

- **Worker Conteneur** : Un conteneur Docker "headless" qui lance juste la boucle python toutes les X heures pour fetch l'API Riot.
- **SQLite Volume** : Un volume Docker partagé `shared_data` contenant `analytics.db`.
- **Streamlit Conteneur** : Un conteneur Docker exposant le port 8501 qui lit le même fichier `analytics.db`.
- **Caddy/Nginx** : Redirige `stats.ton-domaine.com` vers le port 8501 de Streamlit avec HTTPS automatique.

## Le Défi Boss 🌟

La limitation drastique des clés API de développement chez Riot (Rate Limit : ex. 100 req / 2 min). Ton worker *doit* gérer le `HTTP 429 Too Many Requests`. Tu devras implémenter un "Exponential Backoff" ou un "Retry Mechanism" propre dans ton script d'extraction (`httpx` + `tenacity`).
