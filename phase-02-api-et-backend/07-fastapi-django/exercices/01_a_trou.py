"""
Module 07 — Exercice à trou #1
🎯 Thème : FastAPI — Routes, Pydantic, et CRUD basique

Complète les ___ pour que le code fonctionne.
Exécute avec : pip install "fastapi[standard]" httpx
              python 01_a_trou.py
"""

from enum import Enum
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

# ============================================================
# PARTIE 1 : Setup FastAPI
# ============================================================

app = ___(  # Quel objet créer ?
    title="Game Catalog API",
    description="API de catalogue de jeux vidéo",
    version="0.1.0",
)

# ============================================================
# PARTIE 2 : Enum pour les genres
# ============================================================

class Genre(str, ___):  # De quelle classe hériter pour un enum string ?
    RPG = "rpg"
    FPS = "fps"
    PUZZLE = "puzzle"
    PLATFORMER = "platformer"
    STRATEGY = "strategy"


# ============================================================
# PARTIE 3 : Pydantic models (validation)
# ============================================================

class GameCreate(___):  # De quelle classe Pydantic hériter ?
    """Schema pour créer un jeu."""
    title: str = Field(..., min_length=1, max_length=200)
    genre: Genre
    price: float = Field(..., ___=0, le=100)  # ge ou gt ? (greater or equal)
    year: int = Field(..., ge=1970, le=2030)
    tags: list[str] = ___  # Quelle valeur par défaut pour une liste ?


class GameResponse(BaseModel):
    """Schema de réponse."""
    id: int
    title: str
    genre: Genre
    price: float
    year: int
    tags: list[str]


class GameUpdate(BaseModel):
    """Schema pour une mise à jour partielle."""
    title: str | ___ = None  # Quel type pour "optionnel" ?
    genre: Genre | None = None
    price: float | None = None
    year: int | None = None
    tags: list[str] | None = None


# ============================================================
# PARTIE 4 : Base de données en mémoire
# ============================================================

games_db: dict[int, dict] = {}
_next_id: int = 1


def get_next_id() -> int:
    global _next_id
    current = _next_id
    _next_id += 1
    return current


# ============================================================
# PARTIE 5 : Routes CRUD
# ============================================================

@app.___(  "/games", status_code=201)  # Quelle méthode HTTP pour créer ?
async def create_game(game: GameCreate) -> GameResponse:
    """Crée un nouveau jeu."""
    game_id = get_next_id()
    game_dict = {"id": game_id, **game.model_dump()}
    games_db[game_id] = game_dict
    return GameResponse(**game_dict)


@app.___("/games")  # Quelle méthode HTTP pour lister ?
async def list_games(
    genre: Genre | None = None,
    min_price: float = 0,
    max_price: float = 100,
    limit: int = 10,
) -> list[GameResponse]:
    """Liste les jeux avec filtres optionnels."""
    results = list(games_db.values())
    
    if genre is not None:
        results = [g for g in results if g["genre"] == genre]
    
    results = [g for g in results if min_price <= g["price"] <= max_price]
    
    return [GameResponse(**g) for g in results[:limit]]


@app.get("/games/{game_id}")
async def get_game(game_id: ___) -> GameResponse:  # Quel type pour l'ID ?
    """Récupère un jeu par ID."""
    if game_id not in games_db:
        raise ___(status_code=404, detail="Game not found")
    return GameResponse(**games_db[game_id])


@app.___("/games/{game_id}")  # Quelle méthode HTTP pour une mise à jour partielle ?
async def update_game(game_id: int, update: GameUpdate) -> GameResponse:
    """Met à jour partiellement un jeu."""
    if game_id not in games_db:
        raise HTTPException(status_code=___, detail="Game not found")
    
    # exclude_unset=True : ne prend que les champs envoyés
    update_data = update.model_dump(exclude_unset=___)
    games_db[game_id].update(update_data)
    
    return GameResponse(**games_db[game_id])


@app.___("/games/{game_id}", status_code=204)  # Quelle méthode HTTP pour supprimer ?
async def delete_game(game_id: int):
    """Supprime un jeu."""
    if game_id not in games_db:
        raise HTTPException(status_code=404, detail="Game not found")
    del games_db[game_id]


# ============================================================
# PARTIE 6 : Tests avec TestClient
# ============================================================

if __name__ == "__main__":
    client = TestClient(app)
    
    print("🧪 Test de l'API\n")
    
    # Test CREATE
    response = client.post("/games", json={
        "title": "The Legend of Zelda",
        "genre": "rpg",
        "price": 59.99,
        "year": 2023,
        "tags": ["adventure", "open-world"],
    })
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    game = response.json()
    print(f"  ✅ CREATE: {game['title']} (id={game['id']})")
    game_id = game["id"]
    
    # Ajouter plus de jeux
    client.post("/games", json={"title": "Doom", "genre": "fps", "price": 29.99, "year": 2020})
    client.post("/games", json={"title": "Tetris", "genre": "puzzle", "price": 9.99, "year": 1984})
    
    # Test LIST
    response = client.get("/games")
    assert response.status_code == 200
    print(f"  ✅ LIST: {len(response.json())} games")
    
    # Test LIST with filter
    response = client.get("/games?genre=rpg")
    assert len(response.json()) == 1
    print(f"  ✅ FILTER: {len(response.json())} RPG games")
    
    # Test READ
    response = client.get(f"/games/{game_id}")
    assert response.status_code == 200
    print(f"  ✅ READ: {response.json()['title']}")
    
    # Test 404
    response = client.get("/games/999")
    assert response.status_code == 404
    print(f"  ✅ 404: {response.json()['detail']}")
    
    # Test UPDATE
    response = client.patch(f"/games/{game_id}", json={"price": 39.99})
    assert response.status_code == 200
    assert response.json()["price"] == 39.99
    print(f"  ✅ UPDATE: price → {response.json()['price']}")
    
    # Test DELETE
    response = client.delete(f"/games/{game_id}")
    assert response.status_code == 204
    print(f"  ✅ DELETE: game {game_id}")
    
    # Test validation
    response = client.post("/games", json={"title": "", "genre": "rpg", "price": -5, "year": 2020})
    assert response.status_code == 422
    print(f"  ✅ VALIDATION: 422 error on invalid data")
    
    print("\n✅ Tous les tests passés !")
