# Module 04 — POO Pythonique 🏰

> **Objectif** : Maîtriser la programmation orientée objet en Python. Si tu connais les classes JS/TS, tu vas retrouver des concepts familiers mais avec des twists très Python (dunder methods, ABC, dataclasses, protocols).

## 1. Classes de base — Rappel express

```python
# JS :
# class Player {
#   constructor(name, hp = 100) {
#     this.name = name;
#     this.hp = hp;
#   }
#   attack(target) { ... }
# }

# Python :
class Player:
    """Un joueur RPG."""
    
    def __init__(self, name: str, hp: int = 100) -> None:
        # self = this en JS, mais explicite en Python
        self.name = name
        self.hp = hp
        self.inventory: list[str] = []
    
    def attack(self, target: "Player") -> int:
        """Attaque un autre joueur."""
        damage = 10
        target.hp -= damage
        return damage

# Instanciation (pas de 'new' !)
alice = Player("Alice")
bob = Player("Bob", hp=150)
alice.attack(bob)
print(bob.hp)  # 140
```

### Différences clés avec JS :

| JS | Python |
|-----|--------|
| `this` (implicite) | `self` (explicite, premier paramètre) |
| `constructor()` | `__init__()` |
| `new Player()` | `Player()` (pas de new) |
| `#privateField` | `_protected` / `__private` (convention) |
| `get name()` | `@property` |
| `static method()` | `@staticmethod` ou `@classmethod` |

## 2. Dunder Methods (Magic Methods) ✨

Les "double underscore methods" ou "dunder" sont le superpower de la POO Python. Elles définissent comment tes objets se comportent avec les opérateurs, `print()`, `len()`, etc.

```python
class Weapon:
    def __init__(self, name: str, damage: int, weight: float) -> None:
        self.name = name
        self.damage = damage
        self.weight = weight
    
    # __repr__ : représentation "technique" (pour le debug)
    def __repr__(self) -> str:
        return f"Weapon(name={self.name!r}, damage={self.damage}, weight={self.weight})"
    
    # __str__ : représentation "humaine" (pour print())
    def __str__(self) -> str:
        return f"⚔️ {self.name} ({self.damage} dmg)"
    
    # __eq__ : opérateur ==
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Weapon):
            return NotImplemented
        return self.name == other.name and self.damage == other.damage
    
    # __lt__ : opérateur < (permet aussi sorted() !)
    def __lt__(self, other: "Weapon") -> bool:
        return self.damage < other.damage
    
    # __add__ : opérateur +
    def __add__(self, other: "Weapon") -> "Weapon":
        """Fusionne deux armes."""
        return Weapon(
            name=f"{self.name}+{other.name}",
            damage=self.damage + other.damage,
            weight=self.weight + other.weight,
        )
    
    # __len__ : pour len()
    def __len__(self) -> int:
        return self.damage
    
    # __bool__ : pour if weapon:
    def __bool__(self) -> bool:
        return self.damage > 0
    
    # __contains__ : pour 'x in weapon' (ici, cherche dans le nom)
    def __contains__(self, item: str) -> bool:
        return item.lower() in self.name.lower()

# Utilisation
sword = Weapon("Excalibur", 100, 5.0)
dagger = Weapon("Dagger", 25, 1.0)

print(sword)           # ⚔️ Excalibur (100 dmg)   — utilise __str__
print(repr(sword))     # Weapon(name='Excalibur', damage=100, weight=5.0)
print(sword > dagger)  # True   — utilise __lt__ inversé
print(sword + dagger)  # ⚔️ Excalibur+Dagger (125 dmg)
print(len(sword))      # 100
print("excal" in sword)  # True
sorted([sword, dagger])  # Trié par damage grâce à __lt__
```

### Dunder methods les plus utiles

| Méthode | Quand elle est appelée |
|---------|----------------------|
| `__init__` | À la création : `Player()` |
| `__repr__` | `repr(obj)`, debug, REPL |
| `__str__` | `str(obj)`, `print(obj)`, f-strings |
| `__eq__` | `obj1 == obj2` |
| `__lt__`, `__gt__` | `<`, `>` (et `sorted()`) |
| `__add__`, `__sub__` | `+`, `-` |
| `__len__` | `len(obj)` |
| `__bool__` | `if obj:`, `bool(obj)` |
| `__contains__` | `x in obj` |
| `__getitem__` | `obj[key]` |
| `__iter__` | `for x in obj:` |
| `__hash__` | Utilisation dans `set()` ou comme clé de `dict` |

