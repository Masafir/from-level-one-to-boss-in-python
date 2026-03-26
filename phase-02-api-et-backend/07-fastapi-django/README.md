# Module 07 — FastAPI & Django : Les deux piliers du backend Python 🚀

> **Objectif** : Maîtriser FastAPI pour les APIs modernes, et comprendre Django pour savoir quand et pourquoi l'utiliser. En tant que dev Node/Express, tu vas te retrouver vite !

## 🥊 FastAPI vs Django — Le combat

| | **FastAPI** | **Django** |
|--|-----------|---------|
| **Philosophie** | Micro-framework API-first | Batteries-included, full-stack |
| **Équivalent JS** | Express.js / Hono | Next.js (API Routes + ORM + Admin) |
| **Vitesse** | ⚡ Ultra-rapide (async natif, Starlette) | 🐢 Plus lent mais suffisant |
| **Auto-doc API** | ✅ Swagger + ReDoc automatiques | ❌ (DRF ajoute ça) |
| **ORM** | ❌ Pas inclus (SQLAlchemy recommandé) | ✅ Django ORM inté gré (excellent) |
| **Admin** | ❌ Pas inclus | ✅ Interface admin automatique ! |
| **Auth** | ❌ À faire soi-même | ✅ Users, groups, permissions intégrés |
| **Validation** | ✅ Pydantic natif | ✅ Forms + Serializers (DRF) |
| **Async** | ✅ Natif (async/await) | ⚠️ Supporté mais pas natif historiquement |
| **Courbe d'apprentissage** | 📈 Faible (simple, explicite) | 📈 Plus élevée (beaucoup de conventions) |
| **Quand l'utiliser ?** | APIs REST/micro-services, MLOps | Apps web complètes, CMS, admin panels |

### TL;DR

- **FastAPI** = Quand tu veux **juste une API** rapide et moderne (ton futur boulot fullstack Python+React)
- **Django** = Quand tu veux **tout** (admin, auth, ORM, templates, forms) en un seul framework

> 💡 **Dans le monde pro**, beaucoup de boîtes utilisent les deux : **Django** pour le backoffice/admin et **FastAPI** pour les APIs performantes.

---

# PARTIE 1 — FastAPI 🏎️

## 1. Hello FastAPI

```bash
# Installation
pip install "fastapi[standard]"
# Inclut : fastapi, uvicorn, pydantic, etc.
```

```python
# main.py
from fastapi import FastAPI

app = FastAPI(
    title="Game API",
    description="API pour gérer des jeux vidéo",
    version="1.0.0",
)

@app.get("/")
async def root():
    """Page d'accueil."""
    return {"message": "Welcome to Game API!"}

@app.get("/health")
async def health():
    return {"status": "ok"}
```

```bash
# Lancer le serveur (comme nodemon)
uvicorn main:app --reload --port 8000

# Documentation auto :
# http://localhost:8000/docs      ← Swagger UI
# http://localhost:8000/redoc     ← ReDoc
```

> 🤯 Tu as une **doc API interactive automatique** juste en écrivant des routes. En Express il faut swagger-jsdoc + swagger-ui-express...

### Parallèle avec Express.js

```javascript
// Express.js
const app = express();
app.get('/', (req, res) => {
    res.json({ message: 'Hello!' });
});
app.listen(8000);
```

```python
# FastAPI — quasi identique !
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello!"}
```

## 2. Routes et Path Parameters

```python
# Path parameters (comme Express :id)
@app.get("/games/{game_id}")
async def get_game(game_id: int):  # Le type est validé automatiquement !
    return {"game_id": game_id}
# GET /games/42 → {"game_id": 42}
# GET /games/abc → 422 Validation Error (automatique !)

# Query parameters (comme ?limit=10&offset=0)
@app.get("/games")
async def list_games(
    limit: int = 10,          # Valeur par défaut
    offset: int = 0,
    genre: str | None = None, # Optionnel
):
    return {"limit": limit, "offset": offset, "genre": genre}
# GET /games?limit=5&genre=rpg → {"limit": 5, "offset": 0, "genre": "rpg"}

# Enum pour contraindre les valeurs
from enum import Enum

class Genre(str, Enum):
    RPG = "rpg"
    FPS = "fps"
    PUZZLE = "puzzle"

@app.get("/games/genre/{genre}")
async def games_by_genre(genre: Genre):
    return {"genre": genre.value}
# GET /games/genre/rpg → OK
# GET /games/genre/racing → 422 Error
```

