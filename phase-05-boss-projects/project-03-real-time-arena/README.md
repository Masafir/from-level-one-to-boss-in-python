# 👑 Boss Project 3 : "Clicker Arena" (Real-Time Multiplayer Web Game MVP)

> **Technologies** : FastAPI WebSockets, Asyncio, Redis Pub/Sub, React/VueJS, Canvas/DOM.
> **Objectif** : Shiper un vrai jeu web multijoueur synchrone où l'action des joueurs a un impact immédiat sur tous les autres. Le sommet de la réactivité Backend.

## Le Produit : Clicker Arena

Un jeu web social. L'URL pointe vers une arène unique en monde persistant. 
Au centre : Un Boss Titanesque avec 1 Million d'HP.
N'importe quel joueur qui ouvre la page voit le boss évoluer en temps réel et les autres joueurs présents (sous forme de pointeurs ou de compteurs). Chaque clic sur le boss lui fait perdre 1 HP. Des capacités spéciales infligent plus de dégâts. Le premier à tuer le Boss gange. Toutes les 5 minutes, le Boss regagne de la vie (Tick Serveur).

## Fonctionnalités (Real World MVP)

### 1. Le Backend Streaming (Le Moteur de Jeu)
- **Point d'Entrée WebSockets** : Une route FastAPI `/ws` accepte les connexions entrantes des navigateurs.
- **Redis State Manager** : L'état global du Boss (HP actuels, Etat) n'est pas stocké dans une variable en RAM Python (car ça casserait avec de multiples workers Docker), mais dans **Redis**.
- **Serveur de Tick (Game Loop)** : Une `asyncio.Task` infinie tourne en background (ex: gérée par `Celery` ou `RQ` ou juste un worker unique). Elle retire des HP au boss ou gère des "attaques de zone" (ex: Un PNJ).

### 2. L'Event Bus Temps Réel
- Un Front React envoie à FastAPI `{ "action": "hit", "damage": 10 }`.
- FastAPI update l'HP dans Redis et _Publie_ sur un channel Redis `boss_events` : `{ "type": "hp_update", "current_hp": 999990, "user": "Amiralack" }`.
- TOUS les process FastAPI sont abonnés à `boss_events`, reçoivent le msg en 2ms, et le broadcastent au Front via leurs WebSockets respectifs.

### 3. Le Frontend (React/Vanilla)
- **Effets Visuels Locaux** : Le Front dessine le Boss (une simple image) et affiche la barre de HP.
- **Réseau** : WebSocket Event_Listener natif de Javascript (`new WebSocket()`).
- On affiche à droite la "Kill Feed" (Logs) de toutes les attaques des autres joueurs.

## Architecture de Déploiement (Sur ton VPS)

- Un `docker-compose.yml` complet :
  - `redis` : L'épine dorsale de la communication inter-process.
  - `game-api` : L'API FastAPI, scale avec Gunicorn et des UvicornWorkers (`-w 4`). Il est capital d'activer les workers pour prouver que ton système asynchrone via Redis est sans faille.
  - `frontend` : Ton build React exposé.
  - `caddy` / `nginx` : Qui route obligatoirement les websockets. (Attention, router un WebSocket WSS en production nécessite de vérifier que HTTP/1.1 Upgrade est bien configuré sur Nginx/Caddy).

## Le Défi Boss 🌟

Le problème des WebSockets en production c'est la perte de connexion réseau (tunnel TCP qui s'arrête sur mobile). Tu dois coder dans ton Frontend une **reconnexion automatique** (Heartbeat/Ping Pong) de ton JS si le serveur tombe ou la 4G coupe, sans faire planter le state côté serveur. C'est ça qui fait de ton MVP un vrai jeu robuste.
