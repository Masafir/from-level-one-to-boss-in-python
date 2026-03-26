"""Module 07 — Solution exercice à trou #1"""

from enum import Enum
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

app = FastAPI(title="Game Catalog API", description="API de catalogue de jeux vidéo", version="0.1.0")

class Genre(str, Enum):
    RPG = "rpg"; FPS = "fps"; PUZZLE = "puzzle"; PLATFORMER = "platformer"; STRATEGY = "strategy"

class GameCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    genre: Genre
    price: float = Field(..., ge=0, le=100)
    year: int = Field(..., ge=1970, le=2030)
    tags: list[str] = []

class GameResponse(BaseModel):
    id: int; title: str; genre: Genre; price: float; year: int; tags: list[str]

class GameUpdate(BaseModel):
    title: str | None = None; genre: Genre | None = None; price: float | None = None
    year: int | None = None; tags: list[str] | None = None

games_db: dict[int, dict] = {}
_next_id: int = 1

def get_next_id() -> int:
    global _next_id; current = _next_id; _next_id += 1; return current

@app.post("/games", status_code=201)
async def create_game(game: GameCreate) -> GameResponse:
    game_id = get_next_id()
    game_dict = {"id": game_id, **game.model_dump()}
    games_db[game_id] = game_dict
    return GameResponse(**game_dict)

@app.get("/games")
async def list_games(genre: Genre | None = None, min_price: float = 0, max_price: float = 100, limit: int = 10) -> list[GameResponse]:
    results = list(games_db.values())
    if genre is not None:
        results = [g for g in results if g["genre"] == genre]
    results = [g for g in results if min_price <= g["price"] <= max_price]
    return [GameResponse(**g) for g in results[:limit]]

@app.get("/games/{game_id}")
async def get_game(game_id: int) -> GameResponse:
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Game not found")
    return GameResponse(**games_db[game_id])

@app.patch("/games/{game_id}")
async def update_game(game_id: int, update: GameUpdate) -> GameResponse:
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Game not found")
    update_data = update.model_dump(exclude_unset=True)
    games_db[game_id].update(update_data)
    return GameResponse(**games_db[game_id])

@app.delete("/games/{game_id}", status_code=204)
async def delete_game(game_id: int):
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Game not found")
    del games_db[game_id]

if __name__ == "__main__":
    client = TestClient(app)
    print("🧪 Test de l'API\n")
    r = client.post("/games", json={"title": "The Legend of Zelda", "genre": "rpg", "price": 59.99, "year": 2023, "tags": ["adventure"]})
    assert r.status_code == 201; game = r.json(); print(f"  ✅ CREATE: {game['title']} (id={game['id']})")
    game_id = game["id"]
    client.post("/games", json={"title": "Doom", "genre": "fps", "price": 29.99, "year": 2020})
    client.post("/games", json={"title": "Tetris", "genre": "puzzle", "price": 9.99, "year": 1984})
    r = client.get("/games"); assert r.status_code == 200; print(f"  ✅ LIST: {len(r.json())} games")
    r = client.get("/games?genre=rpg"); assert len(r.json()) == 1; print(f"  ✅ FILTER: {len(r.json())} RPG")
    r = client.get(f"/games/{game_id}"); assert r.status_code == 200; print(f"  ✅ READ: {r.json()['title']}")
    r = client.get("/games/999"); assert r.status_code == 404; print(f"  ✅ 404: {r.json()['detail']}")
    r = client.patch(f"/games/{game_id}", json={"price": 39.99}); assert r.json()["price"] == 39.99; print(f"  ✅ UPDATE: price → {r.json()['price']}")
    r = client.delete(f"/games/{game_id}"); assert r.status_code == 204; print(f"  ✅ DELETE: game {game_id}")
    r = client.post("/games", json={"title": "", "genre": "rpg", "price": -5, "year": 2020}); assert r.status_code == 422; print(f"  ✅ VALIDATION: 422")
    print("\n✅ Tous les tests passés !")
