# Module 10 — Testing avec Pytest 🧪

> **Objectif** : Écrire des tests comme un pro Python. Pytest est le standard — plus puissant et élégant que Jest/Mocha.

## 1. Pytest vs Jest

| | **Pytest** | **Jest** |
|--|---------|------|
| **Install** | `pip install pytest` | `npm install jest` |
| **Run** | `pytest` | `jest` |
| **Assertions** | `assert x == y` (natif Python !) | `expect(x).toBe(y)` |
| **Fixtures** | `@pytest.fixture` | `beforeEach` / `afterEach` |
| **Mock** | `pytest-mock` / `unittest.mock` | `jest.mock()` |
| **Coverage** | `pytest-cov` | `jest --coverage` |
| **Paramétrage** | `@pytest.mark.parametrize` | `test.each()` |

```bash
pip install pytest pytest-cov pytest-asyncio httpx
```

## 2. Les bases

```python
# tests/test_math.py

# Test = une fonction qui commence par test_
def test_addition():
    assert 1 + 1 == 2

def test_string():
    name = "Alice"
    assert name.upper() == "ALICE"
    assert "lic" in name

# Test d'exception
import pytest

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0

def test_custom_exception():
    with pytest.raises(ValueError, match="invalide"):
        raise ValueError("valeur invalide")
```

```bash
# Lancer les tests
pytest                    # Tout
pytest tests/test_math.py # Un fichier
pytest -v                 # Verbose
pytest -x                 # Stop au premier échec
pytest -k "test_add"      # Par nom
pytest --tb=short         # Traceback court
```

## 3. Fixtures — Le setup/teardown intelligent

```python
import pytest
from dataclasses import dataclass

@dataclass
class Player:
    name: str
    hp: int = 100
    level: int = 1

# Fixture = une dépendance injectée automatiquement
@pytest.fixture
def player():
    """Crée un joueur pour les tests."""
    return Player(name="TestPlayer", hp=100, level=5)

@pytest.fixture
def inventory():
    """Crée un inventaire avec des items."""
    return ["sword", "shield", "potion"]

# Utilisation : le nom de la fixture = le nom du paramètre
def test_player_hp(player):
    assert player.hp == 100

def test_player_take_damage(player):
    player.hp -= 25
    assert player.hp == 75

def test_inventory_has_items(inventory):
    assert len(inventory) == 3
    assert "sword" in inventory

# Combine plusieurs fixtures !
def test_player_with_inventory(player, inventory):
    assert player.name == "TestPlayer"
    assert len(inventory) == 3
```

### Fixtures avec yield (setup/teardown)

```python
@pytest.fixture
def database():
    """Setup et teardown de la base de données."""
    db = {"players": {}, "games": {}}
    print("  🔧 DB setup")
    yield db  # <-- Le test s'exécute ici
    print("  🧹 DB cleanup")
    db.clear()

# Fixture de scope (shared entre les tests)
@pytest.fixture(scope="module")  # Partagé dans tout le fichier
def config():
    return {"debug": True, "db_url": "sqlite:///:memory:"}
```

### conftest.py — Fixtures partagées

```python
# tests/conftest.py — Automatiquement découvert par pytest
import pytest

@pytest.fixture
def sample_player():
    return Player(name="Alice", hp=100, level=42)

# Disponible dans TOUS les tests du dossier !
```

## 4. Parametrize — Tester plusieurs cas

```python
@pytest.mark.parametrize("damage,expected_hp", [
    (10, 90),
    (50, 50),
    (100, 0),
    (150, 0),  # Clamp à 0
])
def test_take_damage(damage, expected_hp):
    player = Player(name="Test", hp=100)
    player.hp = max(0, player.hp - damage)
    assert player.hp == expected_hp

@pytest.mark.parametrize("input_str,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("", ""),
    ("123abc", "123ABC"),
])
def test_upper(input_str, expected):
    assert input_str.upper() == expected
```

## 5. Mocking

```python
from unittest.mock import Mock, patch, AsyncMock

# Mock simple
def test_with_mock():
    db = Mock()
    db.get_player.return_value = {"id": 1, "name": "Alice"}
    
    result = db.get_player(1)
    assert result["name"] == "Alice"
    db.get_player.assert_called_once_with(1)

# Patch — remplacer temporairement un module/objet
def fetch_data():
    import requests
    return requests.get("https://api.example.com/data").json()

@patch("requests.get")
def test_fetch_data(mock_get):
    mock_get.return_value.json.return_value = {"status": "ok"}
    result = fetch_data()
    assert result == {"status": "ok"}

# Mock async
async def test_async_service():
    service = AsyncMock()
    service.get_player.return_value = {"id": 1}
    result = await service.get_player(1)
    assert result == {"id": 1}
```

## 6. Tester FastAPI

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient  # Client synchrone
import pytest

app = FastAPI()

@app.get("/players/{id}")
async def get_player(id: int):
    return {"id": id, "name": f"Player_{id}"}

# TestClient = l'équivalent de supertest en Node
@pytest.fixture
def client():
    return TestClient(app)

def test_get_player(client):
    response = client.get("/players/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Player_1"

def test_player_not_found(client):
    response = client.get("/players/abc")  # int attendu
    assert response.status_code == 422  # Validation error

# Tester avec auth
def test_auth_required(client):
    response = client.get("/protected")
    assert response.status_code == 401

def test_with_token(client):
    headers = {"Authorization": "Bearer valid-token"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
```

## 7. Coverage

```bash
# Lancer avec coverage
pytest --cov=src --cov-report=term-missing

# Rapport HTML
pytest --cov=src --cov-report=html
# Ouvre htmlcov/index.html

# Minimum de coverage
pytest --cov=src --cov-fail-under=80
```

---

## 🎯 Résumé

| Concept | Ce qu'il faut retenir |
|---------|----------------------|
| **assert** | Pas besoin de `assertEqual()`, juste `assert` ! |
| **Fixture** | Injection de dépendances pour les tests |
| **conftest.py** | Fixtures partagées entre les fichiers |
| **parametrize** | Tester N cas avec un seul test |
| **Mock/patch** | Remplacer les dépendances externes |
| **TestClient** | Tester les APIs FastAPI (comme supertest) |
| **Coverage** | `pytest --cov` pour mesurer la couverture |

---

➡️ **Passe aux exercices dans `exercices/` !**
