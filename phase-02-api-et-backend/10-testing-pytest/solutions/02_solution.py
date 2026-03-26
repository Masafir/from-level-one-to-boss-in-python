"""Module 10 — Solution exercice à trou #2"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi import FastAPI, HTTPException, Depends
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()
_players_db = {1: {"id": 1, "name": "Alice", "score": 15000}, 2: {"id": 2, "name": "Bob", "score": 12000}}
def get_db(): return _players_db

@app.get("/players")
async def list_players(db: dict = Depends(get_db)): return list(db.values())

@app.get("/players/{player_id}")
async def get_player(player_id: int, db: dict = Depends(get_db)):
    if player_id not in db: raise HTTPException(status_code=404, detail="Player not found")
    return db[player_id]

class ScoreCreate(BaseModel):
    player_id: int; value: int

@app.post("/scores", status_code=201)
async def add_score(score: ScoreCreate, db: dict = Depends(get_db)):
    if score.player_id not in db: raise HTTPException(status_code=404, detail="Player not found")
    db[score.player_id]["score"] += score.value; return db[score.player_id]

@pytest.fixture
def client(): return TestClient(app)

@pytest.fixture
def mock_db(): return {1: {"id": 1, "name": "TestPlayer", "score": 0}}

def test_list_players(client):
    r = client.get("/players"); assert r.status_code == 200; assert len(r.json()) >= 2

def test_get_player(client):
    r = client.get("/players/1"); assert r.status_code == 200; assert r.json()["name"] == "Alice"

def test_player_not_found(client):
    r = client.get("/players/999"); assert r.status_code == 404; assert r.json()["detail"] == "Player not found"

def test_add_score(client):
    r = client.post("/scores", json={"player_id": 1, "value": 5000}); assert r.status_code == 201

def test_add_score_invalid_player(client):
    r = client.post("/scores", json={"player_id": 9999, "value": 100}); assert r.status_code == 404

def test_with_mock():
    db = Mock(); db.get_player.return_value = {"id": 1, "name": "Mocked"}
    result = db.get_player(1); assert result["name"] == "Mocked"
    db.get_player.assert_called_once_with(1)

def test_mock_side_effect():
    db = Mock(); db.get_player.side_effect = KeyError("Not found")
    with pytest.raises(KeyError): db.get_player(999)

def test_with_overridden_db(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    client = TestClient(app)
    r = client.get("/players"); assert len(r.json()) == 1; assert r.json()[0]["name"] == "TestPlayer"
    app.dependency_overrides.clear()

if __name__ == "__main__": pytest.main([__file__, "-v"])
