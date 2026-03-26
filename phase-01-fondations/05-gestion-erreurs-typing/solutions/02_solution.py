"""Module 05 — Solution exercice à trou #2"""

import time
import json
from pathlib import Path
from contextlib import contextmanager
from typing import TypeVar, Generic, Callable, Literal
from dataclasses import dataclass


class GameTimer:
    def __init__(self, label: str) -> None:
        self.label = label
        self.elapsed: float = 0.0

    def __enter__(self) -> "GameTimer":
        self.start = time.perf_counter()
        print(f"⏱️ [{self.label}] Start")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.elapsed = time.perf_counter() - self.start
        if exc_type is not None:
            print(f"⏱️ [{self.label}] Error after {self.elapsed:.4f}s: {exc_val}")
        else:
            print(f"⏱️ [{self.label}] Done in {self.elapsed:.4f}s")
        return False


with GameTimer("Heavy computation") as timer:
    total = sum(i ** 2 for i in range(500_000))
print(f"Elapsed: {timer.elapsed:.4f}s\n")


@contextmanager
def game_save_context(filepath: str):
    path = Path(filepath)
    backup = path.with_suffix(".bak")

    if path.exists():
        backup.write_text(path.read_text())
        print(f"  💾 Backup créé: {backup.name}")

    try:
        yield path
    except Exception as e:
        if backup.exists():
            backup.rename(path)
            print(f"  ♻️ Backup restauré après erreur: {e}")
        raise
    else:
        if backup.exists():
            backup.unlink()
            print(f"  🗑️ Backup supprimé (sauvegarde OK)")


test_file = Path("/tmp/test_save.json")
test_file.write_text('{"level": 1}')

with game_save_context(str(test_file)) as save_path:
    data = json.loads(save_path.read_text())
    data["level"] = 42
    save_path.write_text(json.dumps(data, indent=2))

print(f"Save content: {test_file.read_text()}\n")


T = TypeVar("T")


class GameStack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
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


int_stack: GameStack[int] = GameStack()
int_stack.push(42)
int_stack.push(100)
print(f"Stack: popped {int_stack.pop()}")

str_stack: GameStack[str] = GameStack()
str_stack.push("sword")
str_stack.push("shield")
print(f"Stack: peek = {str_stack.peek()}")


EventHandler = Callable[[str, dict], None]


def on_event(event_name: str, handler: EventHandler) -> None:
    print(f"  📌 Handler registered for '{event_name}'")
    handler(event_name, {"timestamp": time.time()})


def log_handler(name: str, data: dict) -> None:
    print(f"  📝 Event '{name}': {data}")


on_event("player_death", log_handler)


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

test_file.unlink(missing_ok=True)
print("\n✅ Exercice terminé avec succès !")
