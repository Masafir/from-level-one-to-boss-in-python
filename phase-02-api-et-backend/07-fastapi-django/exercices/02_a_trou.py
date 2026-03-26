"""
Module 07 — Exercice à trou #2
🎯 Thème : FastAPI — Dependency Injection, Router et Middleware

Complète les ___ pour que le code fonctionne.
Exécute avec : python 02_a_trou.py
"""

import time
from fastapi import FastAPI, Depends, HTTPException, Header, Request, APIRouter
from fastapi.testclient import TestClient
from pydantic import BaseModel

# ============================================================
# PARTIE 1 : Dépendances
# ============================================================

# Simule une base de données
class FakeDB:
    def __init__(self):
        self.data = {
            1: {"id": 1, "name": "Alice", "score": 15000, "role": "admin"},
            2: {"id": 2, "name": "Bob", "score": 12000, "role": "player"},
            3: {"id": 3, "name": "Charlie", "score": 9000, "role": "player"},
        }
    
    def get_player(self, player_id: int) -> dict | None:
        return self.data.get(player_id)
    
    def list_players(self) -> list[dict]:
        return list(self.data.values())

_db = FakeDB()


# Dépendance : fournir la DB
def get_db() -> FakeDB:
    """Fournit l'instance de la base de données."""
    return _db


# Dépendance : vérifier le token
async def verify_token(authorization: str = ___()):  # Quel built-in FastAPI pour lire un header ?
    """Vérifie que le header Authorization contient un token valide."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=___,  # Quel code HTTP pour "non autorisé" ?
            detail="Token manquant ou invalide",
        )
    token = authorization.replace("Bearer ", "")
    if token != "super-secret-token":
        raise HTTPException(status_code=401, detail="Token invalide")
    return token


# Dépendance : récupérer l'utilisateur courant (dépend de verify_token)
async def get_current_user(
    token: str = ___(verify_token),  # Quel built-in FastAPI pour injecter une dépendance ?
    db: FakeDB = Depends(get_db),
):
    """Récupère l'utilisateur à partir du token."""
    # Ici on simule : token valide = user id 1
    user = db.get_player(1)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# Dépendance : vérifier le rôle admin
async def require_admin(
    user: dict = Depends(___),  # Quelle dépendance pour l'utilisateur ?
):
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=___,  # Quel code HTTP pour "interdit" (pas les droits) ?
            detail="Admin access required",
        )
    return user


# ============================================================
# PARTIE 2 : Router
# ============================================================

player_router = ___(  # Quel objet FastAPI pour un sous-routeur ?
    prefix="/players",
    tags=["Players"],
)

admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_admin)],  # Toutes les routes sont protégées !
)

@player_router.get("/")
async def list_players(db: FakeDB = Depends(get_db)):
    return db.list_players()

@player_router.get("/me")
async def get_me(user: dict = Depends(get_current_user)):
    return user

@player_router.get("/{player_id}")
async def get_player(player_id: int, db: FakeDB = Depends(get_db)):
    player = db.get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@admin_router.get("/stats")
async def admin_stats(db: FakeDB = Depends(get_db)):
    players = db.list_players()
    return {
        "total_players": len(players),
        "average_score": sum(p["score"] for p in players) / len(players),
    }


# ============================================================
# PARTIE 3 : App avec middleware
# ============================================================

app = FastAPI(title="Game API v2")

# Middleware : mesurer le temps de réponse
@app.___(  "http")  # Quel decorator pour un middleware ?
async def timing_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = ___ call_next(request)  # Quel mot-clé pour appeler une coroutine ?
    elapsed = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{elapsed:.4f}"
    return response


# Middleware : logging
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    print(f"  📥 {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"  📤 {response.status_code}")
    return response


# Inclure les routers
app.include_router(player_router)
app.include_router(admin_router)


# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":
    client = TestClient(app)
    headers = {"Authorization": "Bearer super-secret-token"}
    
    print("🧪 Test API v2\n")
    
    # Public routes
    r = client.get("/players/")
    assert r.status_code == 200
    print(f"  ✅ List players: {len(r.json())} players")
    
    r = client.get("/players/1")
    assert r.status_code == 200
    print(f"  ✅ Get player: {r.json()['name']}")
    
    r = client.get("/players/999")
    assert r.status_code == 404
    print(f"  ✅ 404: {r.json()['detail']}")
    
    # Auth routes
    r = client.get("/players/me")
    assert r.status_code == 422 or r.status_code == 401
    print(f"  ✅ No token: {r.status_code}")
    
    r = client.get("/players/me", headers=headers)
    assert r.status_code == 200
    print(f"  ✅ With token: {r.json()['name']}")
    
    # Admin routes
    r = client.get("/admin/stats", headers=headers)
    assert r.status_code == 200
    print(f"  ✅ Admin stats: {r.json()}")
    
    # Check timing header
    assert "x-process-time" in r.headers
    print(f"  ✅ Timing header: {r.headers['x-process-time']}s")
    
    print("\n✅ Tous les tests passés !")
