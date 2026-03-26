"""Module 03 — Solution exercice à trou #1"""

from functools import wraps


def create_spell(name: str, *damage: int, **props) -> dict:
    total_damage = sum(damage)
    return {
        "name": name,
        "total_damage": total_damage,
        "hits": len(damage),
        **props,
    }


fireball = create_spell("Fireball", 30, 20, 15, element="fire", aoe=True)
print(f"🔥 {fireball}")

damages = [25, 30, 25, 20]
multi_hit = create_spell("Barrage", *damages, element="physical")
print(f"⚔️ {multi_hit}")


def create_xp_tracker(level_thresholds: list[int]):
    current_xp = 0
    current_level = 1

    def gain_xp(amount: int) -> dict:
        nonlocal current_xp
        nonlocal current_level
        current_xp += amount
        while (current_level - 1) < len(level_thresholds) and \
              current_xp >= level_thresholds[current_level - 1]:
            current_level += 1
            print(f"  🎉 LEVEL UP ! Niveau {current_level} !")
        return {"xp": current_xp, "level": current_level}

    def get_status() -> dict:
        if (current_level - 1) < len(level_thresholds):
            next_threshold = level_thresholds[current_level - 1]
            remaining = next_threshold - current_xp
        else:
            remaining = 0
        return {"level": current_level, "xp": current_xp, "xp_to_next": remaining}

    return gain_xp, get_status


gain_xp, get_status = create_xp_tracker([100, 300, 600, 1000])
print("\n📊 XP Tracker:")
gain_xp(50)
print(f"  Status: {get_status()}")
gain_xp(60)
print(f"  Status: {get_status()}")
gain_xp(200)
print(f"  Status: {get_status()}")


def apply_buffs(base_stats: dict[str, int], *buff_functions) -> dict[str, int]:
    stats = base_stats.copy()
    for buff_fn in buff_functions:
        stats = buff_fn(stats)
    return stats


def strength_buff(stats: dict[str, int]) -> dict[str, int]:
    result = stats.copy()
    result["attack"] = int(result["attack"] * 1.5)
    return result

def shield_buff(stats: dict[str, int]) -> dict[str, int]:
    result = stats.copy()
    result["defense"] = int(result["defense"] * 2.0)
    return result

def create_buff(stat: str, multiplier: float):
    def buff(stats: dict[str, int]) -> dict[str, int]:
        result = stats.copy()
        result[stat] = int(result[stat] * multiplier)
        return result
    return buff


base = {"attack": 50, "defense": 30, "speed": 40}
speed_buff = create_buff("speed", 3.0)
buffed = apply_buffs(base, strength_buff, shield_buff, speed_buff)
print(f"\n💪 Base: {base}")
print(f"💪 Buffed: {buffed}")


def compose(*functions):
    def composed(value):
        result = value
        for fn in reversed(functions):
            result = fn(result)
        return result
    return composed


def parse_score(raw: str) -> int:
    return int(raw.strip())

def apply_bonus(score: int) -> int:
    return int(score * 1.2)

def clamp_max(score: int) -> int:
    return min(score, 99999)


process_score = compose(clamp_max, apply_bonus, parse_score)
print(f"\n🎯 Score: {process_score('  85000  ')}")
print(f"🎯 Score: {process_score('  50000  ')}")

print("\n✅ Exercice terminé avec succès !")
