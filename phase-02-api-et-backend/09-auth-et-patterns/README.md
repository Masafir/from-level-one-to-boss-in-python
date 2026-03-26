# Module 09 — Authentification & Patterns Avancés 🔐

> **Objectif** : Implémenter un système d'auth complet (JWT, bcrypt, RBAC) et maîtriser les patterns async en Python. Indispensable pour le fullstack.

## 1. Hashing de mots de passe

```python
# En Node : bcrypt.hash() / bcrypt.compare()
# En Python : passlib ou bcrypt directement

# pip install passlib[bcrypt]
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash un mot de passe
hashed = pwd_context.hash("my_password")
print(hashed)  # $2b$12$...

# Vérifier un mot de passe
is_valid = pwd_context.verify("my_password", hashed)  # True
is_valid = pwd_context.verify("wrong_password", hashed)  # False
```

## 2. JWT — JSON Web Tokens

```python
# pip install python-jose[cryptography]
from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key-change-in-prod"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Crée un JWT (comme jwt.sign() en Node)."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    """Vérifie et décode un JWT (comme jwt.verify() en Node)."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise ValueError("Token invalide")

# Créer un token
token = create_access_token({"sub": "alice@game.com", "role": "admin"})

# Décoder
payload = decode_token(token)
print(payload)  # {"sub": "alice@game.com", "role": "admin", "exp": ...}
```

## 3. Auth avec FastAPI

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

# OAuth2 scheme (gère le header Authorization: Bearer <token>)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class UserCreate(BaseModel):
    email: str
    password: str
    username: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Fake DB
users_db: dict[str, dict] = {}

@app.post("/auth/register", status_code=201)
async def register(user: UserCreate) -> UserResponse:
    if user.email in users_db:
        raise HTTPException(400, "Email déjà utilisé")
    
    hashed_password = pwd_context.hash(user.password)
    user_data = {
        "id": len(users_db) + 1,
        "email": user.email,
        "username": user.username,
        "hashed_password": hashed_password,
        "role": "player",
    }
    users_db[user.email] = user_data
    return UserResponse(**user_data)

@app.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = users_db.get(form_data.username)  # OAuth2 utilise 'username'
    if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(401, "Identifiants invalides")
    
    token = create_access_token({"sub": user["email"], "role": user["role"]})
    return Token(access_token=token)

# Dépendance : utilisateur courant
async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = decode_token(token)
        email = payload.get("sub")
        if not email or email not in users_db:
            raise HTTPException(401, "Token invalide")
        return users_db[email]
    except ValueError:
        raise HTTPException(401, "Token invalide")

# Dépendance : vérification de rôle
def require_role(role: str):
    async def check_role(user: dict = Depends(get_current_user)):
        if user["role"] != role:
            raise HTTPException(403, f"Rôle '{role}' requis")
        return user
    return check_role

# Routes protégées
@app.get("/me")
async def get_me(user: dict = Depends(get_current_user)):
    return UserResponse(**user)

@app.get("/admin/panel")
async def admin_panel(user: dict = Depends(require_role("admin"))):
    return {"message": f"Welcome admin {user['username']}"}
```

## 4. Async/Await en Python

```python
import asyncio

# En JS :  async function fetchData() { const data = await fetch(url); }
# En Python :

async def fetch_player_data(player_id: int) -> dict:
    """Simule un appel réseau async."""
    await asyncio.sleep(0.1)  # Simule de la latence
    return {"id": player_id, "name": f"Player_{player_id}"}

# Exécuter plusieurs tâches en parallèle (comme Promise.all())
async def fetch_all_players(ids: list[int]) -> list[dict]:
    tasks = [fetch_player_data(pid) for pid in ids]
    results = await asyncio.gather(*tasks)
    return list(results)

# asyncio.run() = le point d'entrée (Node a l'event loop implicite)
# asyncio.run(fetch_all_players([1, 2, 3]))
```

### Parallèle JS ↔ Python async

| JS | Python |
|-----|--------|
| `async function` | `async def` |
| `await promise` | `await coroutine` |
| `Promise.all([...])` | `asyncio.gather(...)` |
| `Promise.race([...])` | `asyncio.wait(tasks, return_when=FIRST_COMPLETED)` |
| `setTimeout(fn, ms)` | `await asyncio.sleep(s)` |
| `setInterval` | `asyncio.create_task` + boucle |
| Event Loop implicite | `asyncio.run()` ou framework (uvicorn) |

## 5. Background Tasks (comme les workers)

```python
from fastapi import BackgroundTasks

def send_welcome_email(email: str):
    """Task en background (ne bloque pas la réponse)."""
    import time
    time.sleep(2)  # Simule l'envoi
    print(f"📧 Email envoyé à {email}")

@app.post("/auth/register-v2")
async def register_v2(
    user: UserCreate,
    background_tasks: BackgroundTasks,
):
    # ... créer l'utilisateur ...
    background_tasks.add_task(send_welcome_email, user.email)
    return {"message": "Inscrit ! Email en cours d'envoi..."}
```

## 6. Patterns avancés

### Repository Pattern

```python
from abc import ABC, abstractmethod

class PlayerRepository(ABC):
    @abstractmethod
    async def get(self, player_id: int) -> dict | None: ...
    @abstractmethod
    async def create(self, data: dict) -> dict: ...
    @abstractmethod
    async def update(self, player_id: int, data: dict) -> dict: ...

class SQLPlayerRepository(PlayerRepository):
    def __init__(self, session):
        self.session = session
    
    async def get(self, player_id: int) -> dict | None:
        # Implémentation avec SQLAlchemy
        ...

class InMemoryPlayerRepository(PlayerRepository):
    """Pour les tests !"""
    def __init__(self):
        self.data = {}
    
    async def get(self, player_id: int) -> dict | None:
        return self.data.get(player_id)
```

### Event-driven Pattern

```python
from typing import Callable
from collections import defaultdict

class EventBus:
    def __init__(self):
        self._handlers: dict[str, list[Callable]] = defaultdict(list)
    
    def on(self, event: str, handler: Callable):
        self._handlers[event].append(handler)
    
    async def emit(self, event: str, data: dict):
        for handler in self._handlers[event]:
            if asyncio.iscoroutinefunction(handler):
                await handler(data)
            else:
                handler(data)

bus = EventBus()
bus.on("player_registered", lambda d: print(f"New player: {d['name']}"))
bus.on("score_submitted", lambda d: print(f"New score: {d['value']}"))
```

---

## 🎯 Résumé

| Concept | Ce qu'il faut retenir |
|---------|----------------------|
| **bcrypt** | `passlib.context` pour hasher les mots de passe |
| **JWT** | `python-jose` pour créer/vérifier les tokens |
| **OAuth2** | `OAuth2PasswordBearer` + `Depends()` dans FastAPI |
| **RBAC** | `require_role()` comme dépendance |
| **async/await** | Comme en JS, mais avec `asyncio.gather` au lieu de `Promise.all` |
| **BackgroundTasks** | Tâches en arrière-plan sans bloquer la réponse |

---

➡️ **Passe aux exercices dans `exercices/` !**