## 3. Properties — Les getters/setters Python

```python
class Character:
    def __init__(self, name: str, max_hp: int = 100) -> None:
        self.name = name
        self.max_hp = max_hp
        self._hp = max_hp  # Convention : _ = "protégé"
    
    @property
    def hp(self) -> int:
        """Getter pour hp."""
        return self._hp
    
    @hp.setter
    def hp(self, value: int) -> None:
        """Setter avec validation."""
        self._hp = max(0, min(value, self.max_hp))  # Clamp entre 0 et max_hp
    
    @property
    def is_alive(self) -> bool:
        """Propriété calculée (pas de setter)."""
        return self._hp > 0
    
    @property
    def hp_bar(self) -> str:
        """Barre de vie visuelle."""
        filled = int(self._hp / self.max_hp * 20)
        return f"[{'█' * filled}{'░' * (20 - filled)}] {self._hp}/{self.max_hp}"

hero = Character("Alice", max_hp=100)
hero.hp = 75
print(hero.hp_bar)    # [███████████████░░░░░] 75/100
hero.hp = -50         # Clampé à 0
print(hero.is_alive)  # False
```

## 4. Héritage et Composition

### Héritage

```python
class Entity:
    """Classe de base pour toutes les entités du jeu."""
    
    def __init__(self, name: str, x: int = 0, y: int = 0) -> None:
        self.name = name
        self.x = x
        self.y = y
    
    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

class Monster(Entity):
    """Un monstre qui hérite d'Entity."""
    
    def __init__(self, name: str, hp: int, damage: int, **kwargs) -> None:
        super().__init__(name, **kwargs)  # Appelle Entity.__init__
        self.hp = hp
        self.damage = damage
    
    def attack(self, target: Entity) -> int:
        print(f"🐉 {self.name} attaque {target.name} !")
        return self.damage

goblin = Monster("Goblin", hp=30, damage=5, x=10, y=20)
goblin.move(1, 0)  # Hérité de Entity
```

### Composition > Héritage

```python
# ❌ TROP d'héritage (anti-pattern)
class FlyingFireMonster(FlyingMonster, FireMonster, Monster, Entity):
    ...

# ✅ Composition (pattern recommandé)
class Ability:
    def __init__(self, name: str, damage: int) -> None:
        self.name = name
        self.damage = damage

class Monster:
    def __init__(self, name: str, hp: int) -> None:
        self.name = name
        self.hp = hp
        self.abilities: list[Ability] = []
    
    def add_ability(self, ability: Ability) -> None:
        self.abilities.append(ability)
    
    def use_ability(self, index: int) -> int:
        ability = self.abilities[index]
        return ability.damage

dragon = Monster("Dragon", hp=500)
dragon.add_ability(Ability("Fireball", 50))
dragon.add_ability(Ability("Fly", 0))
```

## 5. Classes Abstraites (ABC)

```python
from abc import ABC, abstractmethod

class GameEntity(ABC):
    """Classe abstraite — ne peut pas être instanciée directement."""
    
    def __init__(self, name: str) -> None:
        self.name = name
    
    @abstractmethod
    def update(self, dt: float) -> None:
        """Doit être implémenté par les sous-classes."""
        ...
    
    @abstractmethod
    def render(self) -> str:
        """Doit être implémenté par les sous-classes."""
        ...

# entity = GameEntity("test")  # ❌ TypeError: Can't instantiate abstract class

class NPC(GameEntity):
    def __init__(self, name: str, dialogue: str) -> None:
        super().__init__(name)
        self.dialogue = dialogue
    
    def update(self, dt: float) -> None:
        pass  # NPC ne bouge pas
    
    def render(self) -> str:
        return f"🧑 {self.name}"

npc = NPC("Merchant", "Buy something!")  # ✅ OK
```

## 6. Dataclasses — Les classes simplifiées 🚀

