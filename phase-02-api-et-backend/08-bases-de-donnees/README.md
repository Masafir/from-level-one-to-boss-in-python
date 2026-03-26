# Module 08 — Bases de Données avec SQLAlchemy 🗄️

> **Objectif** : Maîtriser l'accès aux bases de données en Python. SQLAlchemy est le Prisma/Sequelize du Python — mais en beaucoup plus puissant.

## 1. SQLAlchemy vs les ORMs JS

| | **SQLAlchemy** | **Prisma** | **Sequelize** |
|--|-------------|----------|------------|
| **Type** | ORM + Core SQL | ORM type-safe | ORM |
| **Philosophie** | 2 niveaux (Core + ORM) | Schema-first | Model-first |
| **Migrations** | Alembic (séparé) | `prisma migrate` | Sequelize CLI |
| **Raw SQL** | ✅ Natif | ⚠️ `$queryRaw` | ⚠️ `sequelize.query` |
| **Async** | ✅ Natif (v2) | ✅ | ❌ |
| **Perfs** | ⚡ Excellent | 🐢 Moyen | 🐢 Moyen |

```bash
pip install sqlalchemy aiosqlite  # async SQLite
# Pour PostgreSQL : pip install asyncpg
```

## 2. Définir des modèles

```python
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

# Base class (comme Prisma schema)
class Base(DeclarativeBase):
    pass

class Player(Base):
    __tablename__ = "players"

    # Mapped[type] = le type Python, mapped_column = les contraintes SQL
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    level: Mapped[int] = mapped_column(default=1)
    xp: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    
    # Relation one-to-many
    scores: Mapped[list["Score"]] = relationship(back_populates="player")
    
    def __repr__(self) -> str:
        return f"Player(id={self.id}, name={self.name!r}, level={self.level})"

class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    genre: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column(Float)
    
    scores: Mapped[list["Score"]] = relationship(back_populates="game")

class Score(Base):
    __tablename__ = "scores"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int] = mapped_column()
    achieved_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    
    # Foreign keys
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    
    # Relations
    player: Mapped["Player"] = relationship(back_populates="scores")
    game: Mapped["Game"] = relationship(back_populates="scores")
```

### Parallèle avec Prisma

```prisma
// Prisma schema
model Player {
  id        Int      @id @default(autoincrement())
  name      String   @unique
  email     String   @unique
  level     Int      @default(1)
  scores    Score[]
  createdAt DateTime @default(now())
}
```

## 3. Créer la DB et les sessions

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Engine = la connexion (comme le pool en Node)
engine = create_engine(
    "sqlite:///game.db",
    echo=True,  # Log les requêtes SQL (debug)
)

# Créer toutes les tables
Base.metadata.create_all(engine)

# Session = une "transaction" (comme prisma.$transaction)
with Session(engine) as session:
    # Créer
    alice = Player(name="Alice", email="alice@game.com")
    session.add(alice)
    session.commit()
    
    # Lire
    player = session.get(Player, 1)  # Par ID
    print(player)

# Async version (pour FastAPI)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

async_engine = create_async_engine("sqlite+aiosqlite:///game.db")
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

## 4. Queries (le CRUD)

```python
from sqlalchemy import select, update, delete

with Session(engine) as session:
    # === CREATE ===
    bob = Player(name="Bob", email="bob@game.com", level=5)
    session.add(bob)
    session.add_all([
        Player(name="Charlie", email="charlie@game.com"),
        Player(name="Diana", email="diana@game.com", level=10),
    ])
    session.commit()
    
    # === READ — SELECT ===
    # Tous les joueurs
    stmt = select(Player)
    players = session.scalars(stmt).all()
    
    # Avec filtre (WHERE)
    stmt = select(Player).where(Player.level > 3)
    high_levels = session.scalars(stmt).all()
    
    # Un seul résultat
    stmt = select(Player).where(Player.name == "Alice")
    alice = session.scalars(stmt).first()
    
    # Tri + limite
    stmt = (
        select(Player)
        .order_by(Player.level.desc())
        .limit(5)
    )
    top_players = session.scalars(stmt).all()
    
    # Requête complexe (JOIN, GROUP BY)
    from sqlalchemy import func
    stmt = (
        select(
            Player.name,
            func.count(Score.id).label("total_scores"),
            func.avg(Score.value).label("avg_score"),
        )
        .join(Score, Player.id == Score.player_id)
        .group_by(Player.id)
        .having(func.count(Score.id) > 0)
        .order_by(func.avg(Score.value).desc())
    )
    
    # === UPDATE ===
    stmt = (
        update(Player)
        .where(Player.name == "Alice")
        .values(level=42, xp=99999)
    )
    session.execute(stmt)
    session.commit()
    
    # Ou via l'objet
    alice = session.get(Player, 1)
    alice.level = 42
    session.commit()
    
    # === DELETE ===
    stmt = delete(Player).where(Player.name == "Bob")
    session.execute(stmt)
    session.commit()
```

## 5. Relations avancées

```python
# One-to-Many : Player a plusieurs Scores
alice = session.get(Player, 1)
print(alice.scores)  # Lazy-loaded !

# Many-to-Many : Players <-> Guilds
from sqlalchemy import Table, Column

# Table d'association
player_guild = Table(
    "player_guild", Base.metadata,
    Column("player_id", ForeignKey("players.id"), primary_key=True),
    Column("guild_id", ForeignKey("guilds.id"), primary_key=True),
)

class Guild(Base):
    __tablename__ = "guilds"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    members: Mapped[list["Player"]] = relationship(
        secondary=player_guild, back_populates="guilds"
    )

# Ajouter à Player :
# guilds: Mapped[list["Guild"]] = relationship(
#     secondary=player_guild, back_populates="members"
# )
```

## 6. Alembic — Les migrations

```bash
# Installation
pip install alembic

# Initialiser
alembic init alembic

# Configurer alembic/env.py avec ta Base et l'URL
# Puis :
alembic revision --autogenerate -m "initial"  # Comme prisma migrate dev
alembic upgrade head                          # Appliquer les migrations
alembic downgrade -1                          # Rollback
```

## 7. FastAPI + SQLAlchemy

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

# Dependency : session DB async
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/players/{player_id}")
async def get_player(player_id: int, db: AsyncSession = Depends(get_db)):
    player = await db.get(Player, player_id)
    if not player:
        raise HTTPException(404, "Player not found")
    return {"id": player.id, "name": player.name, "level": player.level}

@app.post("/players", status_code=201)
async def create_player(name: str, email: str, db: AsyncSession = Depends(get_db)):
    player = Player(name=name, email=email)
    db.add(player)
    await db.commit()
    await db.refresh(player)
    return {"id": player.id, "name": player.name}
```

---

## 🎯 Résumé

| Concept | Ce qu'il faut retenir |
|---------|----------------------|
| **Engine** | La connexion à la DB (`create_engine`) |
| **Session** | La "transaction" (comme `prisma.$transaction`) |
| **Mapped + mapped_column** | Définir un modèle (colonnes, types, contraintes) |
| **select()** | Requête SELECT (le nouvel API v2, pas `query()`) |
| **relationship()** | Définir les relations (one-to-many, many-to-many) |
| **Alembic** | Migrations (comme `prisma migrate`) |

---

➡️ **Passe aux exercices dans `exercices/` !**
