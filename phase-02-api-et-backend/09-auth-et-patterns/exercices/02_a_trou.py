"""
Module 09 — Exercice à trou #2
🎯 Thème : Async patterns et Event Bus

Complète les ___ pour que le code fonctionne.
Exécute avec : python 02_a_trou.py
"""

import asyncio
from collections import defaultdict
from typing import Callable, Any
from dataclasses import dataclass, field

# ============================================================
# PARTIE 1 : Async basics
# ============================================================

___ def fetch_player(player_id: int) -> dict:  # Quel mot-clé avant def ?
    """Simule la récupération d'un joueur depuis une API."""
    ___ asyncio.sleep(0.05)  # Quel mot-clé pour attendre ?
    return {"id": player_id, "name": f"Player_{player_id}"}


async def fetch_all_players(ids: list[int]) -> list[dict]:
    """Récupère tous les joueurs en parallèle (comme Promise.all)."""
    tasks = [fetch_player(pid) for pid in ids]
    results = await asyncio.___(  *tasks)  # Quelle fonction pour exécuter en parallèle ?
    return list(results)


# ============================================================
# PARTIE 2 : Event Bus
# ============================================================

class EventBus:
    """Bus d'événements async (comme EventEmitter en Node)."""
    
    def __init__(self):
        self._handlers: dict[str, list[Callable]] = ___(list)  # Quel type de dict ?
        self._history: list[dict] = []
    
    def on(self, event: str, handler: Callable) -> None:
        """Enregistre un handler pour un événement."""
        self._handlers[event].___(handler)  # Quelle méthode de liste ?
    
    def off(self, event: str, handler: Callable) -> None:
        """Désenregistre un handler."""
        if handler in self._handlers[event]:
            self._handlers[event].remove(handler)
    
    async def emit(self, event: str, data: dict | None = None) -> None:
        """Émet un événement et appelle tous les handlers."""
        self._history.append({"event": event, "data": data})
        
        for handler in self._handlers[event]:
            if asyncio.iscoroutinefunction(handler):
                ___ handler(data or {})  # Comment appeler un handler async ?
            else:
                handler(data or {})
    
    def get_history(self, event: str | None = None) -> list[dict]:
        if event is None:
            return self._history
        return [e for e in self._history if e["event"] == event]


# ============================================================
# PARTIE 3 : Rate Limiter async
# ============================================================

@dataclass
class RateLimiter:
    """Limite le nombre de requêtes par utilisateur."""
    max_requests: int = 10
    window_seconds: float = 60.0
    _requests: dict[str, list[float]] = field(default_factory=lambda: defaultdict(list))
    
    async def check(self, user_id: str) -> bool:
        """
        Vérifie si l'utilisateur peut faire une requête.
        Retourne True si OK, False si rate limited.
        """
        import time
        now = time.time()
        
        # Nettoyer les vieilles entrées
        self._requests[user_id] = [
            t for t in self._requests[user_id]
            if now - t < self.___  # Quel attribut pour la fenêtre ?
        ]
        
        # Vérifier la limite
        if ___(self._requests[user_id]) >= self.max_requests:  # Quelle built-in ?
            return False
        
        self._requests[user_id].append(now)
        return ___  # Quelle valeur de retour si OK ?
    
    def get_remaining(self, user_id: str) -> int:
        import time
        now = time.time()
        recent = [t for t in self._requests.get(user_id, []) if now - t < self.window_seconds]
        return max(0, self.max_requests - len(recent))


# ============================================================
# PARTIE 4 : Task Queue
# ============================================================

class TaskQueue:
    """File d'attente de tâches async (comme Bull/BullMQ en Node)."""
    
    def __init__(self, concurrency: int = 3):
        self.concurrency = concurrency
        self._queue: asyncio.___ = asyncio.Queue()  # Quel type de queue async ?
        self._results: list[dict] = []
    
    async def add(self, task_name: str, task_fn: Callable, *args) -> None:
        await self._queue.put({"name": task_name, "fn": task_fn, "args": args})
    
    async def _worker(self, worker_id: int) -> None:
        while True:
            try:
                task = self._queue.get_nowait()
            except asyncio.QueueEmpty:
                break
            
            print(f"  🔧 Worker-{worker_id}: {task['name']}")
            result = await task["fn"](*task["args"])
            self._results.append({"task": task["name"], "result": result})
            self._queue.task_done()
    
    async def process_all(self) -> list[dict]:
        """Lance les workers en parallèle."""
        workers = [self._worker(i) for i in range(self.concurrency)]
        await asyncio.gather(*workers)
        return self._results


# ============================================================
# MAIN — Tests async
# ============================================================

async def main():
    print("🎮 Test Async Patterns\n")
    
    # Test 1 : Fetch parallèle
    print("--- Fetch parallèle ---")
    players = await fetch_all_players([1, 2, 3, 4, 5])
    print(f"  Got {len(players)} players: {[p['name'] for p in players]}")
    
    # Test 2 : Event Bus
    print("\n--- Event Bus ---")
    bus = EventBus()
    events_log = []
    
    def on_score(data): events_log.append(f"score: {data}")
    async def on_levelup(data): events_log.append(f"levelup: {data}")
    
    bus.on("score_submitted", on_score)
    bus.on("level_up", on_levelup)
    
    await bus.emit("score_submitted", {"player": "Alice", "score": 15000})
    await bus.emit("level_up", {"player": "Alice", "new_level": 42})
    print(f"  Events: {events_log}")
    print(f"  History: {len(bus.get_history())} events")
    
    # Test 3 : Rate Limiter
    print("\n--- Rate Limiter ---")
    limiter = RateLimiter(max_requests=3, window_seconds=1.0)
    for i in range(5):
        allowed = await limiter.check("alice")
        remaining = limiter.get_remaining("alice")
        print(f"  Request {i+1}: {'✅' if allowed else '❌'} (remaining: {remaining})")
    
    # Test 4 : Task Queue
    print("\n--- Task Queue ---")
    queue = TaskQueue(concurrency=2)
    
    async def process_score(name: str, score: int) -> dict:
        await asyncio.sleep(0.01)
        return {"player": name, "processed_score": score * 2}
    
    for name, score in [("Alice", 100), ("Bob", 200), ("Charlie", 300), ("Diana", 400)]:
        await queue.add(f"process_{name}", process_score, name, score)
    
    results = await queue.process_all()
    for r in results:
        print(f"  {r['task']}: {r['result']}")
    
    print("\n✅ Exercice terminé avec succès !")


if __name__ == "__main__":
    asyncio.run(main())
