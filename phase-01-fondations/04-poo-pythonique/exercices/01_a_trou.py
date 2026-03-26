"""
Module 04 — Exercice à trou #1
🎯 Thème : Classes, dunder methods et properties

Complète les ___ pour que le code fonctionne.
Exécute avec : python 01_a_trou.py
"""

from __future__ import annotations

# ============================================================
# PARTIE 1 : Classe de base avec dunder methods
# ============================================================

class Potion:
    """Représente une potion dans un RPG."""
    
    def ___(self, name: str, effect: str, power: int, quantity: int = 1) -> None:
        self.name = name
        self.effect = effect    # "heal", "mana", "strength"
        self.power = power
        self.quantity = quantity
    
    def __repr__(___) -> str:  # Quel est le premier paramètre ?
        return f"Potion({self.name!r}, effect={self.effect!r}, power={self.power})"
    
    def ___( self) -> str:  # Quelle dunder method pour print() ?
        emoji = {"heal": "❤️", "mana": "💙", "strength": "💪"}.get(self.effect, "🧪")
        return f"{emoji} {self.name} (x{self.quantity})"
    
    def __eq__(self, other: object) -> bool:
        if not ___(other, Potion):  # Quelle built-in pour vérifier le type ?
            return NotImplemented
        return self.name == other.name and self.effect == other.effect
    
    def ___( self, other: Potion) -> Potion:  # Quelle dunder pour l'opérateur + ?
        """Combine deux potions du même type."""
        if self.effect != other.effect:
            raise ValueError("Impossible de combiner des potions différentes !")
        return Potion(
            name=f"Super {self.name}",
            effect=self.effect,
            power=self.power + other.power,
            quantity=self.quantity + other.quantity,
        )
    
    def ___( self) -> int:  # Quelle dunder pour len() ?
        return self.quantity
    
    def ___( self) -> bool:  # Quelle dunder pour 'if potion:' ?
        return self.quantity > 0


# Test
heal_potion = Potion("Heal Potion", "heal", 50, 3)
print(heal_potion)           # ❤️ Heal Potion (x3)
print(repr(heal_potion))     # Potion('Heal Potion', effect='heal', power=50)
print(len(heal_potion))      # 3
print(bool(heal_potion))     # True

heal2 = Potion("Heal Potion", "heal", 30, 2)
mega_heal = heal_potion + heal2
print(mega_heal)             # ❤️ Super Heal Potion (x5)
print(f"Power: {mega_heal.power}")  # 80


# ============================================================
# PARTIE 2 : Properties avec validation
# ============================================================

class Character:
    def __init__(self, name: str, max_hp: int = 100, max_mana: int = 50) -> None:
        self.name = name
        self.max_hp = max_hp
        self.max_mana = max_mana
        self._hp = max_hp
        self._mana = max_mana
        self._level = 1
    
    @___  # Quel decorator pour un getter ?
    def hp(self) -> int:
        return self._hp
    
    @hp.___  # Quel decorator pour le setter correspondant ?
    def hp(self, value: int) -> None:
        # Clamp entre 0 et max_hp
        self._hp = max(0, ___(value, self.max_hp))
    
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
            ___ ValueError("Le niveau ne peut pas être inférieur à 1")
        self._level = value
        # Bonus : augmenter les stats à chaque level up
        self.max_hp = 100 + (value - 1) * 20
        self.max_mana = 50 + (value - 1) * 10
    
    @property
    def is_alive(self) -> bool:
        return self._hp ___ 0  # Quel opérateur ?
    
    @property
    def status_bar(self) -> str:
        hp_pct = self._hp / self.max_hp
        mana_pct = self._mana / self.max_mana
        hp_filled = int(hp_pct * 10)
        mana_filled = int(mana_pct * 10)
        return (
            f"{self.name} (Lv.{self._level})\n"
            f"  HP:   [{'█' * hp_filled}{'░' * (10 - hp_filled)}] "
            f"{self._hp}/{self.max_hp}\n"
            f"  MANA: [{'█' * mana_filled}{'░' * (10 - mana_filled)}] "
            f"{self._mana}/{self.max_mana}"
        )


# Test
hero = Character("Alice")
print(hero.status_bar)
hero.hp = 75
hero.hp = -50  # Clamp to 0
print(f"HP after over-damage: {hero.hp}")  # 0
print(f"Alive: {hero.is_alive}")  # False

hero.hp = hero.max_hp  # Full heal
hero.level = 5
print(f"\nAfter level up:")
print(hero.status_bar)


# ============================================================
# PARTIE 3 : Iterable class
# ============================================================

class Inventory:
    """Un inventaire itérable et indexable."""
    
    def __init__(self) -> None:
        self._items: list[Potion] = []
    
    def add(self, item: Potion) -> None:
        # Vérifier si on a déjà cet item
        for existing in self._items:
            if existing == item:
                existing.quantity += item.quantity
                return
        self._items.append(item)
    
    def ___( self, index: int) -> Potion:  # Quelle dunder pour inventory[0] ?
        return self._items[index]
    
    def ___( self):  # Quelle dunder pour 'for item in inventory:' ?
        return iter(self._items)
    
    def ___( self) -> int:  # Quelle dunder pour len(inventory) ?
        return len(self._items)
    
    def __contains__(self, item_name: str) -> bool:
        return ___(p.name == item_name for p in self._items)  # any ou all ?
    
    def __str__(self) -> str:
        if not self._items:
            return "🎒 Inventaire vide"
        lines = ["🎒 Inventaire :"]
        for i, item in ___(self._items):  # Quelle built-in pour index + valeur ?
            lines.append(f"  [{i}] {item}")
        return "\n".join(lines)


# Test
inv = Inventory()
inv.add(Potion("Heal", "heal", 50, 3))
inv.add(Potion("Mana", "mana", 30, 2))
inv.add(Potion("Heal", "heal", 50, 1))  # Devrait augmenter la quantité

print(f"\n{inv}")
print(f"Items: {len(inv)}")
print(f"First item: {inv[0]}")
print(f"Has heal: {'Heal' in inv}")

print("\nItération :")
for potion in inv:
    print(f"  {potion}")


# ============================================================
# CHECK FINAL
# ============================================================

if __name__ == "__main__":
    print("\n✅ Exercice terminé avec succès !")
