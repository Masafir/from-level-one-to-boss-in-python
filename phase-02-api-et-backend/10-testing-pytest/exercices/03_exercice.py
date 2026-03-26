"""
Module 10 — Exercice complet #3
🎯 Thème : Suite de tests complète pour une API de jeu

Écris tous les tests pour valider une API de gestion de tournois.

Exécute avec : pytest 03_exercice.py -v --tb=short
"""

import pytest
from fastapi import FastAPI, HTTPException, Depends
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from dataclasses import dataclass, field
from enum import Enum

# ============================================================
# CODE DE L'API (À NE PAS MODIFIER)
# ============================================================

class TournamentStatus(str, Enum):
    DRAFT = "draft"
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"

class TournamentCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    max_players: int = Field(..., ge=2, le=64)
    genre: str

class ParticipantCreate(BaseModel):
    player_name: str
    rank: int = 0

app = FastAPI(title="Tournament API")
tournaments: dict[int, dict] = {}
_tid = 1

@app.post("/tournaments", status_code=201)
async def create_tournament(t: TournamentCreate):
    global _tid
    data = {"id": _tid, **t.model_dump(), "status": "draft", "participants": []}
    tournaments[_tid] = data; _tid += 1
    return data

@app.get("/tournaments")
async def list_tournaments(status: str | None = None):
    results = list(tournaments.values())
    if status: results = [t for t in results if t["status"] == status]
    return results

@app.get("/tournaments/{tid}")
async def get_tournament(tid: int):
    if tid not in tournaments: raise HTTPException(404, "Not found")
    return tournaments[tid]

@app.post("/tournaments/{tid}/open")
async def open_tournament(tid: int):
    if tid not in tournaments: raise HTTPException(404, "Not found")
    t = tournaments[tid]
    if t["status"] != "draft": raise HTTPException(400, "Can only open draft tournaments")
    t["status"] = "open"
    return t

@app.post("/tournaments/{tid}/join")
async def join_tournament(tid: int, p: ParticipantCreate):
    if tid not in tournaments: raise HTTPException(404, "Not found")
    t = tournaments[tid]
    if t["status"] != "open": raise HTTPException(400, "Tournament not open")
    if len(t["participants"]) >= t["max_players"]: raise HTTPException(400, "Tournament full")
    if any(pp["player_name"] == p.player_name for pp in t["participants"]):
        raise HTTPException(400, "Already joined")
    t["participants"].append(p.model_dump())
    return t

@app.delete("/tournaments/{tid}", status_code=204)
async def delete_tournament(tid: int):
    if tid not in tournaments: raise HTTPException(404, "Not found")
    del tournaments[tid]


# ============================================================
# TON TRAVAIL : ÉCRIRE LES TESTS
# ============================================================

# TODO : Implémenter les tests suivants

# 1. Fixtures
#    - client : TestClient
#    - sample_tournament : crée un tournoi et retourne son ID
#    - open_tournament : crée et ouvre un tournoi
#    - autouse fixture pour reset la DB entre les tests

# 2. Tests CRUD basiques (au moins 8 tests)
#    - test_create_tournament
#    - test_create_tournament_validation (nom trop court, max_players invalide)
#    - test_list_tournaments
#    - test_list_tournaments_filter_by_status
#    - test_get_tournament
#    - test_get_tournament_not_found
#    - test_delete_tournament
#    - test_delete_tournament_not_found

# 3. Tests du workflow (au moins 5 tests)
#    - test_open_tournament
#    - test_open_already_open_tournament
#    - test_join_tournament
#    - test_join_full_tournament
#    - test_join_duplicate_player
#    - test_join_draft_tournament

# 4. Tests paramétriques
#    - test_valid_tournament_names (plusieurs noms valides)
#    - test_invalid_max_players (0, 1, 65, -1)

# 5. Tests d'intégration
#    - test_full_tournament_lifecycle : create → open → join → verify


# ============================================================
# MAIN — Lancer les tests
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
