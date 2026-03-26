# Module 15 — Docker & Conteneurisation Python 🐳

> **Objectif** : Packager tes applications Python pour qu'elles tournent de la même manière partout (sur ton mac, et sur les serveurs de production).

## 1. Pourquoi Docker avec Python ?

En Node.js, tu as `package.json` et `node_modules/`.
En Python, tu as `requirements.txt` (ou `pyproject.toml`) et les environnements virtuels (`venv`).

Le problème, c'est que certaines librairies Python (comme `numpy`, `psycopg2` pour PostgreSQL, ou `cryptography`) compilent du code en C. Si tu compiles sur un Mac (ARM) et que tu déploies sur un serveur Linux (x86), **ça va crasher**.

Docker résout ça : on package l'application ET l'OS de base.

## 2. Le `Dockerfile` Python Ultime (Best Practice)

Voici le standard de l'industrie pour créer une image Python : **Multi-stage build pour alléger l'image et la sécuriser**.

Crée un fichier nommé `Dockerfile` (sans extension) :

```dockerfile
# ==========================================
# STAGE 1 : Builder (On compile les dépendances)
# ==========================================
FROM python:3.12-slim as builder

# Définir le répertoire de travail
WORKDIR /app

# Ne pas écrire les .pyc (fichiers caches Python) sur disque
ENV PYTHONDONTWRITEBYTECODE=1
# Ne pas bufferiser stderr/stdout (les logs s'affichent instantanément)
ENV PYTHONUNBUFFERED=1

# Installer des outils systèmes nécessaires pour compiler (ex: postgresql, gcc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Créer un environnement virtuel
RUN python -m venv /opt/venv
# Activer le venv pour les prochaines commandes
ENV PATH="/opt/venv/bin:$PATH"

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances dans le venv
RUN pip install --no-cache-dir -r requirements.txt


# ==========================================
# STAGE 2 : Runner (Image finale de Prod)
# ==========================================
FROM python:3.12-slim as runner

WORKDIR /app

# Récupérer l'environnement virtuel du Stage 1 (sans les outils de build !)
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Créer un utilisateur non-root par sécurité
RUN useradd -m -r appuser && chown -R appuser /app
USER appuser

# Copier le code (en ignorant local venv grâce au .dockerignore)
COPY src/ ./src/

# Exposer le port (si API web)
EXPOSE 8000

# Commande de lancement (ex: serveur FastAPI)
# En prod, on ne fait JAMAIS "fastapi dev", on utilise Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 3. Le fichier `.dockerignore`

AUSSI IMPORTANT QUE `.gitignore`. Si tu copies ton dossier `venv/` Mac dans l'image Linux, ça plantera.

Crée un fichier `.dockerignore` :
```text
.git
.venv
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.pytest_cache/
```

## 4. Commandes de Base Docker

```bash
# Construire l'image (le "." à la fin indique le dossier courant)
docker build -t my-python-api:latest .

# Lancer le conteneur (--rm pour le supprimer à l'arrêt, -p pour mapper les ports)
docker run --rm -p 8000:8000 my-python-api:latest

# Lancer en background (-d pour detach)
docker run -d --name game-api -p 8000:8000 my-python-api:latest

# Voir les logs
docker logs -f game-api
```

## 5. Docker Compose pour l'écosystème

Ton API a souvent besoin d'une Base de Données (PostgreSQL) et éventuellement d'un Message Broker (Redis). `docker-compose.yml` orchestre tout ça, exactement comme en Node.js.

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      # L'URL pings service "db" via le réseau interne Docker
      - DATABASE_URL=postgresql+psycopg2://user:password@db:5432/game_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
    networks:
      - game-network

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=game_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d game_db"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - game-network

  redis:
    image: redis:7-alpine
    networks:
      - game-network

volumes:
  postgres_data:

networks:
  game-network:
```

```bash
# Tout lancer
docker-compose up -d

# Tout couper
docker-compose down
```

## 6. Variables d'Environnement en Python

```python
import os
# Préférer `pydantic-settings` ou `python-dotenv` en dev, 
# mais en prod avec docker-compose, os.getenv fait le job :

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db") # fallback si absent
```

---

## 🎯 Résumé

| Concept | Ce qu'il faut retenir |
|---------|----------------------|
| **Multi-stage build** | Un `builder` pour installer (avec compilateurs), un `runner` pour exécuter (léger). |
| **`PYTHONUNBUFFERED=1`** | OBLIGATOIRE dans un Dockerfile Python pour voir les print() dans `docker logs`. |
| **`.dockerignore`** | OBLIGATOIRE. N'inclus jamais ton environnement virtuel `venv` local dans le build. |
| **`CMD ["uvicorn"...]`** | Le point d'entrée exécutable (pas `python run.py`, pas `fastapi dev`). |
| **`docker-compose`** | Parfait pour simuler l'environnement de Prod (API + Postgres + Redis). |

---

➡️ **Passe aux exercices pour construire ton premier conteneur !**
