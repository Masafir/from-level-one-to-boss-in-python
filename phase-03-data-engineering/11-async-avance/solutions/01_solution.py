"""Module 11 — Solution exercice à trou #1"""
import asyncio, time

async def fetch_game_data(game_id: int) -> dict:
    await asyncio.sleep(0.05)
    return {"id": game_id, "title": f"Game_{game_id}", "score": game_id * 1000}

async def fetch_all_games(ids: list[int]) -> list[dict]:
    return list(await asyncio.gather(*[fetch_game_data(gid) for gid in ids]))

async def api_call(url: str, semaphore: asyncio.Semaphore) -> str:
    async with semaphore:
        await asyncio.sleep(0.1)
        return f"data_from_{url}"

async def slow_operation() -> str:
    await asyncio.sleep(10); return "done"

async def process_item(item_id: int) -> dict:
    await asyncio.sleep(0.02)
    return {"id": item_id, "status": "processed"}

async def main():
    print("--- Partie 1 : gather ---")
    start = time.perf_counter()
    games = await fetch_all_games(list(range(1, 21)))
    print(f"  Récupéré {len(games)} jeux en {time.perf_counter()-start:.2f}s ✅")

    print("\n--- Partie 2 : Semaphore ---")
    sem = asyncio.Semaphore(3)
    results = await asyncio.gather(*[api_call(f"api/{i}", sem) for i in range(10)])
    print(f"  {len(results)} résultats ✅")

    print("\n--- Partie 3 : Timeouts ---")
    try: await asyncio.wait_for(slow_operation(), timeout=0.5)
    except asyncio.TimeoutError: print("  ⏰ Timeout capturé ✅")

    print("\n--- Partie 4 : TaskGroup ---")
    results = []
    async with asyncio.TaskGroup() as tg:
        for i in range(5): results.append(tg.create_task(process_item(i)))
    for t in results: print(f"  {t.result()}")
    print("  ✅ OK")
    print("\n✅ Exercice terminé avec succès !")

if __name__ == "__main__": asyncio.run(main())
