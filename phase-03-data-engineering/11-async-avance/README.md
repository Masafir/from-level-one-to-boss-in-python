# Module 11 — Async Avancé : asyncio, Queues & Workers 🔄

> **Objectif** : Maîtriser la programmation concurrente en Python. L'async en Python c'est plus subtil qu'en Node.js — ici on va au-delà du simple `await`.

## 1. Rappel : Concurrence vs Parallélisme

```
Concurrence (asyncio) :
  Tâche A: ████░░░░████
  Tâche B: ░░░░████░░░░████
  → UN seul thread, on switch quand on attend (I/O)

Parallélisme (multiprocessing) :
  CPU 1: ████████████
  CPU 2: ████████████
  → Plusieurs CPU, calcul simultané

Threading :
  Thread 1: ████░░████░░
  Thread 2: ░░████░░████
  → Plusieurs threads, MAIS le GIL limite le vrai parallélisme
```

### Quand utiliser quoi ?

| Besoin | Outil Python | Équivalent Node |
|--------|-------------|-----------------|
| I/O intensive (HTTP, DB, files) | `asyncio` | Event loop natif |
| CPU intensive (calcul, ML) | `multiprocessing` | Worker threads |
| Mix I/O + simple threading | `threading` | — |
| Tâches en background | `asyncio.Task` | — |
| File d'attente de jobs | `asyncio.Queue` | Bull/BullMQ |

## 2. asyncio en profondeur

### Event Loop

```python
import asyncio

# En Node, la boucle d'événements est implicite
# En Python, tu dois la démarrer explicitement

async def main():
    print("Hello async world!")

# Point d'entrée
asyncio.run(main())  # Crée une event loop + exécute main()

# Accéder à la loop (rarement nécessaire)
loop = asyncio.get_running_loop()
```

### Tasks — Fire & Forget

```python
async def background_job(name: str, delay: float):
    print(f"  🔄 {name} started")
    await asyncio.sleep(delay)
    print(f"  ✅ {name} done")
    return f"{name}_result"

async def main():
    # create_task = lancer une tâche sans attendre
    # (comme un Promise sans await en JS)
    task1 = asyncio.create_task(background_job("Job A", 1))
    task2 = asyncio.create_task(background_job("Job B", 2))
    
    print("Tasks lancées, on continue...")
    
    # Attendre les résultats quand on veut
    result1 = await task1
    result2 = await task2
    print(f"Results: {result1}, {result2}")
```

### gather vs wait vs TaskGroup

```python
# === gather : attendre TOUTES les tâches (comme Promise.all) ===
results = await asyncio.gather(
    fetch_data("url1"),
    fetch_data("url2"),
    fetch_data("url3"),
)  # → [result1, result2, result3]

# Avec gestion d'erreurs
results = await asyncio.gather(
    fetch_data("url1"),
    fetch_data("bad_url"),
    return_exceptions=True,  # Ne pas crasher si une erreur
)  # → [result1, ValueError("...")]

# === wait : attendre avec conditions ===
done, pending = await asyncio.wait(
    [task1, task2, task3],
    return_when=asyncio.FIRST_COMPLETED,  # Dès qu'une finit
    # return_when=asyncio.ALL_COMPLETED,  # Toutes (default)
)
for task in done:
    print(task.result())

# === TaskGroup (Python 3.11+, recommandé) ===
async with asyncio.TaskGroup() as tg:
    task1 = tg.create_task(fetch_data("url1"))
    task2 = tg.create_task(fetch_data("url2"))
# Ici toutes les tâches sont terminées
print(task1.result(), task2.result())
```

### Timeouts

```python
# Timeout sur une opération (comme AbortController en JS)
try:
    result = await asyncio.wait_for(
        slow_operation(),
        timeout=5.0  # Max 5 secondes
    )
except asyncio.TimeoutError:
    print("Timeout ! L'opération a pris trop longtemps")

# Timeout avec TaskGroup (Python 3.11+)
async with asyncio.timeout(10.0):
    await long_operation()
```

## 3. Queues — Files d'attente async

