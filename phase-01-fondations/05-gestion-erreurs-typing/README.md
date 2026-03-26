# Module 05 — Gestion d'Erreurs & Typing Avancé 🛡️

> **Objectif** : Écrire du code Python robuste et bien typé. Les exceptions custom, les context managers et le typing avancé sont la marque d'un dev Python pro.

## 1. Exceptions — try/except/else/finally

### Les bases (parallèle avec JS)

```python
# JS :
# try { ... } catch (e) { ... } finally { ... }

# Python :
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Division par zéro !")
except (ValueError, TypeError) as e:  # Plusieurs types d'erreur
    print(f"Erreur : {e}")
except Exception as e:  # Catch-all (comme catch(e) en JS)
    print(f"Erreur inattendue : {e}")
else:
    # S'exécute SEULEMENT si aucune exception (n'existe pas en JS !)
    print(f"Résultat : {result}")
finally:
    # S'exécute TOUJOURS (comme en JS)
    print("Fini !")
```

### Hiérarchie des exceptions

```
BaseException
├── SystemExit
├── KeyboardInterrupt
├── GeneratorExit
└── Exception              ← Tu attrapes ici en général
    ├── ValueError
    ├── TypeError
    ├── KeyError
    ├── IndexError
    ├── FileNotFoundError
    ├── ConnectionError
    ├── TimeoutError
    ├── PermissionError
    ├── AttributeError
    ├── RuntimeError
    └── ... (et tes exceptions custom)
```

### ⚠️ Règles d'or

```python
# ❌ JAMAIS catch Exception nu (sauf logging)
try:
    do_something()
except:  # Attrape TOUT, même Ctrl+C !
    pass

# ❌ Trop large
try:
    do_something()
except Exception:
    pass  # On perd toute info sur l'erreur

# ✅ Spécifique
try:
    data = json.loads(raw_input)
except json.JSONDecodeError as e:
    print(f"JSON invalide : {e}")
    data = {}

# ✅ Re-raise après logging
try:
    process_data(data)
except ValueError as e:
    logger.error(f"Erreur de traitement : {e}")
    raise  # Re-raise l'exception originale
```

## 2. Exceptions Custom

```python
# Crée une hiérarchie d'exceptions pour ton application

class GameError(Exception):
    """Base exception pour toutes les erreurs du jeu."""
    pass

class InsufficientManaError(GameError):
    """Pas assez de mana pour lancer un sort."""
    
    def __init__(self, required: int, available: int) -> None:
        self.required = required
        self.available = available
        super().__init__(
            f"Mana insuffisant : {available}/{required} requis"
        )

class InventoryFullError(GameError):
    """L'inventaire est plein."""
    
    def __init__(self, max_slots: int) -> None:
        self.max_slots = max_slots
        super().__init__(f"Inventaire plein ({max_slots} slots max)")

class ItemNotFoundError(GameError):
    """Item non trouvé dans l'inventaire."""
    
    def __init__(self, item_name: str) -> None:
        self.item_name = item_name
        super().__init__(f"Item '{item_name}' non trouvé")

# Utilisation
def cast_spell(caster: dict, spell: dict) -> None:
    if caster["mana"] < spell["cost"]:
        raise InsufficientManaError(
            required=spell["cost"],
            available=caster["mana"]
        )
    caster["mana"] -= spell["cost"]
    print(f"✨ {spell['name']} lancé !")

# Catch avec info riche
try:
    cast_spell({"mana": 10}, {"name": "Fireball", "cost": 30})
except InsufficientManaError as e:
    print(f"❌ {e}")
    print(f"   Il manque {e.required - e.available} mana")
```

## 3. Context Managers — Le `with` statement

### Le principe

Un context manager garantit qu'une ressource est correctement nettoyée, même en cas d'erreur. C'est comme un `try/finally` automatique.

```python
# ❌ Sans context manager (risque de fuite de ressource)
f = open("file.txt")
data = f.read()
f.close()  # Et si une erreur arrive avant ?

# ✅ Avec context manager
with open("file.txt") as f:
    data = f.read()
# Le fichier est fermé automatiquement, même si une exception est levée
```

