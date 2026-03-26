"""Module 04 — Solution exercice à trou #1"""

from __future__ import annotations


class Potion:
    def __init__(self, name: str, effect: str, power: int, quantity: int = 1) -> None:
        self.name = name
        self.effect = effect
        self.power = power
        self.quantity = quantity

    def __repr__(self) -> str:
        return f"Potion({self.name!r}, effect={self.effect!r}, power={self.power})"

    def __str__(self) -> str:
        emoji = {"heal": "❤️", "mana": "💙", "strength": "💪"}.get(self.effect, "🧪")
        return f"{emoji} {self.name} (x{self.quantity})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Potion):
            return NotImplemented
        return self.name == other.name and self.effect == other.effect

    def __add__(self, other: Potion) -> Potion:
        if self.effect != other.effect:
            raise ValueError("Impossible de combiner des potions différentes !")
        return Potion(
            name=f"Super {self.name}", effect=self.effect,
            power=self.power + other.power, quantity=self.quantity + other.quantity,
        )

    def __len__(self) -> int:
        return self.quantity

    def __bool__(self) -> bool:
        return self.quantity > 0


heal_potion = Potion("Heal Potion", "heal", 50, 3)
print(heal_potion)
print(repr(heal_potion))
print(len(heal_potion))
print(bool(heal_potion))

heal2 = Potion("Heal Potion", "heal", 30, 2)
mega_heal = heal_potion + heal2
print(mega_heal)
print(f"Power: {mega_heal.power}")


class Character:
    def __init__(self, name: str, max_hp: int = 100, max_mana: int = 50) -> None:
        self.name = name
        self.max_hp = max_hp
        self.max_mana = max_mana
        self._hp = max_hp
        self._mana = max_mana
        self._level = 1

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))

    @property
    def mana(self) -> int:
        return self._mana

    @mana.setter
    def mana(self, value: int) -> None:
        self._mana = max(0, min(value, self.max_mana))

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: int) -> None:
        if value < 1:
            raise ValueError("Le niveau ne peut pas être inférieur à 1")
        self._level = value
        self.max_hp = 100 + (value - 1) * 20
        self.max_mana = 50 + (value - 1) * 10

    @property
    def is_alive(self) -> bool:
        return self._hp > 0

    @property
    def status_bar(self) -> str:
        hp_pct = self._hp / self.max_hp
        mana_pct = self._mana / self.max_mana
        hp_filled = int(hp_pct * 10)
        mana_filled = int(mana_pct * 10)
        return (
            f"{self.name} (Lv.{self._level})\n"
            f"  HP:   [{'█' * hp_filled}{'░' * (10 - hp_filled)}] {self._hp}/{self.max_hp}\n"
            f"  MANA: [{'█' * mana_filled}{'░' * (10 - mana_filled)}] {self._mana}/{self.max_mana}"
        )


hero = Character("Alice")
print(hero.status_bar)
hero.hp = 75
hero.hp = -50
print(f"HP after over-damage: {hero.hp}")
print(f"Alive: {hero.is_alive}")
hero.hp = hero.max_hp
hero.level = 5
print(f"\nAfter level up:")
print(hero.status_bar)


class Inventory:
    def __init__(self) -> None:
        self._items: list[Potion] = []

    def add(self, item: Potion) -> None:
        for existing in self._items:
            if existing == item:
                existing.quantity += item.quantity
                return
        self._items.append(item)

    def __getitem__(self, index: int) -> Potion:
        return self._items[index]

    def __iter__(self):
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, item_name: str) -> bool:
        return any(p.name == item_name for p in self._items)

    def __str__(self) -> str:
        if not self._items:
            return "🎒 Inventaire vide"
        lines = ["🎒 Inventaire :"]
        for i, item in enumerate(self._items):
            lines.append(f"  [{i}] {item}")
        return "\n".join(lines)


inv = Inventory()
inv.add(Potion("Heal", "heal", 50, 3))
inv.add(Potion("Mana", "mana", 30, 2))
inv.add(Potion("Heal", "heal", 50, 1))

print(f"\n{inv}")
print(f"Items: {len(inv)}")
print(f"First item: {inv[0]}")
print(f"Has heal: {'Heal' in inv}")

print("\nItération :")
for potion in inv:
    print(f"  {potion}")

print("\n✅ Exercice terminé avec succès !")
