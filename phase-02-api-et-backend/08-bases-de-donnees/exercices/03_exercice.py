"""
Module 08 — Exercice complet #3
🎯 Thème : API de Leaderboard avec FastAPI + SQLAlchemy

Crée une API de leaderboard de jeux vidéo.

Exécute avec : pip install fastapi sqlalchemy httpx
              python 03_exercice.py
"""

from sqlalchemy import create_engine, String, Integer, Float, ForeignKey, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from pydantic import BaseModel, Field
from fastapi import FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient


# ============================================================
# PARTIE 1 : Modèles SQLAlchemy
# ============================================================

class Base(DeclarativeBase):
    pass

# TODO : Crée les modèles suivants :

# Player : id, username (unique), country, created_at
# Game : id, title, genre, max_score
# Score : id, value, player_id (FK), game_id (FK), achieved_at
# Avec les relations appropriées


# ============================================================
# PARTIE 2 : Pydantic Schemas
# ============================================================

# TODO : Crée les schemas pour :
# PlayerCreate, PlayerResponse
# GameCreate, GameResponse
# ScoreCreate, ScoreResponse
# LeaderboardEntry (rank, player_name, score, country)


# ============================================================
# PARTIE 3 : Database dependency
# ============================================================

engine = create_engine("sqlite:///:memory:", echo=False)
# TODO : Créer les tables
# TODO : Créer la dependency get_db() pour FastAPI


# ============================================================
# PARTIE 4 : Endpoints
# ============================================================

app = FastAPI(title="Leaderboard API")

# TODO : Implémenter :

# POST /players — Créer un joueur
# GET /players — Lister les joueurs
# GET /players/{id} — Détail avec ses scores

# POST /games — Créer un jeu
# GET /games — Lister les jeux

# POST /scores — Enregistrer un score
# GET /games/{game_id}/leaderboard — Top 10 du jeu
#   Retourne : rank, player_name, score, country
#   Tri par score descendant

# GET /players/{id}/stats — Stats d'un joueur
#   Retourne : total_games_played, average_score, best_score, favorite_genre

# GET /leaderboard/global — Classement global
#   Agrège les meilleurs scores de chaque joueur


# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":
    client = TestClient(app)
    print("🧪 Test Leaderboard API\n")
    
    # Décommenter au fur et à mesure
    
    # # Create players
    # for p in [("Alice", "FR"), ("Bob", "US"), ("Charlie", "JP")]:
    #     r = client.post("/players", json={"username": p[0], "country": p[1]})
    #     assert r.status_code == 201
    # print("  ✅ Players created")
    
    # # Create games
    # for g in [("Zelda", "rpg", 99999), ("Tetris", "puzzle", 999999)]:
    #     r = client.post("/games", json={"title": g[0], "genre": g[1], "max_score": g[2]})
    #     assert r.status_code == 201
    # print("  ✅ Games created")
    
    # # Add scores
    # scores = [(1,1,15000), (2,1,12000), (3,1,18000), (1,2,50000), (2,2,45000)]
    # for pid, gid, val in scores:
    #     r = client.post("/scores", json={"player_id": pid, "game_id": gid, "value": val})
    #     assert r.status_code == 201
    # print("  ✅ Scores added")
    
    # # Leaderboard
    # r = client.get("/games/1/leaderboard")
    # assert r.status_code == 200
    # print(f"  ✅ Leaderboard Zelda: {r.json()}")
    
    # # Player stats
    # r = client.get("/players/1/stats")
    # assert r.status_code == 200
    # print(f"  ✅ Alice stats: {r.json()}")
    
    print("\n✅ Tests terminés !")
