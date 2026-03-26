"""
Module 07 — Exercice complet #3
🎯 Thème : API complète de catalogue de jeux vidéo avec FastAPI

Objectif : Créer une API REST complète pour un catalogue de jeux vidéo
avec validation, filtres, pagination, et statistiques.

Exécute avec : pip install "fastapi[standard]" httpx
              python 03_exercice.py
"""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.testclient import TestClient


# ============================================================
# MODÈLES
# ============================================================

class Genre(str, Enum):
    RPG = "rpg"
    FPS = "fps"
    PUZZLE = "puzzle"
    PLATFORMER = "platformer"
    STRATEGY = "strategy"
    SIMULATION = "simulation"


class SortField(str, Enum):
    TITLE = "title"
    PRICE = "price"
    YEAR = "year"
    RATING = "rating"


class GameCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    genre: Genre
    price: float = Field(..., ge=0, le=200)
    year: int = Field(..., ge=1970, le=2030)
    developer: str = Field(..., min_length=1)
    rating: float = Field(default=0, ge=0, le=10)
    tags: list[str] = []


class GameResponse(BaseModel):
    id: int
    title: str
    genre: Genre
    price: float
    year: int
    developer: str
    rating: float
    tags: list[str]
    created_at: str


class PaginatedResponse(BaseModel):
    items: list[GameResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


# BDD en mémoire
games_db: dict[int, dict] = {}
_next_id = 1


# Seed data
SEED_DATA = [
    {"title": "The Legend of Zelda: TOTK", "genre": "rpg", "price": 59.99, "year": 2023, "developer": "Nintendo", "rating": 9.5, "tags": ["adventure", "open-world"]},
    {"title": "Doom Eternal", "genre": "fps", "price": 29.99, "year": 2020, "developer": "id Software", "rating": 8.8, "tags": ["action", "fast-paced"]},
    {"title": "Tetris Effect", "genre": "puzzle", "price": 19.99, "year": 2018, "developer": "Enhance", "rating": 9.0, "tags": ["relaxing", "vr"]},
    {"title": "Hollow Knight", "genre": "platformer", "price": 14.99, "year": 2017, "developer": "Team Cherry", "rating": 9.2, "tags": ["metroidvania", "indie"]},
    {"title": "Civilization VI", "genre": "strategy", "price": 39.99, "year": 2016, "developer": "Firaxis", "rating": 8.5, "tags": ["4x", "turn-based"]},
    {"title": "Elden Ring", "genre": "rpg", "price": 49.99, "year": 2022, "developer": "FromSoftware", "rating": 9.8, "tags": ["souls-like", "open-world"]},
    {"title": "Celeste", "genre": "platformer", "price": 9.99, "year": 2018, "developer": "Maddy Makes Games", "rating": 9.3, "tags": ["indie", "precision"]},
    {"title": "Portal 2", "genre": "puzzle", "price": 9.99, "year": 2011, "developer": "Valve", "rating": 9.6, "tags": ["physics", "coop"]},
    {"title": "Stardew Valley", "genre": "simulation", "price": 14.99, "year": 2016, "developer": "ConcernedApe", "rating": 9.1, "tags": ["farming", "indie"]},
    {"title": "Hades", "genre": "rpg", "price": 24.99, "year": 2020, "developer": "Supergiant", "rating": 9.4, "tags": ["roguelike", "indie"]},
]


app = FastAPI(title="Game Catalog API", version="1.0.0")


# ============================================================
# TODO : Implémenter les endpoints suivants
# ============================================================

# POST /games — Créer un jeu
# GET /games — Lister avec filtres, tri, pagination
# GET /games/{id} — Détail d'un jeu
# PUT /games/{id} — Remplacer un jeu
# PATCH /games/{id} — Mise à jour partielle
# DELETE /games/{id} — Supprimer
# GET /games/stats/overview — Statistiques globales
# GET /games/stats/by-genre — Statistiques par genre
# GET /games/search — Recherche full-text dans titre et tags


def seed_database():
    """
    TODO: Implémenter le seeding de la BDD.
    Ajoute tous les jeux de SEED_DATA dans games_db.
    """
    pass


def create_game_endpoint():
    """
    TODO: POST /games
    - Valide avec GameCreate
    - Ajoute created_at (datetime ISO)
    - Retourne GameResponse + status 201
    """
    pass


def list_games_endpoint():
    """
    TODO: GET /games
    
    Query params :
    - genre (optionnel) : filtrer par genre
    - min_price, max_price : filtre de prix
    - min_rating : filtre par note min
    - developer : filtre par développeur (case insensitive, partiel)
    - tag : filtre par tag
    - sort_by : champ de tri (title, price, year, rating)
    - sort_desc : booléen pour tri descendant
    - page : numéro de page (default 1)
    - per_page : items par page (default 10, max 50)
    
    Retourne PaginatedResponse
    """
    pass


def get_stats_overview():
    """
    TODO: GET /games/stats/overview
    
    Retourne :
    {
        "total_games": 10,
        "average_price": 27.39,
        "average_rating": 9.22,
        "price_range": {"min": 9.99, "max": 59.99},
        "year_range": {"min": 2011, "max": 2023},
        "top_rated": {"title": "Elden Ring", "rating": 9.8},
        "cheapest": {"title": "Celeste", "price": 9.99},
        "most_expensive": {"title": "Zelda", "price": 59.99},
    }
    """
    pass


def get_stats_by_genre():
    """
    TODO: GET /games/stats/by-genre
    
    Retourne pour chaque genre :
    {
        "rpg": {
            "count": 3,
            "average_price": 44.99,
            "average_rating": 9.57,
            "games": ["Elden Ring", "Zelda", "Hades"]
        },
        ...
    }
    """
    pass


def search_games():
    """
    TODO: GET /games/search?q=indie
    
    Recherche dans le titre ET les tags (case insensitive).
    Retourne les jeux triés par pertinence (titre match > tag match).
    """
    pass


# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":
    # Seed la BDD
    seed_database()
    
    client = TestClient(app)
    print("🧪 Test Game Catalog API\n")
    
    # Si les endpoints ne sont pas encore implémentés, ça va 404
    # Implémente-les un par un et décommente les tests !
    
    # Test list
    # r = client.get("/games")
    # print(f"  Games: {len(r.json()['items'])} / {r.json()['total']}")
    
    # Test filter by genre
    # r = client.get("/games?genre=rpg")
    # print(f"  RPGs: {len(r.json()['items'])}")
    
    # Test pagination
    # r = client.get("/games?page=1&per_page=3")
    # print(f"  Page 1: {len(r.json()['items'])} items, {r.json()['total_pages']} pages")
    
    # Test stats
    # r = client.get("/games/stats/overview")
    # print(f"  Stats: avg price={r.json()['average_price']}")
    
    # Test search
    # r = client.get("/games/search?q=indie")
    # print(f"  Search 'indie': {len(r.json())} results")
    
    print("\n✅ Tests terminés !")
