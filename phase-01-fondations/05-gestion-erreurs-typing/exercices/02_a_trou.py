"""
Module 05 — Exercice à trou #2
🎯 Thème : Context managers et typing avancé

Complète les ___ pour que le code fonctionne.
Exécute avec : python 02_a_trou.py
"""

import time
import json
from pathlib import Path
from contextlib import ___  # Quel import pour le decorator context manager ?
from typing import TypeVar, Generic, Callable
from dataclasses import dataclass, field

# ============================================================
# PARTIE 1 : Context managers
# ============================================================

class GameTimer:
    """Context manager qui mesure et log le temps d'un bloc."""
    
    def __init__(self, label: str) -> None:
        self.label = label
        self.elapsed: float = 0.0
    
    def ___(self) -> "GameTimer":  # Quelle dunder pour entrer dans le 'with' ?
        self.start = time.perf_counter()
        print(f"⏱️ [{self.label}] Start")
        return ___  # Que retourner pour le 'as' ?
    
    def ___(self, exc_type, exc_val, exc_tb) -> bool:
        self.elapsed = time.perf_counter() - self.start
        if exc_type is not None:
            print(f"⏱️ [{self.label}] Error after {self.elapsed:.4f}s: {exc_val}")
        else:
            print(f"⏱️ [{self.label}] Done in {self.elapsed:.4f}s")
        return ___  # True supprime l'exception, False la propage


# Test
with GameTimer("Heavy computation") as timer:
    total = sum(i ** 2 for i in range(500_000))

print(f"Elapsed: {timer.elapsed:.4f}s\n")


# Context manager avec @contextmanager
@___  # Quel decorator ?
def game_save_context(filepath: str):
    """
    Context manager pour gérer un fichier de sauvegarde.
    - Crée un backup avant modification
    - Restaure le backup en cas d'erreur
    - Supprime le backup si tout va bien
    """
    path = Path(filepath)
    backup = path.with_suffix(".bak")
    
    # Backup si le fichier existe
    if path.exists():
        backup.write_text(path.read_text())
        print(f"  💾 Backup créé: {backup.name}")
    
    ___:  # Quel bloc contient le yield ?
        ___ path  # Quel mot-clé pour produire la valeur au 'as' ?
    except Exception as e:
        # Restaurer le backup
        if backup.exists():
            backup.rename(path)
            print(f"  ♻️ Backup restauré après erreur: {e}")
        raise
    ___:  # Quel bloc si pas d'erreur ?
        if backup.exists():
            backup.unlink()
            print(f"  🗑️ Backup supprimé (sauvegarde OK)")


# Test
test_file = Path("/tmp/test_save.json")
test_file.write_text('{"level": 1}')

with game_save_context(str(test_file)) as save_path:
    data = json.loads(save_path.read_text())
    data["level"] = 42
    save_path.write_text(json.dumps(data, indent=2))

print(f"Save content: {test_file.read_text()}\n")


# ============================================================
# PARTIE 2 : Typing avancé — TypeVar et Generic
# ============================================================

T = ___("T")  # Créer un TypeVar

class GameStack(___[T]):  # De quelle classe hériter pour les generics ?
    """Stack générique typée (comme Stack<T> en TypeScript)."""
    
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def push(self, item: ___) -> None:  # Quel type pour item ?
        self._items.append(item)
    
    def pop(self) -> T:
        if not self._items:
            raise IndexError("Stack vide !")
        return self._items.pop()
    
    def peek(self) -> T | None:
        return self._items[-1] if self._items else None
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __bool__(self) -> bool:
        return len(self._items) > 0


# Test generics
int_stack: GameStack[int] = GameStack()
int_stack.push(42)
int_stack.push(100)
print(f"Stack: popped {int_stack.pop()}")  # 100

str_stack: GameStack[str] = GameStack()
str_stack.push("sword")
str_stack.push("shield")
print(f"Stack: peek = {str_stack.peek()}")  # shield


# ============================================================
# PARTIE 3 : Callable types
# ============================================================

# Typer une fonction comme argument
EventHandler = ___[[str, dict], None]  # Quel type du module typing ?

def on_event(event_name: str, handler: EventHandler) -> None:
    """Enregistre un handler d'événement."""
    print(f"  📌 Handler registered for '{event_name}'")
    handler(event_name, {"timestamp": time.time()})


def log_handler(name: str, data: dict) -> None:
    print(f"  📝 Event '{name}': {data}")


on_event("player_death", log_handler)


# ============================================================
# PARTIE 4 : Literal types
# ============================================================

from typing import ___  # Quel import pour les types littéraux ?

Difficulty = Literal["easy", "normal", "hard", "nightmare"]
Element = Literal["fire", "water", "earth", "air"]

@dataclass
class GameSettings:
    difficulty: Difficulty = "normal"
    resolution: tuple[int, int] = (1920, 1080)
    vsync: bool = True
    
    def __post_init__(self) -> None:
        valid_difficulties = {"easy", "normal", "hard", "nightmare"}
        if self.difficulty not in valid_difficulties:
            raise ValueError(f"Difficulté invalide: {self.difficulty}")


settings = GameSettings(difficulty="hard")
print(f"\n⚙️ Settings: {settings}")


# ============================================================
# CHECK FINAL
# ============================================================

if __name__ == "__main__":
    # Cleanup
    test_file.unlink(missing_ok=True)
    print("\n✅ Exercice terminé avec succès !")
