"""
Module 11 — Exercice complet #3
🎯 Thème : Système de traitement d'événements de jeu en temps réel

Crée un pipeline async complet qui :
1. Génère des événements de jeu (kills, scores, items)
2. Les route vers différents handlers par type
3. Agrège les stats en temps réel
4. Gère les erreurs et timeouts

Exécute avec : python 03_exercice.py
"""

import asyncio
import random
from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum

# ============================================================
# TYPES D'ÉVÉNEMENTS
# ============================================================

class EventType(str, Enum):
    KILL = "kill"
    DEATH = "death"
    SCORE = "score"
    ITEM_PICKUP = "item_pickup"
    LEVEL_UP = "level_up"
    CHAT = "chat"
    DISCONNECT = "disconnect"


@dataclass
class GameEvent:
    event_type: EventType
    player: str
    data: dict = field(default_factory=dict)
    timestamp: float = 0.0


# ============================================================
# TODO : Implémenter le système
# ============================================================

class EventRouter:
    """
    TODO: Route les événements vers les bons handlers.
    
    - register(event_type, handler_fn) : enregistre un handler
    - route(event) : envoie l'événement au bon handler
    - Supporte plusieurs handlers par event_type
    - Gère les erreurs dans les handlers sans crasher le pipeline
    """
    pass


class StatsAggregator:
    """
    TODO: Agrège les statistiques en temps réel.
    
    - process(event) : met à jour les stats
    - get_stats() : retourne les stats actuelles :
      {
        "total_events": 150,
        "events_by_type": {"kill": 30, "death": 20, ...},
        "events_by_player": {"Alice": 45, "Bob": 35, ...},
        "top_killers": [("Alice", 15), ("Bob", 10)],
        "total_score": 150000,
      }
    """
    pass


class RateLimitedQueue:
    """
    TODO: Queue avec rate limiting.
    
    - put(item) : ajoute un item
    - get() : récupère un item
    - Limite le débit à max_per_second items/seconde
    - Calcule les stats de débit (throughput)
    """
    pass


async def event_generator(queue: asyncio.Queue, n_events: int):
    """
    TODO: Génère des événements de jeu aléatoires.
    
    - Crée n_events événements avec types et joueurs aléatoires
    - Les données varient selon le type (kill → victim, score → value, etc.)
    - Envoie un signal de fin (None × nombre de consumers)
    """
    pass


async def event_processor(
    queue: asyncio.Queue,
    router: "EventRouter",
    stats: "StatsAggregator",
    name: str,
):
    """
    TODO: Consomme les événements et les traite.
    
    - Lit depuis la queue
    - Route via le router
    - Met à jour les stats
    - Gère les timeouts (max 1s par événement)
    - S'arrête sur poison pill (None)
    """
    pass


async def run_pipeline():
    """
    TODO: Orchestre le pipeline complet.
    
    1. Créer la queue, le router, le stats aggregator
    2. Enregistrer les handlers dans le router :
       - KILL → log + stats
       - SCORE → validation + stats
       - LEVEL_UP → notification
    3. Lancer le producer + 3 consumers en parallèle
    4. Afficher les stats finales
    """
    pass


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    asyncio.run(run_pipeline())
    print("\n✅ Pipeline terminé !")