## 3. Request Body avec Pydantic

```python
from pydantic import BaseModel, Field

# Pydantic model = le schema de validation (comme Joi ou Zod en JS)
class GameCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    genre: Genre
    price: float = Field(..., ge=0, le=100)
    tags: list[str] = []

class GameResponse(BaseModel):
    id: int
    title: str
    genre: Genre
    price: float
    tags: list[str]

# POST avec body
@app.post("/games", response_model=GameResponse, status_code=201)
async def create_game(game: GameCreate):
    # game est automatiquement validé !
    return GameResponse(id=1, **game.model_dump())

# La doc Swagger montre le schema automatiquement !
```

### Pydantic vs les validateurs JS

```python
# Pydantic c'est comme Zod mais en mieux intégré
# Zod : const schema = z.object({ title: z.string().min(1) })
# Pydantic :

from pydantic import BaseModel, Field, field_validator

class PlayerCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: str
    level: int = Field(default=1, ge=1, le=100)
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Email invalide")
        return v.lower()

    model_config = {"json_schema_extra": {
        "examples": [{"name": "Alice", "email": "alice@game.com", "level": 42}]
    }}
```

## 4. CRUD complet

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Simule une BDD en mémoire
db: dict[int, dict] = {}
next_id = 1

# CREATE
@app.post("/games", status_code=201)
async def create_game(game: GameCreate) -> GameResponse:
    global next_id
    game_dict = {"id": next_id, **game.model_dump()}
    db[next_id] = game_dict
    next_id += 1
    return GameResponse(**game_dict)

# READ (liste)
@app.get("/games")
async def list_games(limit: int = 10, offset: int = 0) -> list[GameResponse]:
    games = list(db.values())
    return [GameResponse(**g) for g in games[offset:offset + limit]]

# READ (détail)
@app.get("/games/{game_id}")
async def get_game(game_id: int) -> GameResponse:
    if game_id not in db:
        raise HTTPException(status_code=404, detail="Game not found")
    return GameResponse(**db[game_id])

# UPDATE
@app.put("/games/{game_id}")
async def update_game(game_id: int, game: GameCreate) -> GameResponse:
    if game_id not in db:
        raise HTTPException(status_code=404, detail="Game not found")
    db[game_id] = {"id": game_id, **game.model_dump()}
    return GameResponse(**db[game_id])

# DELETE
@app.delete("/games/{game_id}", status_code=204)
async def delete_game(game_id: int):
    if game_id not in db:
        raise HTTPException(status_code=404, detail="Game not found")
    del db[game_id]
```

## 5. Dependency Injection — Le superpower de FastAPI

```python
from fastapi import Depends

# Une dépendance = une fonction qui fournit un service
async def get_db():
    """Fournit une session DB (simulée)."""
    db = {"connection": "active"}
    try:
        yield db  # C'est un generator !
    finally:
        print("DB connection closed")

async def get_current_user(token: str = Header()):
    """Vérifie le token et retourne l'utilisateur."""
    if token != "secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user_id": 1, "name": "Alice"}

# Utiliser les dépendances
@app.get("/profile")
async def get_profile(
    user: dict = Depends(get_current_user),
    db: dict = Depends(get_db),
):
    return {"user": user, "db_status": db["connection"]}
```

## 6. Middleware et CORS

```python
from fastapi.middleware.cors import CORSMiddleware

# CORS — indispensable pour ton frontend React !
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Ton app React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware custom
import time

