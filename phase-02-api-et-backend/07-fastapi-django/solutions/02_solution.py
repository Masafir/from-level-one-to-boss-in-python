"""Module 07 — Solution exercice à trou #2"""

import time
from fastapi import FastAPI, Depends, HTTPException, Header, Request, APIRouter
from fastapi.testclient import TestClient
from pydantic import BaseModel

class FakeDB:
    def __init__(self):
        self.data = {
            1: {"id": 1, "name": "Alice", "score": 15000, "role": "admin"},
            2: {"id": 2, "name": "Bob", "score": 12000, "role": "player"},
            3: {"id": 3, "name": "Charlie", "score": 9000, "role": "player"},
        }
    def get_player(self, player_id: int) -> dict | None: return self.data.get(player_id)
    def list_players(self) -> list[dict]: return list(self.data.values())

_db = FakeDB()
def get_db() -> FakeDB: return _db

async def verify_token(authorization: str = Header()):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token manquant ou invalide")
    token = authorization.replace("Bearer ", "")
    if token != "super-secret-token":
        raise HTTPException(status_code=401, detail="Token invalide")
    return token

async def get_current_user(token: str = Depends(verify_token), db: FakeDB = Depends(get_db)):
    user = db.get_player(1)
    if not user: raise HTTPException(status_code=401, detail="User not found")
    return user

async def require_admin(user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

player_router = APIRouter(prefix="/players", tags=["Players"])
admin_router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(require_admin)])

@player_router.get("/")
async def list_players(db: FakeDB = Depends(get_db)): return db.list_players()

@player_router.get("/me")
async def get_me(user: dict = Depends(get_current_user)): return user

@player_router.get("/{player_id}")
async def get_player(player_id: int, db: FakeDB = Depends(get_db)):
    player = db.get_player(player_id)
    if not player: raise HTTPException(status_code=404, detail="Player not found")
    return player

@admin_router.get("/stats")
async def admin_stats(db: FakeDB = Depends(get_db)):
    players = db.list_players()
    return {"total_players": len(players), "average_score": sum(p["score"] for p in players) / len(players)}

app = FastAPI(title="Game API v2")

@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.4f}"
    return response

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    print(f"  📥 {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"  📤 {response.status_code}")
    return response

app.include_router(player_router)
app.include_router(admin_router)

if __name__ == "__main__":
    client = TestClient(app)
    headers = {"Authorization": "Bearer super-secret-token"}
    print("🧪 Test API v2\n")
    r = client.get("/players/"); assert r.status_code == 200; print(f"  ✅ List: {len(r.json())} players")
    r = client.get("/players/1"); assert r.status_code == 200; print(f"  ✅ Get: {r.json()['name']}")
    r = client.get("/players/999"); assert r.status_code == 404; print(f"  ✅ 404: {r.json()['detail']}")
    r = client.get("/players/me", headers=headers); assert r.status_code == 200; print(f"  ✅ Auth: {r.json()['name']}")
    r = client.get("/admin/stats", headers=headers); assert r.status_code == 200; print(f"  ✅ Admin: {r.json()}")
    assert "x-process-time" in r.headers; print(f"  ✅ Timing: {r.headers['x-process-time']}s")
    print("\n✅ Tous les tests passés !")
