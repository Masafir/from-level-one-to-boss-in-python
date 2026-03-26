"""Module 04 — Solution exercice à trou #2"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@dataclass
class Stats:
    hp: int = 100
    attack: int = 10
    defense: int = 10
    speed: int = 10

    @property
    def power_score(self) -> float:
        return (self.hp * 0.8) + (self.attack * 1.2) + (self.defense * 1.0) + (self.speed * 1.0)

    def __add__(self, other: Stats) -> Stats:
        return Stats(
            hp=self.hp + other.hp, attack=self.attack + other.attack,
            defense=self.defense + other.defense, speed=self.speed + other.speed,
        )


@dataclass
class Equipment:
    name: str
    slot: str
    bonus_stats: Stats = field(default_factory=Stats)
    rarity: str = "common"

    def __post_init__(self) -> None:
        valid_slots = {"weapon", "armor", "accessory", "helmet", "boots"}
        if self.slot not in valid_slots:
            raise ValueError(f"Slot invalide: {self.slot}")
        valid_rarities = {"common", "uncommon", "rare", "epic", "legendary"}
        if self.rarity not in valid_rarities:
            raise ValueError(f"Rareté invalide: {self.rarity}")


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def distance_to(self, other: Position) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


stats = Stats(hp=150, attack=30, defense=20, speed=25)
print(f"Stats: {stats}")
print(f"Power: {stats.power_score}")

sword = Equipment("Excalibur", "weapon", Stats(attack=50), "legendary")
print(f"\n{sword}")

pos1 = Position(0, 0)
pos2 = Position(3, 4)
print(f"\nDistance: {pos1.distance_to(pos2)}")


class GameEntity(ABC):
    def __init__(self, name: str, position: Position) -> None:
        self.name = name
        self.position = position

    @abstractmethod
    def update(self, dt: float) -> None: ...

    @abstractmethod
    def render(self) -> str: ...

    def __str__(self) -> str:
        return f"{self.render()} {self.name} at ({self.position.x}, {self.position.y})"


class Hero(GameEntity):
    def __init__(self, name: str, stats: Stats, position: Position = Position(0, 0)) -> None:
        super().__init__(name, position)
        self.stats = stats
        self.equipment: list[Equipment] = []

    @property
    def total_stats(self) -> Stats:
        result = self.stats
        for eq in self.equipment:
            result = result + eq.bonus_stats
        return result

    def update(self, dt: float) -> None:
        pass

    def render(self) -> str:
        return "🦸"

    def equip(self, item: Equipment) -> None:
        self.equipment.append(item)
        print(f"  {self.name} equips {item.name}!")


class Enemy(GameEntity):
    def __init__(self, name: str, stats: Stats, xp_reward: int,
                 position: Position = Position(0, 0)) -> None:
        super().__init__(name, position)
        self.stats = stats
        self.xp_reward = xp_reward

    def update(self, dt: float) -> None:
        pass

    def render(self) -> str:
        return "👹"


hero = Hero("Alice", Stats(hp=200, attack=30, defense=25, speed=20))
hero.equip(sword)
print(f"\n{hero}")
print(f"Base attack: {hero.stats.attack}")
print(f"Total attack: {hero.total_stats.attack}")

goblin = Enemy("Goblin", Stats(hp=30, attack=8), xp_reward=15)
print(f"{goblin}")


@runtime_checkable
class Attackable(Protocol):
    stats: Stats
    name: str
    def take_damage(self, amount: int) -> int: ...


class CombatHero(Hero):
    def take_damage(self, amount: int) -> int:
        actual = max(0, amount - self.total_stats.defense)
        self.stats.hp -= actual
        print(f"  {self.name} takes {actual} damage ! ({self.stats.hp} HP left)")
        return actual


class CombatEnemy(Enemy):
    def take_damage(self, amount: int) -> int:
        actual = max(0, amount - self.stats.defense)
        self.stats.hp -= actual
        return actual


def attack(attacker: Attackable, target: Attackable) -> int:
    damage = attacker.stats.attack
    print(f"⚔️ {attacker.name} attacks {target.name} for {damage} damage!")
    return target.take_damage(damage)


combat_hero = CombatHero("Alice", Stats(hp=200, attack=50, defense=25))
combat_goblin = CombatEnemy("Goblin", Stats(hp=30, attack=8, defense=5), xp_reward=15)

print(f"\nIs Attackable: {isinstance(combat_hero, Attackable)}")
attack(combat_hero, combat_goblin)
attack(combat_goblin, combat_hero)

print("\n✅ Exercice terminé avec succès !")
