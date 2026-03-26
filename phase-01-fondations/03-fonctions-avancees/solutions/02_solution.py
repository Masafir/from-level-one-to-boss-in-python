"""Module 03 — Solution exercice à trou #2"""

import time
from functools import wraps
from collections import Counter


def cooldown(seconds: float):
    def decorator(func):
        last_called = [0.0]
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < seconds:
                remaining = seconds - elapsed
                print(f"  ⏳ Cooldown ! Attends encore {remaining:.1f}s")
                return None
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator


def count_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        print(f"  📊 {func.__name__} appelée {wrapper.call_count} fois")
        return func(*args, **kwargs)
    wrapper.call_count = 0
    return wrapper


def validate_types(**type_hints):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for param_name, expected_type in type_hints.items():
                if param_name in kwargs:
                    value = kwargs[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"'{param_name}' doit être {expected_type.__name__}, "
                            f"pas {type(value).__name__}"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator


@cooldown(1.0)
@count_calls
def cast_spell(name: str, target: str) -> str:
    return f"✨ {name} lancé sur {target} !"

print("🪄 Test Cooldown + Count:")
print(cast_spell("Fireball", "Goblin"))
print(cast_spell("Ice Bolt", "Orc"))
time.sleep(1.1)
print(cast_spell("Thunder", "Dragon"))

@validate_types(name=str, damage=int)
def create_weapon(name: str, damage: int) -> dict:
    return {"name": name, "damage": damage}

print(f"\n⚔️ {create_weapon(name='Excalibur', damage=100)}")
try:
    create_weapon(name="Sword", damage="fifty")
except TypeError as e:
    print(f"  ❌ {e}")


def dungeon_crawler(rooms: list[dict]):
    for i, room in enumerate(rooms, start=1):
        print(f"  🚪 Salle {i}/{len(rooms)} : {room['name']}")
        if room["enemies"] > 0:
            print(f"     ⚔️ {room['enemies']} ennemis !")
        if room["treasure"]:
            print(f"     💎 Trésor trouvé !")
        yield room


dungeon = [
    {"name": "Entrance Hall", "enemies": 0, "treasure": False},
    {"name": "Dark Corridor", "enemies": 3, "treasure": False},
    {"name": "Treasury", "enemies": 1, "treasure": True},
    {"name": "Boss Room", "enemies": 1, "treasure": True},
]

print("\n🏰 Dungeon Crawl:")
for room in dungeon_crawler(dungeon):
    pass


def fibonacci_xp():
    a, b = 1, 1
    while True:
        yield a * 100
        a, b = b, a + b


print("\n📈 XP Thresholds (Fibonacci):")
xp_gen = fibonacci_xp()
for i in range(8):
    xp = next(xp_gen)
    print(f"  Level {i+2}: {xp} XP requis")


def loot_drop_generator(drop_table: dict[str, float]):
    import random
    items = list(drop_table.keys())
    weights = list(drop_table.values())
    while True:
        drop = random.choices(items, weights=weights, k=1)[0]
        yield drop


print("\n🎁 Loot Drops:")
loot = loot_drop_generator({
    "🗡️ sword": 0.3,
    "🛡️ shield": 0.2,
    "🧪 potion": 0.4,
    "👑 legendary": 0.1,
})

drops = [next(loot) for _ in range(50)]
distribution = Counter(drops)
for item, count in distribution.most_common():
    bar = "█" * count
    print(f"  {item:<20} {bar} ({count})")

print("\n✅ Exercice terminé avec succès !")