```python
# asyncio.Queue = comme Bull/BullMQ mais intégré

async def producer(queue: asyncio.Queue, n: int):
    """Produit des éléments dans la queue."""
    for i in range(n):
        item = {"id": i, "data": f"item_{i}"}
        await queue.put(item)
        print(f"  📤 Produced: {item['data']}")
    
    # Signal de fin (poison pill)
    await queue.put(None)

async def consumer(queue: asyncio.Queue, name: str):
    """Consomme les éléments de la queue."""
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break  # Poison pill reçu
        
        print(f"  📥 {name} processing: {item['data']}")
        await asyncio.sleep(0.1)  # Simule du travail
        queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=10)  # Buffer de 10
    
    # Lancer producer + consumers en parallèle
    await asyncio.gather(
        producer(queue, 20),
        consumer(queue, "Worker-1"),
        consumer(queue, "Worker-2"),
        consumer(queue, "Worker-3"),
    )
    
    # Attendre que la queue soit vide
    await queue.join()
```

### Priority Queue

```python
# Queue avec priorité (les éléments urgents passent en premier)
queue = asyncio.PriorityQueue()

# (priorité, data) — plus petit = plus prioritaire
await queue.put((1, "🚨 URGENT: server down"))
await queue.put((5, "📝 Log: user login"))
await queue.put((3, "⚠️ Warning: disk 80%"))

while not queue.empty():
    priority, message = await queue.get()
    print(f"  [{priority}] {message}")
# Ordre: URGENT → Warning → Log
```

## 4. Semaphores — Limiter la concurrence

```python
# Limiter le nombre d'opérations simultanées
# (comme un pool de connexions)

semaphore = asyncio.Semaphore(5)  # Max 5 fetch simultanés

async def limited_fetch(url: str):
    async with semaphore:  # Attend si 5 déjà en cours
        print(f"  Fetching {url}")
        await asyncio.sleep(0.5)
        return f"data_from_{url}"

async def main():
    urls = [f"https://api.example.com/data/{i}" for i in range(20)]
    results = await asyncio.gather(*[limited_fetch(url) for url in urls])
    # Max 5 requêtes en même temps, même avec 20 URLs
```

## 5. Worker Pool Pattern

```python
async def worker_pool(
    tasks: list[dict],
    worker_fn,
    concurrency: int = 5,
) -> list:
    """
    Pool de workers async.
    Traite une liste de tâches avec N workers max.
    """
    queue = asyncio.Queue()
    results = []
    
    # Remplir la queue
    for task in tasks:
        await queue.put(task)
    
    async def worker(worker_id: int):
        while True:
            try:
                task = queue.get_nowait()
            except asyncio.QueueEmpty:
                break
            result = await worker_fn(task)
            results.append(result)
            queue.task_done()
    
    # Lancer les workers
    workers = [worker(i) for i in range(concurrency)]
    await asyncio.gather(*workers)
    
    return results

# Utilisation
async def process_game_data(task: dict) -> dict:
    await asyncio.sleep(0.05)
    return {"id": task["id"], "processed": True}

results = await worker_pool(
    tasks=[{"id": i} for i in range(100)],
    worker_fn=process_game_data,
    concurrency=10,
)
```

## 6. Patterns de production

### Retry avec backoff exponentiel

```python
async def retry_with_backoff(
    fn,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
):
    """Retry une opération async avec backoff exponentiel."""
    for attempt in range(max_retries):
        try:
            return await fn()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = min(base_delay * (2 ** attempt), max_delay)
            print(f"  ⚠️ Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
            await asyncio.sleep(delay)
```

### Circuit Breaker

```python
from enum import Enum
from dataclasses import dataclass, field
import time

class CircuitState(Enum):
    CLOSED = "closed"      # Normal, les requêtes passent
    OPEN = "open"          # Erreurs, les requêtes sont bloquées
    HALF_OPEN = "half_open"  # On teste si ça remarche

@dataclass
class CircuitBreaker:
    failure_threshold: int = 5
    recovery_timeout: float = 30.0
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    last_failure_time: float = 0.0
    
    async def call(self, fn, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise RuntimeError("Circuit breaker is OPEN")
        
        try:
            result = await fn(*args, **kwargs)
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise
```

---

## 🎯 Résumé

| Concept | Ce qu'il faut retenir |
|---------|----------------------|
| **asyncio.gather** | Promise.all() — exécuter en parallèle |
| **asyncio.create_task** | Fire & forget — lancer sans attendre |
| **asyncio.Queue** | File d'attente async (producer/consumer) |
| **Semaphore** | Limiter la concurrence (pool de connexions) |
| **TaskGroup** | Python 3.11+, gestion d'erreurs propre |
| **Timeout** | `asyncio.wait_for(coro, timeout=5)` |
| **Worker Pool** | N workers traitent M tâches |

---

➡️ **Passe aux exercices dans `exercices/` !**
