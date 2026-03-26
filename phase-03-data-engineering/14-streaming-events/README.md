# Module 14 — Streaming et Event Processing 🌊

> **Objectif** : Comprendre les architectures Event-Driven modernes, Apache Kafka (les concepts) et Pub/Sub. C'est le cœur du Data Engineering en temps réel.

## 1. Batch vs Streaming

En Data Engineering, il y a deux écoles principales :

*   **Batch (Module 12)** : On traite les données par blocs. Par exemple, tous les soirs à minuit (cron job), on lit les logs de la journée, on les transforme, et on les sauve. *(Lent, mais très résilient et simple).*
*   **Streaming (Module 14)** : On traite la donnée **au moment où elle est générée**. Dès qu'un joueur clique sur "Acheter", l'événement circule dans l'infrastructure en quelques millisecondes. *(Complexe, mais ultra-réactif).*

## 2. Pub / Sub (Publish - Subscribe)

Le pattern principal du streaming est le **Pub/Sub**.

*   **Publisher (Producteur)** : Celui qui crée la donnée (ex: Le serveur de jeu, le frontend).
*   **Topic / Queue** : Le canal de communication (ex: Kafka, Redis Pub/Sub, RabbitMQ).
*   **Subscriber (Consommateur)** : Celui qui lit l'événement en temps réel (ex: Le service Analytics, le service Anticheat).

> **En Node**, tu ferais ça avec EventEmitter. En Python, ça s'implémente au niveau de l'infrastructure, mais on peut le concevoir en asynchrone pour simuler le comportement.

## 3. Simuler du Streaming en Python (Générateurs + Async)

Pour traiter du vrai "streaming", ta fonction ne "retourne" jamais une liste complète. Elle lit un flux infini.

```python
import asyncio
import random

# Simulation d'un "Topic" Kafka infini
async def event_stream_simulator():
    """Génère un flux d'événements infini (comme un vrai flux Kafka)."""
    while True: # Boucle infinie !
        yield {"user": f"Player{random.randint(1,10)}", "event": "click"}
        await asyncio.sleep(0.5) # Un event toutes les 0.5s

# Simulation d'un Consommateur (Subscriber)
async def process_stream():
    """Consomme le flux infini sans jamais planter."""
    async for event in event_stream_simulator():
        print(f"⚡ Processing real-time event: {event}")
        # ICI: Envoyer à Prometheus, Redis, etc.
```

## 4. Kafka / RabbitMQ : Les vrais outils (Concept)

Dans un environnement réel, tu n'utilises pas une file d'attente en RAM avec `asyncio.Queue`, car si le script crashe, tu perds toutes les données en attente.

Tu utilises un Message Broker (ex: **Redis**, **RabbitMQ**, ou **Apache Kafka**).

### Exemple d'architecture Kafka (Theoric)

1.  **Topic** : `game.player.movements`
2.  Le serveur FastAPI (Producer) envoie 10 000 JSON par seconde dans ce Topic.
3.  Kafka stocke ces messages sur disque de façon ultra performante.
4.  Consommateur A (Python) lit le Topic et met à jour la minimap en temps réel.
5.  Consommateur B (Python) lit le MÊME Topic et détecte les tricheurs (SpeedHack).

### Exemple minimaliste avec Redis (Concept)

```python
# Exemple purement théorique (nécessite pip install redis)
import aioredis

async def publisher(redis):
    # Envoie dans le canal "game_chat"
    await redis.publish("game_chat", "Hello World!")

async def subscriber(redis):
    # Écoute le canal "game_chat"
    pubsub = redis.pubsub()
    await pubsub.subscribe("game_chat")
    async for message in pubsub.listen():
        print(f"Message reçu : {message}")
```

## 5. Fenêtres temporelles (Windowing)

Le plus dur en streaming, c'est l'aggrégation globale.
En Batch (Pandas), on a tout le fichier, on fait `.mean()`.
En Streaming, on a un flux infini. Comment faire la moyenne ?

**Solution : Windowing (Les fenêtres).**
On aggrège par paquets de temps (ex: "Combien d'événements ces 10 dernières secondes ?").

```python
import time
from collections import defaultdict

class TumblingWindowMetrics:
    def __init__(self, window_size_seconds=10):
        self.window_size = window_size_seconds
        self.metrics = defaultdict(int)
        self.window_start = time.time()
        
    def add_event(self, event_type):
        now = time.time()
        # Si on a dépassé la fenêtre (ex: 10 sc écoulées), 
        # On affiche le résultat et on RESET.
        if now - self.window_start >= self.window_size:
            self.flush()
            
        self.metrics[event_type] += 1
        
    def flush(self):
        print(f"📊 [WINDOW] Result for last {self.window_size}s: {dict(self.metrics)}")
        # Reset de la fenêtre
        self.metrics.clear()
        self.window_start = time.time()
```

## 6. L'Architecture Lambda / Kappa

Deux mots que tu vas souvent entendre en entretien Data.

*   **Lambda Architecture** : Avoir un pipeline Batch (précis et lourd, calculé la nuit) + un pipeline Streaming (rapide mais potentiellement imprécis, en temps réel) et "fusionner" les résultats pour le client.
*   **Kappa Architecture** : Utiliser *uniquement* le Streaming. (Kafka gère tout).

---

## 🎯 Résumé

| Concept | Explication |
|---------|-------------|
| **Streaming** | Traitement continu (en temps réel) de flux de données infinis. |
| **Pub/Sub** | Pattern (Publish/Subscribe) pour découpler la production de la consommation. |
| **Message Broker** | Kafka, RabbitMQ, Redis. Ils gèrent la persistance des files d'attente. |
| **Windowing** | Aggréger les données du flux infini par tranches de temps (ex: toutes les 5 secondes). |

> **Transition** : Le streaming asynchrone boucle la boucle de notre Phase 3 "Data Engineering". Mêler les tâches `asyncio`, les queues, et le streaming est ce qui distingue un Junior d'un Boss.

---

➡️ **Passe aux exercices pour construire un Mini-Moteur de Streaming en RAM !**
