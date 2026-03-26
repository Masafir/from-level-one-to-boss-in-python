"""Module 11 — Solution exercice à trou #2"""
import asyncio, random
from dataclasses import dataclass, field

async def game_event_producer(queue: asyncio.Queue, n_events: int):
    events = ["kill", "death", "item_pickup", "level_up", "quest_complete"]
    for i in range(n_events):
        await queue.put({"id": i, "type": random.choice(events), "player": f"Player_{random.randint(1,5)}"})
        await asyncio.sleep(0.01)
    await queue.put(None); await queue.put(None)

async def event_consumer(queue: asyncio.Queue, name: str, results: list):
    count = 0
    while True:
        event = await queue.get()
        if event is None: queue.task_done(); break
        results.append({"consumer": name, "event": event}); count += 1; queue.task_done()
    print(f"  📊 {name}: traité {count} événements")

async def process_score(score: dict) -> dict:
    await asyncio.sleep(0.02)
    return {"player": score["player"], "normalized_score": score["value"] / 1000, "rank": "S" if score["value"] > 50000 else "A"}

async def worker_pool(tasks, worker_fn, concurrency=3):
    queue = asyncio.Queue(); results = []
    for t in tasks: await queue.put(t)
    async def worker(wid):
        while not queue.empty():
            try: task = queue.get_nowait()
            except asyncio.QueueEmpty: break
            results.append(await worker_fn(task))
    await asyncio.gather(*[worker(i) for i in range(concurrency)])
    return results

_call_count = 0
async def unreliable_api(success_after=3):
    global _call_count; _call_count += 1
    if _call_count < success_after: raise ConnectionError(f"Server error (attempt {_call_count})")
    return "success!"

async def retry_with_backoff(fn, max_retries=5, base_delay=0.1):
    for attempt in range(max_retries):
        try: return await fn()
        except Exception as e:
            if attempt == max_retries - 1: raise
            delay = base_delay * (2 ** attempt)
            print(f"    ⚠️ Attempt {attempt+1} failed: {e}. Retry in {delay:.2f}s")
            await asyncio.sleep(delay)

async def main():
    print("--- Partie 1 : Producer/Consumer ---")
    queue = asyncio.Queue(maxsize=5); results = []
    await asyncio.gather(game_event_producer(queue, 20), event_consumer(queue, "Analytics", results), event_consumer(queue, "Logger", results))
    print(f"  Total : {len(results)} ✅")

    print("\n--- Partie 2 : Worker Pool ---")
    scores = [{"player": f"P{i}", "value": random.randint(1000, 80000)} for i in range(30)]
    r = await worker_pool(scores, process_score, concurrency=5)
    print(f"  Traités : {len(r)}, S-ranks : {len([x for x in r if x['rank']=='S'])} ✅")

    print("\n--- Partie 3 : Retry ---")
    global _call_count; _call_count = 0
    result = await retry_with_backoff(unreliable_api)
    print(f"  Résultat : {result} (après {_call_count} appels) ✅")
    print("\n✅ Exercice terminé avec succès !")

if __name__ == "__main__": asyncio.run(main())
