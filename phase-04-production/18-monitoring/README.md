# Module 18 — Monitoring & Observabilité 🔭

> **Objectif** : Ton application est en production. Comment savoir si elle fonctionne bien ? Comment être alerté s'il y a un bug avant que les joueurs ne s'en plaignent sur Twitter ?

## 1. Pourquoi le `print()` ne suffit plus ?

En développement (Phase 1, 2, 3), tu utilisais `print("Le joueur s'est connecté")`.
En production, cette approche pose plusieurs problèmes :
1. Où vont les prints ? (Dans la console Docker, mais si le serveur redémarre, tout est perdu).
2. Impossible de chercher un print précis ("Quand est-ce que Joe a acheté cette épée ?").
3. Impossible de filtrer par gravité (INFO, WARNING, ERROR, CRITICAL).

**La solution : Le module `logging` de Python (ou la librairie moderne `loguru`).**

## 2. Le standard : Le module `logging` (intégré)

```python
import logging

# 1. Configuration (À faire une seule fois au démarrage de l'app)
# En Prod, on écrit souvent au format JSON pour que des outils externes puissent lire les logs
logging.basicConfig(
    level=logging.INFO, # Niveau minimum affiché (Ignore les logs DEBUG)
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(), # Affiche dans la console (pour docker logs)
        # logging.FileHandler("app.log") # Optionnel : écrire dans un fichier
    ]
)

# 2. Utilisation
logger = logging.getLogger(__name__)

def pay_item(user, amount):
    logger.debug("Début de la fonction de paiement.") # Caché en prod
    if amount < 0:
        logger.warning(f"Tentative de paiement frauduleux par {user}.")
        
    try:
        # Code sensible...
        1/0
        logger.info(f"{user} a payé {amount}$.")
    except Exception as e:
        logger.error("Le paiement a explosé !", exc_info=True) # exc_info capture la Stack Trace entière!
```

## 3. Sentry (Tracking d'Exceptions)

Le fichier de logs, c'est bien. Mais si l'API crashe à 3h du matin, tu ne lis pas le fichier log. 
C'est là qu'interviennent les outils d'APM (Application Performance Monitoring) / Tracking d'Erreurs. 

**Le boss final : SENTRY**.

Sentry capture automatiquement chaque exception non gérée, t'envoie une alerte Slack/Email, et te montre la ligne exacte du crash avec les variables locales lors du plantage !

```python
# pip install sentry-sdk
import sentry_sdk
from fastapi import FastAPI

# Initialisation magique (Lis le DSN depuis les variables d'environnement)
sentry_sdk.init(
    dsn="https://<cle_sentry>@o12345.ingest.sentry.io/12345",
    
    # Capture 100% des erreurs, et 20% des traces de performances (vitesse des requêtes)
    traces_sample_rate=0.2,
    
    # Pour savoir dans quel environnement l'erreur est survenue
    environment="production"
)

app = FastAPI()

@app.get("/crash-test")
def trigger_error():
    # Ça va crasher : FastAPI renvoie une Erreur 500,
    # ET ça part immédiatement dans l'interface web de Sentry !
    division_by_zero = 1 / 0
    return {"message": "You will never see this"}
```

## 4. Métriques et Prometheus

Les logs racontent **l'histoire**. (ex: "Connexion échouée à 12h01").
Les métriques donnent la **santé globale**. (ex: "Nombre de CPU utilisés : 85%", "RPS (Requêtes Par Seconde) : 2500").

L'écosystème roi est **Prometheus + Grafana**.
Prometheus "scrappe" (lit) périodiquement un endpoint `/metrics` de ton API.
Grafana lit Prometheus et dessine des graphiques magnifiques.

**Exemple d'intégration FastAPI :**
```python
# pip install prometheus-fastapi-instrumentator
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# 1 ligne de code = API monitorée.
# Prometheus pourra venir lire http://ton-api/metrics toutes les 15 secondes
Instrumentator().instrument(app).expose(app)
```

## 5. Le triptyque de l'Observabilité Moderne

1.  **LOGS (ELK Stack, Datadog, Loki)** : Pour le débogage précis. (Python `logging`).
2.  **TRACES / ERRORS (Sentry)** : Pour être alerté des crashs avec le contexte du code.
3.  **METRICS (Prometheus/Grafana)** : Pour les tableaux de bord et les alertes d'usage CPU/RAM/Trafic.

---

## 🎯 Résumé

| Concept | Équivalent ou Utilité |
|---------|-------------|
| **`logging`** | Remplace `console.log()` et `print()`. Gère les niveaux de criticité (INFO, WARN, ERROR). |
| **Sentry** | Envoie le crash-report au développeur (Slack/Email) avec le contexte des variables. |
| **Prometheus** | Scraping de la santé de l'API (Métriques). |
| **Grafana** | Visualisation des données de Prometheus (Les Dashboards DevOps). |

---

➡️ **Passe aux exercices pour implémenter de vrais logs et Sentry !**
