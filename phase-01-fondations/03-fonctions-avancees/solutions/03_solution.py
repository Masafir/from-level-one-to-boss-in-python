"""Module 03 — Solution exercice complet #3 — RPG Buff System"""

import time
from functools import wraps


def timed_ability(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  ⚡ Using: {func.__name__}")
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  → Result: {result}")
        print(f"  ⏱️ {elapsed:.4f}s")
        return result
    return wrapper


def buff(stat: str, multiplier: float, duration: int = 3):
    def decorator(func):
        uses_left = [duration]

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if uses_left[0] > 0:
                uses_left[0] -= 1
                original = result[stat]
                result[stat] = int(original * multiplier)
                print(f"  💪 Buff active! {stat}: {original} → {result[stat]} "
                      f"(x{multiplier}, {uses_left[0]} uses left)")
            else:
                print(f"  💨 Buff expired on {stat}")
            return result
        return wrapper
    return decorator


def create_combo_system(combo_multipliers: dict[int, float]):
    combo_count = 0

    def hit(base_damage: int) -> dict:
        nonlocal combo_count
        combo_count += 1
        applicable = max(k for k in combo_multipliers if k <= combo_count)
        mult = combo_multipliers[applicable]
        actual_damage = int(base_damage * mult)
        return {"damage": actual_damage, "combo": combo_count, "multiplier": mult}

    def reset():
        nonlocal combo_count
        combo_count = 0

    def get_combo() -> int:
        return combo_count

    return hit, reset, get_combo


def buff_timeline(*buffs: dict):
    active = [dict(b) for b in buffs]
    turn = 0

    while active:
        turn += 1
        active_names = [b["name"] for b in active]
        effects = {}
        for b in active:
            effects[b["stat"]] = effects.get(b["stat"], 1.0) * b["value"]

        expired = []
        remaining = []
        for b in active:
            b["duration"] -= 1
            if b["duration"] <= 0:
                expired.append(b["name"])
            else:
                remaining.append(b)

        yield {
            "turn": turn,
            "active_buffs": active_names,
            "effects": effects,
            "expired": expired,
        }

        active = remaining


def create_ability(name: str, base_damage: int, element: str = "neutral"):
    def use(target: str) -> dict:
        return {
            "name": name,
            "damage": base_damage,
            "element": element,
            "target": target,
        }
    return use


if __name__ == "__main__":
    print("=" * 50)
    print("⚔️ RPG BUFF/DEBUFF SYSTEM — Tests")
    print("=" * 50)

    print("\n--- Test 1 : @timed_ability ---")
    @timed_ability
    def fireball(target: str) -> dict:
        return {"damage": 75, "element": "fire", "target": target}
    fireball("Dragon")

    print("\n--- Test 2 : @buff ---")
    @buff("damage", 2.0, duration=2)
    def slash(target: str) -> dict:
        return {"damage": 25, "target": target}
    for i in range(4):
        result = slash(f"enemy_{i}")
        print(f"  Hit {i+1}: {result}")

    print("\n--- Test 3 : Combo System ---")
    hit, reset, get_combo = create_combo_system({1: 1.0, 3: 1.5, 5: 2.0, 10: 3.0})
    for i in range(7):
        result = hit(10)
        print(f"  Hit {i+1}: {result}")
    reset()
    print(f"  Combo after reset: {get_combo()}")

    print("\n--- Test 4 : Buff Timeline ---")
    for turn_info in buff_timeline(
        {"name": "Power Up", "stat": "attack", "value": 1.5, "duration": 3},
        {"name": "Shield", "stat": "defense", "value": 2.0, "duration": 2},
        {"name": "Haste", "stat": "speed", "value": 1.8, "duration": 4},
    ):
        active = ", ".join(turn_info["active_buffs"])
        expired = ", ".join(turn_info["expired"])
        print(f"  Turn {turn_info['turn']}: [{active}]" +
              (f" | Expired: {expired}" if expired else ""))

    print("\n--- Test 5 : Ability ---")
    fire = create_ability("Fireball", 75, "fire")
    print(f"  {fire('Goblin')}")

    print("\n✅ Tests terminés !")