Les dataclasses sont le game changer pour les classes "de données" (DTOs, modèles, configs).

```python
from dataclasses import dataclass, field

# Sans dataclass (verbeux !)
class ItemOld:
    def __init__(self, name: str, value: int, weight: float, tags: list[str]) -> None:
        self.name = name
        self.value = value
        self.weight = weight
        self.tags = tags
    
    def __repr__(self): ...
    def __eq__(self, other): ...
    # etc...

# Avec dataclass (magique !)
@dataclass
class Item:
    name: str
    value: int
    weight: float
    tags: list[str] = field(default_factory=list)  # Mutable default safe !
    
    # __init__, __repr__, __eq__ sont générés automatiquement !

sword = Item("Sword", 100, 3.5, ["weapon", "melee"])
print(sword)  # Item(name='Sword', value=100, weight=3.5, tags=['weapon', 'melee'])

# Comparaison automatique
sword2 = Item("Sword", 100, 3.5, ["weapon", "melee"])
print(sword == sword2)  # True !

# Frozen dataclass (immutable, comme Object.freeze() en JS)
@dataclass(frozen=True)
class Position:
    x: int
    y: int

pos = Position(10, 20)
# pos.x = 30  # ❌ FrozenInstanceError !

# Dataclass avec méthodes custom
@dataclass
class GameConfig:
    width: int = 1920
    height: int = 1080
    fps: int = 60
    fullscreen: bool = False
    
    @property
    def resolution(self) -> str:
        return f"{self.width}x{self.height}"
    
    def __post_init__(self) -> None:
        """Appelé après __init__ — pour validation."""
        if self.fps not in (30, 60, 120, 144):
            raise ValueError(f"FPS invalide: {self.fps}")
```

## 7. Protocols — Le duck typing typé

Les Protocols c'est comme les interfaces TypeScript mais en "structural typing" (duck typing).

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Damageable(Protocol):
    """Tout ce qui peut recevoir des dégâts."""
    hp: int
    
    def take_damage(self, amount: int) -> None: ...

@runtime_checkable
class Renderable(Protocol):
    """Tout ce qui peut être affiché."""
    def render(self) -> str: ...

# Pas besoin de "implements Damageable" !
# Si la classe a les bons attributs/méthodes, ça marche.

class Wall:
    def __init__(self, hp: int) -> None:
        self.hp = hp
    
    def take_damage(self, amount: int) -> None:
        self.hp -= amount
    
    def render(self) -> str:
        return "🧱"

# Wall est Damageable ET Renderable sans le déclarer !
wall = Wall(50)
print(isinstance(wall, Damageable))  # True !
print(isinstance(wall, Renderable))  # True !

def destroy(target: Damageable) -> None:
    """Fonctionne avec TOUT objet qui a hp et take_damage."""
    target.take_damage(999)
```

## 8. Slots — Optimisation mémoire

```python
# Sans __slots__ : chaque instance a un __dict__ (flexible mais lourd)
class PlayerHeavy:
    def __init__(self, name: str, hp: int):
        self.name = name
        self.hp = hp

# Avec __slots__ : attributs fixes, mémoire réduite (~40% de RAM en moins)
class PlayerLight:
    __slots__ = ("name", "hp")
    
    def __init__(self, name: str, hp: int):
        self.name = name
        self.hp = hp

# player = PlayerLight("Alice", 100)
# player.mana = 50  # ❌ AttributeError ! (pas dans __slots__)

# Utile quand tu crées des milliers d'instances (particules, projectiles, etc.)
```

---

## 🎯 Résumé

| Concept | Quand l'utiliser |
|---------|-----------------|
| **Classe classique** | Logique complexe, beaucoup de méthodes |
| **Dataclass** | Classes de données (DTOs, configs, modèles) |
| **ABC** | Forcer une interface commune entre sous-classes |
| **Protocol** | Duck typing avec vérification de types (préféré aux ABC souvent) |
| **@property** | Getter/setter avec validation |
| **Dunder methods** | Personnaliser print, ==, +, len(), in, [] etc. |
| **Composition** | Quand l'héritage crée trop de couplage |

---

➡️ **Maintenant, passe aux exercices dans `exercices/` !**
