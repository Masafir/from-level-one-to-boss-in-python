"""
Module 11 — Exercice à trou #2
🎯 Thème : Producer/Consumer, Worker Pool, Retry

Complète les ___ pour que le code fonctionne.
Exécute avec : python 02_a_trou.py
"""

import asyncio
import random
from dataclasses import dataclass, field

# ============================================================
# PARTIE 1 : Producer / Consumer
# ============================================================

async def game_event_producer(queue: asyncio.Queue, n_events: int):
    """Produit des événements de jeu."""
    events = ["kill", "death", "item_pickup", "level_up", "quest_complete"]
    for i in range(n_events):
        event = {
            "id": i,
            "type": random.choice(events),
            "player": f"Player_{random.randint(1, 5)}",
        }
        await queue.___(event)  # Quelle méthode pour ajouter ?
        await asyncio.sleep(0.01)
    
    # Poison pills pour arrêter les consumers
    await queue.put(None)
    await queue.put(None)


async def event_consumer(queue: asyncio.Queue, name: str, results: list):
    """Consomme et traite les événements."""
    count = 0
    while True:
        event = ___ queue.get()  # Quel mot-clé pour attendre ?
        
        if event is ___:  # Quel opérateur pour comparer à None ?
            queue.task_done()
            break
        
        results.append({"consumer": name, "event": event})
        count += 1
        queue.___()  # Quelle méthode pour signaler que c'est traité ?
    
    print(f"  📊 {name}: traité {count} événements")


async def part1():
    print("--- Partie 1 : Producer/Consumer ---")
    queue = asyncio.Queue(maxsize=___)  # Quelle taille de buffer ? (5)
    results = []
    
    await asyncio.gather(
        game_event_producer(queue, 20),
        event_consumer(queue, "Analytics", results),
        event_consumer(queue, "Logger", results),
    )
    
    print(f"  Total traité : {len(results)}")
    print("  ✅ OK")


# ============================================================
# PARTIE 2 : Worker Pool
# ============================================================

async def process_score(score: dict) -> dict:
    """Traitement async d'un score."""
    await asyncio.sleep(0.02)
    return {
        "player": score["player"],
        "normalized_score": score["value"] / 1000,
        "rank": "S" if score["value"] > 50000 else "A",
    }


async def worker_pool(tasks: list, worker_fn, concurrency: int = 3) -> list:
    """Pool de workers génériques."""
    queue = asyncio.Queue()
    results = []
    
    for task in tasks:
        await queue.put(task)
    
    async def worker(wid: int):
        while not queue.___():  # Quelle méthode pour vérifier si vide ?
            try:
                task = queue.get_nowait()
            except asyncio.QueueEmpty:
                break
            result = ___ worker_fn(task)  # Quel mot-clé ?
            results.append(result)
    
    workers = [worker(i) for i in range(concurrency)]
    await asyncio.___(*workers)  # Quelle fonction ?
    
    return results


async def part2():
    print("\n--- Partie 2 : Worker Pool ---")
    scores = [
        {"player": f"P{i}", "value": random.randint(1000, 80000)}
        for i in range(30)
    ]
    
    results = await worker_pool(scores, process_score, concurrency=5)
    s_ranks = [r for r in results if r["rank"] == "S"]
    print(f"  Traités : {len(results)}, S-ranks : {len(s_ranks)}")
    print("  ✅ OK")


# ============================================================
# PARTIE 3 : Retry avec backoff
# ============================================================

_call_count = 0

async def unreliable_api(success_after: int = 3) -> str:
    """API qui fail les premières fois."""
    global _call_count
    _call_count += 1
    if _call_count < success_after:
        raise ConnectionError(f"Server error (attempt {_call_count})")
    return "success!"


async def retry_with_backoff(
    fn,
    max_retries: int = 5,
    base_delay: float = 0.1,
) -> any:
    """Retry une fonction async avec backoff exponentiel."""
    for attempt in ___(max_retries):  # Quelle built-in pour itérer N fois ?
        ___:  # Quel bloc pour capturer les erreurs ?
            return await fn()
        except Exception as e:
            if attempt == max_retries - 1:
                raise  # Plus de retries, on propage
            delay = base_delay * (2 ** ___)  # Quelle variable pour le backoff ?
            print(f"    ⚠️ Attempt {attempt + 1} failed: {e}. Retry in {delay:.2f}s")
            await asyncio.sleep(delay)


async def part3():
    print("\n--- Partie 3 : Retry ---")
    global _call_count
    _call_count = 0
    
    result = await retry_with_backoff(unreliable_api)
    print(f"  Résultat : {result} (après {_call_count} appels)")
    print("  ✅ OK")


# ============================================================
# MAIN
# ============================================================

async def main():
    await part1()
    await part2()
    await part3()
    print("\n✅ Exercice terminé avec succès !")

if __name__ == "__main__":
    asyncio.run(main())
