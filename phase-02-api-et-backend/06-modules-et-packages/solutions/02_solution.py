"""Module 06 — Solution exercice à trou #2"""

import os
from dataclasses import dataclass, field
from typing import TypeVar, Callable, Any

@dataclass
class AppConfig:
    app_name: str = "RPG Server"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    db_url: str = "sqlite:///game.db"
    secret_key: str = "change-me-in-production"
    max_connections: int = 100

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            app_name=os.getenv("APP_NAME", "RPG Server"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            db_url=os.getenv("DATABASE_URL", "sqlite:///game.db"),
            secret_key=os.getenv("SECRET_KEY", "change-me-in-production"),
        )

    def validate(self) -> list[str]:
        errors = []
        if self.secret_key == "change-me-in-production" and not self.debug:
            errors.append("SECRET_KEY doit être changé en production !")
        if self.port < 1 or self.port > 65535:
            errors.append(f"PORT invalide : {self.port}")
        return errors


config = AppConfig.from_env()
print(f"⚙️ Config : {config.app_name} on {config.host}:{config.port}")
print(f"   Debug: {config.debug}")


T = TypeVar("T")

class Registry:
    def __init__(self, name: str) -> None:
        self.name = name
        self._registry: dict[str, type] = {}

    def register(self, key: str) -> Callable:
        def decorator(cls: type) -> type:
            self._registry[key] = cls
            print(f"  📌 {self.name}: registered '{key}'")
            return cls
        return decorator

    def create(self, key: str, **kwargs) -> Any:
        if key not in self._registry:
            raise KeyError(f"{self.name}: '{key}' non enregistré")
        return self._registry[key](**kwargs)

    def list_registered(self) -> list[str]:
        return list(self._registry.keys())

    def __contains__(self, key: str) -> bool:
        return key in self._registry


enemy_registry = Registry("EnemyRegistry")

@enemy_registry.register("goblin")
class Goblin:
    def __init__(self, level: int = 1):
        self.name = "Goblin"; self.level = level; self.hp = 20 + level * 5
    def __repr__(self): return f"Goblin(lv.{self.level}, hp={self.hp})"

@enemy_registry.register("dragon")
class Dragon:
    def __init__(self, level: int = 10):
        self.name = "Dragon"; self.level = level; self.hp = 200 + level * 50
    def __repr__(self): return f"Dragon(lv.{self.level}, hp={self.hp})"

@enemy_registry.register("slime")
class Slime:
    def __init__(self, level: int = 1):
        self.name = "Slime"; self.level = level; self.hp = 10 + level * 2
    def __repr__(self): return f"Slime(lv.{self.level}, hp={self.hp})"

print(f"\n🗃️ Ennemis enregistrés : {enemy_registry.list_registered()}")
print(f"   Has goblin : {'goblin' in enemy_registry}")
goblin = enemy_registry.create("goblin", level=5)
dragon = enemy_registry.create("dragon", level=20)
print(f"\n🐲 Créés : {goblin}, {dragon}")


class Database:
    def __init__(self, url: str): self.url = url
    def query(self, sql: str) -> list[dict]:
        print(f"  🔍 DB Query: {sql}"); return [{"id": 1, "name": "Alice"}]

class MockDatabase(Database):
    def __init__(self): super().__init__("mock://memory")
    def query(self, sql: str) -> list[dict]: return [{"id": 999, "name": "TestPlayer"}]

class PlayerService:
    def __init__(self, db: Database, config: AppConfig) -> None:
        self.db = db; self.config = config
    def get_player(self, player_id: int) -> dict | None:
        results = self.db.query(f"SELECT * FROM players WHERE id = {player_id}")
        return results[0] if results else None

prod_service = PlayerService(db=Database(config.db_url), config=config)
test_service = PlayerService(db=MockDatabase(), config=AppConfig(debug=True))

print(f"\n🏭 Prod: {prod_service.get_player(1)}")
print(f"🧪 Test: {test_service.get_player(1)}")
print("\n✅ Exercice terminé avec succès !")
