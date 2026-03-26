"""
Module 10 — Exercice à trou #2
🎯 Thème : Mocking, FastAPI TestClient, fixtures avancées

Complète les ___ pour que les tests passent.
Exécute avec : pip install fastapi httpx pytest
              pytest 02_a_trou.py -v
"""

import pytest
from unittest.mock import Mock, patch, ___ as AsyncMock  # Quel import pour les mocks async ?
from fastapi import FastAPI, HTTPException, Depends
from fastapi.testclient import ___  # Quel import pour le client de test ?
from pydantic import BaseModel

# ============================================================
# CODE À TESTER — API FastAPI
# ============================================================

app = FastAPI()

# Fake DB
_players_db = {
    1: {"id": 1, "name": "Alice", "score": 15000},
    2: {"id": 2, "name": "Bob", "score": 12000},
}

def get_db():
    return _players_db

@app.get("/players")
async def list_players(db: dict = Depends(get_db)):
    return list(db.values())

@app.get("/players/{player_id}")
async def get_player(player_id: int, db: dict = Depends(get_db)):
    if player_id not in db:
        raise HTTPException(status_code=404, detail="Player not found")
    return db[player_id]

class ScoreCreate(BaseModel):
    player_id: int
    value: int

@app.post("/scores", status_code=201)
async def add_score(score: ScoreCreate, db: dict = Depends(get_db)):
    if score.player_id not in db:
        raise HTTPException(status_code=404, detail="Player not found")
    db[score.player_id]["score"] += score.value
    return db[score.player_id]


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def ___():  # Nomme cette fixture correctement
    """Client de test pour l'API."""
    return TestClient(app)


@pytest.fixture
def mock_db():
    """Base de données mockée."""
    return {
        1: {"id": 1, "name": "TestPlayer", "score": 0},
    }


# ============================================================
# TESTS DE L'API
# ============================================================

def test_list_players(client):
    response = client.___(  "/players")  # Quelle méthode HTTP ?
    assert response.status_code == ___  # Quel status code ?
    data = response.json()
    assert len(data) >= 2


def test_get_player(client):
    response = client.get("/players/1")
    assert response.status_code == 200
    data = response.___()  # Quelle méthode pour parser le JSON ?
    assert data["name"] == "Alice"


def test_player_not_found(client):
    response = client.get("/players/999")
    assert response.status_code == ___  # Quel code pour "non trouvé" ?
    assert response.json()["detail"] == "Player not found"


def test_add_score(client):
    response = client.post("/scores", ___={  # Quel paramètre pour envoyer du JSON ?
        "player_id": 1,
        "value": 5000,
    })
    assert response.status_code == 201


def test_add_score_invalid_player(client):
    response = client.post("/scores", json={
        "player_id": 9999,
        "value": 100,
    })
    assert response.status_code == ___  # Quel code ?


# ============================================================
# TESTS AVEC MOCKING
# ============================================================

def test_with_mock():
    """Test avec un Mock simple."""
    db = ___()  # Créer un mock
    db.get_player.return_value = {"id": 1, "name": "Mocked"}
    
    result = db.get_player(1)
    assert result["name"] == "Mocked"
    db.get_player.___(1)  # Vérifier que le mock a été appelé avec 1


def test_mock_side_effect():
    """Test un mock qui lève une exception."""
    db = Mock()
    db.get_player.side_effect = ___("Not found")  # Quelle exception ?
    
    with pytest.raises(KeyError):
        db.get_player(999)


# ============================================================
# TESTS AVEC DEPENDENCY OVERRIDE
# ============================================================

def test_with_overridden_db(mock_db):
    """Utilise dependency override pour injecter un mock."""
    def override_get_db():
        return mock_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    client = TestClient(app)
    response = client.get("/players")
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "TestPlayer"
    
    # Cleanup !
    app.dependency_overrides.clear()


# ============================================================
# CHECK — Lancer les tests
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
