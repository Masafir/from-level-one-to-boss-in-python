"""
Module 11 — Exercice à trou #1
🎯 Thème : asyncio.gather, Tasks, Semaphores

Complète les ___ pour que le code fonctionne.
Exécute avec : python 01_a_trou.py
"""

import asyncio
import time

# ============================================================
# PARTIE 1 : Tasks et gather
# ============================================================

async def fetch_game_data(game_id: int) -> dict:
    """Simule un appel API pour récupérer les données d'un jeu."""
    ___ asyncio.sleep(0.05)  # Quel mot-clé pour attendre un awaitable ?
    return {"id": game_id, "title": f"Game_{game_id}", "score": game_id * 1000}


async def fetch_all_games(ids: list[int]) -> list[dict]:
    """Récupère tous les jeux en parallèle."""
    tasks = [fetch_game_data(gid) for gid in ids]
    results = await asyncio.___(  *tasks)  # Quelle fonction pour Promise.all ?
    return list(results)


async def part1():
    print("--- Partie 1 : gather ---")
    start = time.perf_counter()
    
    games = await fetch_all_games(list(range(1, 21)))
    elapsed = time.perf_counter() - start
    
    print(f"  Récupéré {len(games)} jeux en {elapsed:.2f}s")
    assert len(games) == 20
    assert elapsed < 0.5  # Parallèle, pas séquentiel !
    print("  ✅ OK")


# ============================================================
# PARTIE 2 : Semaphore — limiter la concurrence
# ============================================================

async def api_call(url: str, semaphore: asyncio.Semaphore) -> str:
    """Simule un appel API avec limite de concurrence."""
    ___ ___ semaphore:  # Quel mot-clé + syntaxe pour le context manager async ?
        print(f"    🔄 Fetching {url}")
        await asyncio.sleep(0.1)
        return f"data_from_{url}"


async def part2():
    print("\n--- Partie 2 : Semaphore ---")
    sem = asyncio.___(  3)  # Quel objet pour max 3 simultanés ?
    
    urls = [f"api/{i}" for i in range(10)]
    start = time.perf_counter()
    results = await asyncio.gather(*[api_call(url, sem) for url in urls])
    elapsed = time.perf_counter() - start
    
    print(f"  {len(results)} résultats en {elapsed:.2f}s")
    assert len(results) == 10
    # 10 URLs / 3 concurrent × 0.1s ≈ 0.4s (pas 1s séquentiel)
    assert elapsed < 0.6
    print("  ✅ OK")


# ============================================================
# PARTIE 3 : Timeouts
# ============================================================

async def slow_operation() -> str:
    await asyncio.sleep(10)
    return "done"


async def part3():
    print("\n--- Partie 3 : Timeouts ---")
    
    try:
        result = await asyncio.___(  # Quelle fonction pour timeout ?
            slow_operation(),
            timeout=0.5
        )
    except asyncio.___:  # Quelle exception pour un timeout ?
        print("  ⏰ Timeout capturé !")
    
    print("  ✅ OK")


# ============================================================
# PARTIE 4 : TaskGroup (Python 3.11+)
# ============================================================

async def process_item(item_id: int) -> dict:
    await asyncio.sleep(0.02)
    if item_id == 99:
        raise ValueError(f"Item {item_id} invalide !")
    return {"id": item_id, "status": "processed"}


async def part4():
    print("\n--- Partie 4 : TaskGroup ---")
    
    results = []
    ___ ___ asyncio.TaskGroup() as tg:  # Quel mot-clé + syntaxe ?
        for i in range(5):
            task = tg.create_task(process_item(i))
            results.append(task)
    
    # Ici toutes les tâches sont terminées
    for task in results:
        print(f"  {task.result()}")
    
    print("  ✅ OK")


# ============================================================
# MAIN
# ============================================================

async def main():
    await part1()
    await part2()
    await part3()
    await part4()
    print("\n✅ Exercice terminé avec succès !")


if __name__ == "__main__":
    asyncio.___(main())  # Quelle fonction pour lancer l'event loop ?
