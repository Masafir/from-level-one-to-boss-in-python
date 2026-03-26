# Module 15 — Exercice à trou #1
# 🎯 Thème : Le Dockerfile Multi-Stage parfait
#
# Complète les ___ pour que ce Dockerfile respecte les best practices Python.
# Il packagera une API FastAPI fictive.

# ==========================================
# STAGE 1 : Builder
# ==========================================
FROM python:3.12-slim as ___ # Comment on appelle cette étape ?

WORKDIR /app

# Best Practices d'environnement Python
ENV ___=1 # Ne pas écrire les .pyc
ENV PYTHONUNBUFFERED=1

# Créer un environnement virtuel dans /opt/venv
RUN python -m ___ /opt/venv # Quel module python pour créer un VENV ?
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

# Installer les reqs sans utiliser de cache Docker (pour alléger)
RUN pip install --___ -r requirements.txt # Quel flag pour désactiver le cache HTTP de pip ?


# ==========================================
# STAGE 2 : Runner
# ==========================================
FROM python:3.12-slim as runner

WORKDIR /app

# Récupérer l'environnement virtuel compilé du builder
COPY --from=___ /opt/venv /opt/venv # De quel stage on copie ?
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Création d'un utilisateur non-root pour la sécurité
RUN useradd -m -r appuser && chown -R appuser /app
___ appuser # Quelle commande Docker pour changer d'utilisateur ?

# Copier le code source de l'application
COPY src/ ./src/

# Documenter le port que l'app utilise
___ 8000 # Quel mot-clé Docker pour le port ?

# Commande de démarrage (le tableau de strings)
___ ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"] # Quel mot clé Docker ?