### Créer un context manager avec `__enter__` / `__exit__`

```python
import time

class Timer:
    """Context manager qui mesure le temps d'exécution."""
    
    def __init__(self, label: str = "Block") -> None:
        self.label = label
        self.elapsed = 0.0
    
    def __enter__(self):
        """Appelé au début du 'with'. Retourne self."""
        self.start = time.perf_counter()
        return self  # Cette valeur va dans la variable après 'as'
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Appelé à la fin du 'with', même si une exception est levée.
        
        Args:
            exc_type: Type de l'exception (ou None)
            exc_val:  Valeur de l'exception (ou None)
            exc_tb:   Traceback (ou None)
        
        Returns:
            True pour supprimer l'exception, False pour la propager
        """
        self.elapsed = time.perf_counter() - self.start
        print(f"⏱️ {self.label}: {self.elapsed:.4f}s")
        return False  # Ne pas supprimer les exceptions

# Utilisation
with Timer("Data processing"):
    total = sum(i**2 for i in range(1_000_000))
# ⏱️ Data processing: 0.1234s
```

### Créer un context manager avec `@contextmanager`

```python
from contextlib import contextmanager

@contextmanager
def game_session(player_name: str):
    """
    Context manager pour une session de jeu.
    Code avant yield = __enter__
    Code après yield = __exit__
    """
    print(f"🎮 {player_name} rejoint la partie")
    session = {"player": player_name, "start": time.time()}
    
    try:
        yield session  # Valeur retournée au 'as'
    except Exception as e:
        print(f"❌ Erreur pendant la session : {e}")
        raise
    finally:
        duration = time.time() - session["start"]
        print(f"👋 {player_name} quitte ({duration:.1f}s)")

# Utilisation
with game_session("Alice") as session:
    print(f"  Session: {session}")
    # ... jouer ...
```

### Context manager pour les fichiers de sauvegarde

```python
@contextmanager
def save_file(filepath: str, backup: bool = True):
    """
    Context manager pour sauvegarder un fichier de manière sûre.
    Crée un backup avant modification.
    Si une erreur arrive, restaure le backup.
    """
    from pathlib import Path
    path = Path(filepath)
    backup_path = path.with_suffix(path.suffix + ".bak")
    
    # Backup si le fichier existe
    if backup and path.exists():
        backup_path.write_bytes(path.read_bytes())
    
    try:
        yield path
    except Exception:
        # Restaurer le backup en cas d'erreur
        if backup and backup_path.exists():
            backup_path.rename(path)
            print("♻️ Backup restauré")
        raise
    else:
        # Succès : supprimer le backup
        if backup and backup_path.exists():
            backup_path.unlink()
    
# Utilisation
with save_file("game_save.json") as path:
    path.write_text('{"player": "Alice", "level": 42}')
```

## 4. Type Hints Avancés

### Les bases (déjà vues, rappel rapide)

```python
# Types simples
name: str = "Alice"
hp: int = 100
is_alive: bool = True
damage: float = 25.5

# Containers
scores: list[int] = [100, 200]
player: dict[str, int] = {"hp": 100, "mana": 50}
position: tuple[int, int] = (10, 20)
unique_items: set[str] = {"sword", "shield"}

# Optional (peut être None)
target: str | None = None  # Python 3.10+ syntax
# Équivalent ancien : Optional[str]

# Union
damage: int | float = 25  # Peut être int OU float
```

### Types avancés

