"""
Module 04 — Exercice à trou #2
🎯 Thème : Dataclasses, ABC et héritage

Complète les ___ pour que le code fonctionne.
Exécute avec : python 02_a_trou.py
"""

from __future__ import annotations
from abc import ___, abstractmethod  # Quel import pour les classes abstraites ?
from dataclasses import ___, field  # Quel import pour les dataclasses ?
from typing import Protocol, runtime_checkable

# ============================================================
# PARTIE 1 : Dataclasses
# ============================================================

@___  # Quel decorator pour une dataclass ?
class Stats:
    hp: int = 100
    attack: int = 10
    defense: int = 10
    speed: int = 10
    
    @property
    def power_score(self) -> float:
        return (self.hp * 0.8) + (self.attack * 1.2) + \
               (self.defense * 1.0) + (self.speed * 1.0)
    
    def __add__(self, other: Stats) -> Stats:
        return Stats(
            hp=self.hp + other.hp,
            attack=self.attack + other.attack,
            defense=self.defense + other.defense,
            speed=self.speed + other.speed,
        )


@dataclass
class Equipment:
    name: str
    slot: str  # "weapon", "armor", "accessory"
    bonus_stats: Stats = field(default_factory=___)  # Quelle factory par défaut ?
    rarity: str = "common"
    
    def __post_init__(self) -> None:
        """Validation après création."""
        valid_slots = {"weapon", "armor", "accessory", "helmet", "boots"}
        if self.slot not in valid_slots:
            raise ___( f"Slot invalide: {self.slot}")
        valid_rarities = {"common", "uncommon", "rare", "epic", "legendary"}
        if self.rarity not in valid_rarities:
            raise ValueError(f"Rareté invalide: {self.rarity}")


# Frozen dataclass (immutable)
@dataclass(___=True)  # Quel argument pour rendre immutable ?
class Position:
    x: int
    y: int
    
    def distance_to(self, other: Position) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


# Test
stats = Stats(hp=150, attack=30, defense=20, speed=25)
print(f"Stats: {stats}")
print(f"Power: {stats.power_score}")

sword = Equipment("Excalibur", "weapon", Stats(attack=50), "legendary")
print(f"\n{sword}")

pos1 = Position(0, 0)
pos2 = Position(3, 4)
print(f"\nDistance: {pos1.distance_to(pos2)}")  # 5.0


# ============================================================
# PARTIE 2 : Classes abstraites (ABC)
# ============================================================

class GameEntity(___):  # De quelle classe abstraite hériter ?
    """Classe abstraite pour toutes les entités du jeu."""
    
    def __init__(self, name: str, position: Position) -> None:
        self.name = name
        self.position = position
    
    @___  # Quel decorator pour une méthode abstraite ?
    def update(self, dt: float) -> None:
        """Met à jour l'entité chaque frame."""
        ...
    
    @abstractmethod
    def render(self) -> str:
        """Retourne la représentation visuelle."""
        ...
    
    def __str__(self) -> str:
        return f"{self.render()} {self.name} at ({self.position.x}, {self.position.y})"


class Hero(GameEntity):
    def __init__(self, name: str, stats: Stats, position: Position = Position(0, 0)) -> None:
        ___().__init__(name, position)  # Appeler le __init__ parent
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


# Test
hero = Hero("Alice", Stats(hp=200, attack=30, defense=25, speed=20))
hero.equip(sword)
print(f"\n{hero}")
print(f"Base attack: {hero.stats.attack}")
print(f"Total attack: {hero.total_stats.attack}")  # 30 + 50 = 80

goblin = Enemy("Goblin", Stats(hp=30, attack=8), xp_reward=15)
print(f"{goblin}")


# ============================================================
# PARTIE 3 : Protocols (duck typing)
# ============================================================

@runtime_checkable
class Attackable(___):  # De quelle classe hériter pour un Protocol ?
    """Tout ce qui peut être attaqué."""
    stats: Stats
    name: str
    
    def take_damage(self, amount: int) -> int: ...


# Ajoutons take_damage aux classes
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
    """
    Fonction générique — fonctionne avec TOUT objet Attackable.
    """
    damage = attacker.stats.attack
    print(f"⚔️ {attacker.name} attacks {target.name} for {damage} damage!")
    return target.take_damage(damage)


# Test
combat_hero = CombatHero("Alice", Stats(hp=200, attack=50, defense=25))
combat_goblin = CombatEnemy("Goblin", Stats(hp=30, attack=8, defense=5), xp_reward=15)

print(f"\nIs Attackable: {___(combat_hero, Attackable)}")  # isinstance
attack(combat_hero, combat_goblin)
attack(combat_goblin, combat_hero)


# ============================================================
# CHECK FINAL
# ============================================================

if __name__ == "__main__":
    print("\n✅ Exercice terminé avec succès !")
