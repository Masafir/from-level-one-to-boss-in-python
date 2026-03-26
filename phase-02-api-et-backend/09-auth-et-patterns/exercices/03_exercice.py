"""
Module 09 — Exercice complet #3
🎯 Thème : API sécurisée avec auth complète

Crée une API de jeu multijoueur avec authentification,
RBAC, rate limiting et event bus.

Exécute avec : pip install fastapi passlib[bcrypt] httpx
              python 03_exercice.py
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient

# ============================================================
# TODO : Implémenter le système complet
# ============================================================

# 1. AuthService
#    - register(email, username, password) -> User
#    - login(email, password) -> Token
#    - get_current_user(token) -> User
#    - require_role(token, role) -> User
#    - change_password(token, old_pw, new_pw) -> bool
#    - Hashing avec passlib/bcrypt

# 2. Rate Limiter (middleware)
#    - Max 30 requêtes par minute par utilisateur
#    - Headers : X-RateLimit-Remaining, X-RateLimit-Reset

# 3. Event Bus
#    - Events : user_registered, user_logged_in, score_submitted
#    - Handlers : log console, update stats

# 4. Endpoints
#    POST /auth/register
#    POST /auth/login
#    GET /me
#    PATCH /me/password
#    GET /users (admin only)
#    POST /scores (authenticated)
#    GET /scores/leaderboard (public)
#    GET /admin/events (admin, historique events)


app = FastAPI(title="Secure Game API")


# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":
    client = TestClient(app)
    print("🧪 Test Secure Game API\n")
    
    # Décommenter au fur et à mesure
    
    # # Register
    # r = client.post("/auth/register", json={"email": "alice@g.com", "username": "Alice", "password": "pass123"})
    # assert r.status_code == 201
    # print(f"  ✅ Register: {r.json()['username']}")
    
    # # Login
    # r = client.post("/auth/login", data={"username": "alice@g.com", "password": "pass123"})
    # assert r.status_code == 200
    # token = r.json()["access_token"]
    # headers = {"Authorization": f"Bearer {token}"}
    # print(f"  ✅ Login: token obtained")
    
    # # Me
    # r = client.get("/me", headers=headers)
    # assert r.status_code == 200
    # print(f"  ✅ Me: {r.json()['username']}")
    
    # # Without auth
    # r = client.get("/me")
    # assert r.status_code == 401
    # print(f"  ✅ No auth: 401")
    
    print("\n✅ Tests terminés !")
