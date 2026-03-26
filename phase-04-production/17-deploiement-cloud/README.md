# Module 17 — Déploiement : Relier Python au Web 🚀

> **Objectif** : Ton code marche sur ton Mac. La CI est au vert. Le conteneur Docker build. Comment on met ça sur internet pour les joueurs ?

## 1. Uvicorn vs Gunicorn (Le cœur du déploiement Python)

Node.js gère son propre serveur HTTP en C++ via libuv. 
Python a besoin d'un **serveur WSGI ou ASGI** pour traduire les requêtes HTTP (qui arrivent d'Internet) en appels de fonctions Python.

*   `WSGI` (Synchrone) : Le standard pour **Django** et Flask. L'outil roi s'appelle **Gunicorn**.
*   `ASGI` (Asynchrone) : Le standard pour **FastAPI**. L'outil roi s'appelle **Uvicorn**.

### Pourquoi Uvicorn NE SUFFIT PAS en Production ?

`uvicorn src.main:app` lance un **seul processus** (worker). Sur un serveur à 8 coeurs, tu gâches 7 coeurs ! De plus, si l'unique processus crash, l'API est down.

**Le standard de l'industrie (Best Practice ultime)** :
On lance **Gunicorn** en tant que "Process Manager", et on lui dit d'utiliser les workers de **Uvicorn** !

```bash
# Dans ton Dockerfile de prod (FastAPI) :
pip install gunicorn uvicorn[standard]

# La ligne de commande magique de production :
# -k ou --worker-class : On dit à Gunicorn d'utiliser Uvicorn pour l'Asynchrone
# -w ou --workers : 4 processus en parallèle (Règle d'or : (Cœurs CPU x 2) + 1)
CMD ["gunicorn", "src.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

## 2. Reverse Proxy (Nginx / Caddy)

Même avec Gunicorn, on ne met jamais Python directement face à l'Internet public (port 80 ou 443).

*Pourquoi ?*
1. La gestion du HTTPS (Certificats SSL) est complexe en Python.
2. Servir des fichiers statiques (images, CSS) est lent en Python.
3. Risque d'attaques DDoS (Slowloris).

**L'architecture classique d'un VPS (Virtual Private Server) :**
```text
[ INTERNET ] ---> [ NGINX (Port 443 HTTPS) ] ---> [ Gunicorn/Uvicorn (Port 8000 interne) ] ---> [ FastAPI / Django ]
```

## 3. Options de Déploiement Modernes

Aujourd'hui, il y a deux écoles selon ton portemonnaie et ton besoin de contrôle.

### École 1 : PaaS (Platform as a Service) - Simple, plus cher
*ex: Render, Railway, Fly.io, Heroku*

Tu leur donnes ton Dockerfile, ils font tout.
**Fichier `render.yaml` (Exemple pour Render.com) :**
```yaml
services:
  - type: web
    name: my-game-api
    env: docker # Il va lire ton Dockerfile automatiquement !
    plan: starter
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: my-postgres-db
          property: connectionString
```

### École 2 : VPS (Virtual Private Server) - Total contrôle, moins cher
*ex: DigitalOcean Droplets, OVH, Hetzner, AWS EC2*

Tu loues une machine Linux nue (Ubuntu) à 5$/mois.
**Comment on déploie dessus ?**
1. Tu installes Docker et Docker Compose.
2. Tu tires ton code (ou ton image depuis le Docker Hub via GitHub Actions).
3. Tu lances `docker-compose up -d`.
4. Tu configures un Nginx en "Reverse Proxy" avec un certificat Let's Encrypt automatique via `certbot`.

*(Astuce de boss : `Caddy Server` remplace `Nginx` + `Certbot` en 3 lignes de configuration, il gère le HTTPS tout seul !)*

## 4. Gérer les variables d'environnement (Secrets)

**RÈGLE D'OR : On ne commit JAMAIS un `.env` sur Git.**

*   **En Local** : Fichier `.env` lu par `pydantic-settings` ou `python-dotenv`.
*   **En PaaS (Railway/Render)** : Tu les rentres dans leur interface web.
*   **Sur un VPS** : Tu crées un fichier `.env.prod` directement sur le serveur, et `docker-compose` va le lire avec `env_file: .env.prod`.

---

## 🎯 Résumé

| Concept | Explication |
|---------|-------------|
| **Uvicorn / Gunicorn** | Les serveurs pour faire tourner Python (Le traducteur HTTP -> Python). |
| **Gunicorn + Uvicorn Workers** | La configuration ultime en Prod pour utiliser tous les coeurs CPU. |
| **Reverse Proxy (Nginx / Caddy)** | Le bouclier face à internet qui gère le HTTPS avant de passer la requête à Python. |
| **PaaS (Railway/Render)** | On donne le repo GitHub, ça déploie. Merveilleux pour commencer. |
| **VPS (DigitalOcean)** | On loue un Linux nu, on installe Docker Compose, on maîtrise tout. |

---

➡️ **Passe aux exercices pour écrire ton script de déploiement ultime !**
