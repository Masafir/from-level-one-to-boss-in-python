# Module 17 — Exercice à trou #1
# 🎯 Thème : La commande ultime de production (Gunicorn)
#
# FastAPI est génial, mais `uvicorn` en solo n'utilise qu'un seul cœur CPU.
# Complète ce petit script bash (ou cette ligne CMD de Dockerfile) 
# pour lancer une API avec la puissance de Gunicorn orchestrant Uvicorn.

# Supposons que ton app s'appelle `app` dans le fichier `src/main.py`
# et que ton serveur VPS a 4 cœurs (donc on veut 4*2 + 1 = 9 workers)

# ==========================================
# LA COMMANDE DE DÉPLOIEMENT
# ==========================================

___ \                                 # 1. Quel est l'outil principal (le Process Manager WSGI) ?
    src.main:___ \                    # 2. Quel est le nom de l'instance FastAPI dans main.py ?
    -w ___ \                          # 3. Combien de workers pour 4 coeurs CPU ? (Formule: Coeurs*2 + 1)
    -k ___.workers.UvicornWorker \    # 4. Quelle est la classe de worker qui permet l'Asynchrone (ASGI) ?
    --bind 0.0.0.0:___                # 5. Sur quel port interne on écoute généralement l'API ? (ex: 8000)

# Pourquoi c'est important ?
# Si ton API a 1000 connexions simultanées, un seul process plantera.
# Avec 9 workers gérés par le manager, ils se répartissent la charge 
# et si l'un crash, le manager en relance un instantanément.
