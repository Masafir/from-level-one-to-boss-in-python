"""Module 09 — Solution exercice à trou #2"""

import asyncio
from collections import defaultdict
from typing import Callable
from dataclasses import dataclass, field

async def fetch_player(player_id: int) -> dict:
    await asyncio.sleep(0.05)
    return {"id": player_id, "name": f"Player_{player_id}"}

async def fetch_all_players(ids: list[int]) -> list[dict]:
    tasks = [fetch_player(pid) for pid in ids]
    results = await asyncio.gather(*tasks)
    return list(results)

class EventBus:
    def __init__(self):
        self._handlers: dict[str, list[Callable]] = defaultdict(list)
        self._history: list[dict] = []

    def on(self, event: str, handler: Callable) -> None:
        self._handlers[event].append(handler)

    def off(self, event: str, handler: Callable) -> None:
        if handler in self._handlers[event]: self._handlers[event].remove(handler)

    async def emit(self, event: str, data: dict | None = None) -> None:
        self._history.append({"event": event, "data": data})
        for handler in self._handlers[event]:
            if asyncio.iscoroutinefunction(handler): await handler(data or {})
            else: handler(data or {})

    def get_history(self, event: str | None = None) -> list[dict]:
        if event is None: return self._history
        return [e for e in self._history if e["event"] == event]

@dataclass
class RateLimiter:
    max_requests: int = 10
    window_seconds: float = 60.0
    _requests: dict[str, list[float]] = field(default_factory=lambda: defaultdict(list))

    async def check(self, user_id: str) -> bool:
        import time; now = time.time()
        self._requests[user_id] = [t for t in self._requests[user_id] if now - t < self.window_seconds]
        if len(self._requests[user_id]) >= self.max_requests: return False
        self._requests[user_id].append(now); return True

    def get_remaining(self, user_id: str) -> int:
        import time; now = time.time()
        recent = [t for t in self._requests.get(user_id, []) if now - t < self.window_seconds]
        return max(0, self.max_requests - len(recent))

class TaskQueue:
    def __init__(self, concurrency: int = 3):
        self.concurrency = concurrency
        self._queue: asyncio.Queue = asyncio.Queue()
        self._results: list[dict] = []

    async def add(self, task_name: str, task_fn: Callable, *args) -> None:
        await self._queue.put({"name": task_name, "fn": task_fn, "args": args})

    async def _worker(self, worker_id: int) -> None:
        while True:
            try: task = self._queue.get_nowait()
            except asyncio.QueueEmpty: break
            print(f"  🔧 Worker-{worker_id}: {task['name']}")
            result = await task["fn"](*task["args"])
            self._results.append({"task": task["name"], "result": result})
            self._queue.task_done()

    async def process_all(self) -> list[dict]:
        workers = [self._worker(i) for i in range(self.concurrency)]
        await asyncio.gather(*workers); return self._results

async def main():
    print("🎮 Test Async Patterns\n")
    players = await fetch_all_players([1, 2, 3, 4, 5])
    print(f"--- Fetch parallèle ---\n  Got {len(players)} players")

    print("\n--- Event Bus ---")
    bus = EventBus(); events_log = []
    bus.on("score_submitted", lambda d: events_log.append(f"score: {d}"))
    async def on_levelup(data): events_log.append(f"levelup: {data}")
    bus.on("level_up", on_levelup)
    await bus.emit("score_submitted", {"player": "Alice", "score": 15000})
    await bus.emit("level_up", {"player": "Alice", "new_level": 42})
    print(f"  Events: {events_log}")

    print("\n--- Rate Limiter ---")
    limiter = RateLimiter(max_requests=3, window_seconds=1.0)
    for i in range(5):
        ok = await limiter.check("alice")
        print(f"  Request {i+1}: {'✅' if ok else '❌'} (remaining: {limiter.get_remaining('alice')})")

    print("\n--- Task Queue ---")
    queue = TaskQueue(concurrency=2)
    async def process_score(name, score): await asyncio.sleep(0.01); return {"player": name, "score": score * 2}
    for n, s in [("Alice", 100), ("Bob", 200), ("Charlie", 300), ("Diana", 400)]:
        await queue.add(f"process_{n}", process_score, n, s)
    for r in await queue.process_all(): print(f"  {r['task']}: {r['result']}")
    print("\n✅ Exercice terminé avec succès !")

if __name__ == "__main__":
    asyncio.run(main())