@app.middleware("http")
async def add_timing_header(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{elapsed:.4f}"
    return response
```

## 7. Router — Organiser les routes

```python
# routes/games.py
from fastapi import APIRouter

router = APIRouter(prefix="/games", tags=["Games"])

@router.get("/")
async def list_games():
    return []

@router.get("/{game_id}")
async def get_game(game_id: int):
    return {"id": game_id}

# main.py
from routes.games import router as games_router
app.include_router(games_router)
# Les routes sont maintenant /games/ et /games/{game_id}
```

---

# PARTIE 2 — Django : Pourquoi c'est bien 🏰

## 1. Philosophie Django

Django suit le principe **"Don't Repeat Yourself" (DRY)** et le pattern **MVT** (Model-View-Template) :
- **Model** = définition des données (ORM)
- **View** = logique de traitement (≈ controller en Express)
- **Template** = rendu HTML (mais pour les APIs on utilise DRF)

```bash
# Installation
pip install django djangorestframework

# Créer un projet
django-admin startproject gamesite
cd gamesite

# Créer une app (module)
python manage.py startapp games
```

### Structure Django

```
gamesite/                 # Projet
├── manage.py             # CLI (comme artisan en Laravel)
├── gamesite/             # Configuration
│   ├── settings.py       # Config centrale (comme .env mais en Python)
│   ├── urls.py           # Routes principales
│   └── wsgi.py           # Point d'entrée serveur
└── games/                # App "games"
    ├── models.py         # Modèles BDD
    ├── views.py          # Logique (controllers)
    ├── urls.py           # Routes de l'app
    ├── serializers.py    # Validation (avec DRF)
    ├── admin.py          # Interface admin
    └── tests.py
```

## 2. L'ORM Django — La killer feature

```python
# games/models.py
from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    release_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title

class Score(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="scores")
    player_name = models.CharField(max_length=100)
    value = models.IntegerField()
    achieved_at = models.DateTimeField(auto_now_add=True)
```

```bash
# Générer les migrations (comme Prisma migrate)
python manage.py makemigrations
python manage.py migrate
```

```python
# Requêtes ORM — ultra expressif !
# Créer
game = Game.objects.create(title="Zelda", genre="rpg", price=59.99)

# Lire
all_games = Game.objects.all()
rpg_games = Game.objects.filter(genre="rpg")
cheap = Game.objects.filter(price__lt=20)  # price < 20
zelda = Game.objects.get(title="Zelda")

# Requêtes avancées
from django.db.models import Avg, Count, Q

# Score moyen par jeu
Game.objects.annotate(avg_score=Avg("scores__value"))

# Recherche complexe
Game.objects.filter(
    Q(genre="rpg") | Q(genre="adventure"),
    price__lte=40,
).order_by("-price")
```

## 3. L'admin Django — Magique ✨

```python
# games/admin.py
from django.contrib import admin
from .models import Game, Score

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ["title", "genre", "price", "created_at"]
    list_filter = ["genre"]
    search_fields = ["title"]

# UN seul fichier et tu as un backoffice complet !
# Accessible sur http://localhost:8000/admin/
```

> 🤯 **L'admin Django est un game changer.** En 10 lignes de code tu as un backoffice complet avec CRUD, filtres, recherche, pagination, permissions. En Node il faudrait AdminJS ou retool...

## 4. Django REST Framework (DRF) — Pour les APIs

```python
# games/serializers.py
from rest_framework import serializers
from .models import Game

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["id", "title", "genre", "price", "created_at"]

# games/views.py
from rest_framework import viewsets
from .models import Game
from .serializers import GameSerializer

class GameViewSet(viewsets.ModelViewSet):
    """CRUD complet en 4 lignes !"""
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filterset_fields = ["genre"]
    ordering_fields = ["price", "created_at"]

# games/urls.py
from rest_framework.routers import DefaultRouter
from .views import GameViewSet

router = DefaultRouter()
router.register("games", GameViewSet)
# Crée automatiquement : GET/POST /games/ et GET/PUT/DELETE /games/{id}/
```

## 5. Quand utiliser quoi ?

| Besoin | Choix |
|--------|-------|
| API REST pour frontend React | **FastAPI** |
| Backoffice/admin interne | **Django** |
| Micro-service performant | **FastAPI** |
| App web complète (auth, admin, BDD) | **Django** |
| API + data science / ML | **FastAPI** |
| CMS, e-commerce, gestion | **Django** |
| Prototype rapide avec admin | **Django** |
| WebSockets / real-time | **FastAPI** |
| Tu travailles seul sur une API | **FastAPI** |
| Grande équipe, projet complexe | **Django** (conventions fortes) |

---

## 🎯 Résumé

| Concept | FastAPI | Django |
|---------|---------|--------|
| **Routes** | Decorators `@app.get()` | `urls.py` + views |
| **Validation** | Pydantic `BaseModel` | Serializers (DRF) |
| **ORM** | SQLAlchemy (séparé) | Django ORM (intégré) |
| **Admin** | ❌ | ✅ Automatique |
| **Auth** | DIY ou package | ✅ Intégré |
| **Middleware** | `@app.middleware` | `MIDDLEWARE` dans settings |
| **Tests** | pytest + httpx | Django TestCase |
| **DI** | `Depends()` | N/A (conventions) |

---

➡️ **Les exercices se concentrent sur FastAPI (ton outil principal pour le fullstack React+Python). Django sera pratiqué dans le mini-projet !**