```python
from typing import (
    TypeAlias, TypeVar, Generic, Callable,
    Literal, TypeGuard, overload, Self,
)

# TypeAlias — nommer des types complexes
JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None
Stats: TypeAlias = dict[str, int]

# Callable — typer des fonctions (comme les function types en TS)
# Callable[[ParamTypes], ReturnType]
BuffFunction: TypeAlias = Callable[[Stats], Stats]
EventHandler: TypeAlias = Callable[[str, dict], None]

def apply_buff(stats: Stats, buff_fn: BuffFunction) -> Stats:
    return buff_fn(stats)

# Literal — valeurs exactes (comme les literal types en TS)
from typing import Literal

Element = Literal["fire", "water", "earth", "air"]
Rarity = Literal["common", "uncommon", "rare", "epic", "legendary"]

def create_item(name: str, rarity: Rarity) -> dict:
    return {"name": name, "rarity": rarity}

create_item("Sword", "rare")       # ✅
create_item("Sword", "mythical")   # ❌ mypy error !

# TypeVar — génériques (comme les generics en TS)
T = TypeVar("T")

def first_or_none(items: list[T]) -> T | None:
    """Retourne le premier élément ou None."""
    return items[0] if items else None

# Le type de retour est inféré automatiquement
first_or_none([1, 2, 3])        # → int | None
first_or_none(["a", "b"])       # → str | None

# Generic classes (comme class Container<T> en TS)
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> T:
        return self._items.pop()

int_stack: Stack[int] = Stack()
int_stack.push(42)
# int_stack.push("hello")  # ❌ mypy error !
```

### Overload — Signatures multiples

```python
from typing import overload

@overload
def get_damage(weapon: str) -> int: ...
@overload
def get_damage(weapon: str, critical: bool) -> tuple[int, bool]: ...

def get_damage(weapon: str, critical: bool = False) -> int | tuple[int, bool]:
    base = {"sword": 25, "staff": 30}.get(weapon, 10)
    if critical:
        return base * 2, True
    return base
```

### TypeGuard — Narrowing de types

```python
from typing import TypeGuard

def is_valid_player(data: dict) -> TypeGuard[dict[str, str | int]]:
    """Vérifie si un dict est un joueur valide."""
    return "name" in data and "hp" in data

def process(data: dict) -> None:
    if is_valid_player(data):
        # Ici data est typé comme dict[str, str | int]
        print(data["name"])
```

## 5. Patterns d'erreurs courants

### EAFP vs LBYL

```python
# LBYL (Look Before You Leap) — Style JS/Java
# "Vérifie avant de faire"
if "name" in player:
    name = player["name"]

# EAFP (Easier to Ask Forgiveness than Permission) — Style Python
# "Essaie et gère l'erreur"
try:
    name = player["name"]
except KeyError:
    name = "Unknown"

# En Python, EAFP est idiomatique et souvent plus performant
# (car les exceptions sont "cheap" si elles ne sont pas levées)

# Mais le plus Pythonique de tous :
name = player.get("name", "Unknown")
```

### Pattern : Validation avec exceptions

```python
from dataclasses import dataclass

@dataclass
class GameConfig:
    width: int
    height: int
    fps: int
    difficulty: Literal["easy", "normal", "hard"]
    
    def __post_init__(self) -> None:
        errors: list[str] = []
        
        if self.width < 640:
            errors.append(f"Width too small: {self.width}")
        if self.height < 480:
            errors.append(f"Height too small: {self.height}")
        if self.fps not in (30, 60, 120):
            errors.append(f"Invalid FPS: {self.fps}")
        
        if errors:
            raise ValueError(
                "Invalid config:\n" + "\n".join(f"  - {e}" for e in errors)
            )
```

---

## 🎯 Résumé

| Concept | Ce qu'il faut retenir |
|---------|----------------------|
| **try/except/else/finally** | `else` = pas d'erreur, `finally` = toujours |
| **Exceptions custom** | Crée une hiérarchie (GameError → InsufficientManaError) |
| **Context managers** | `with` = cleanup garanti. `@contextmanager` ou `__enter__/__exit__` |
| **EAFP** | Essaie d'abord, gère l'erreur ensuite (style Python) |
| **Type hints** | `TypeAlias`, `TypeVar`, `Generic`, `Literal`, `Callable` |
| **mypy** | Lance-le souvent : `mypy --strict src/` |

---

➡️ **Maintenant, passe aux exercices dans `exercices/` !**
