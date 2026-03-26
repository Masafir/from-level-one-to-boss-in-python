"""
Module 08 — Exercice à trou #2
🎯 Thème : Requêtes avancées, agrégations et FastAPI+SQLAlchemy

Complète les ___ pour que le code fonctionne.
Exécute avec : python 02_a_trou.py
"""

from sqlalchemy import create_engine, String, Integer, Float, ForeignKey, func, select, update, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

# ============================================================
# SETUP (même modèles que l'exo 1)
# ============================================================

class Base(DeclarativeBase): pass

class Game(Base):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    genre: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column(Float)
    year: Mapped[int] = mapped_column(Integer)
    scores: Mapped[list["Score"]] = relationship(back_populates="game")

class Player(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    level: Mapped[int] = mapped_column(default=1)
    scores: Mapped[list["Score"]] = relationship(back_populates="player")

class Score(Base):
    __tablename__ = "scores"
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int] = mapped_column()
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    player: Mapped["Player"] = relationship(back_populates="scores")
    game: Mapped["Game"] = relationship(back_populates="scores")

engine = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.create_all(engine)

# Seed
with Session(engine) as s:
    s.add_all([
        Game(title="Zelda", genre="rpg", price=59.99, year=2023),
        Game(title="Doom", genre="fps", price=29.99, year=2020),
        Game(title="Celeste", genre="platformer", price=9.99, year=2018),
        Game(title="Hades", genre="rpg", price=24.99, year=2020),
        Game(title="Portal 2", genre="puzzle", price=9.99, year=2011),
        Game(title="Elden Ring", genre="rpg", price=49.99, year=2022),
    ])
    s.add_all([Player(name="Alice", level=42), Player(name="Bob", level=15), Player(name="Charlie", level=30)])
    s.commit()
    s.add_all([
        Score(value=15000, player_id=1, game_id=1), Score(value=12000, player_id=1, game_id=4),
        Score(value=9000, player_id=2, game_id=2), Score(value=18000, player_id=3, game_id=1),
        Score(value=7500, player_id=2, game_id=5), Score(value=20000, player_id=1, game_id=6),
        Score(value=11000, player_id=3, game_id=6), Score(value=16000, player_id=2, game_id=4),
    ])
    s.commit()


# ============================================================
# PARTIE 1 : Requêtes avancées
# ============================================================

with Session(engine) as session:
    # Compter le nombre de jeux par genre
    stmt = (
        select(
            Game.genre,
            ___(Game.id).label("count"),  # Quelle fonction d'agrégation ?
        )
        .group_by(Game.___)  # Grouper par quel champ ?
    )
    print("📊 Jeux par genre :")
    for row in session.execute(stmt):
        print(f"  {row.genre}: {row.count}")
    
    # Prix moyen par genre
    stmt = (
        select(
            Game.genre,
            func.___(Game.price).label("avg_price"),  # Quelle fonction pour la moyenne ?
        )
        .group_by(Game.genre)
        .order_by(func.avg(Game.price).desc())
    )
    print("\n💰 Prix moyen par genre :")
    for row in session.execute(stmt):
        print(f"  {row.genre}: {row.avg_price:.2f}€")
    
    # Top scores avec JOIN
    stmt = (
        select(
            Player.name,
            Game.title,
            Score.value,
        )
        .___(Score, Player.id == Score.player_id)  # Quelle méthode pour JOIN ?
        .join(Game, Game.id == Score.game_id)
        .order_by(Score.value.___)  # Quel ordre pour le top ?
        .limit(5)
    )
    print("\n🏆 Top 5 scores :")
    for row in session.execute(stmt):
        print(f"  {row.name} — {row.title}: {row.value}")
    
    # Joueurs avec plus de 2 scores
    stmt = (
        select(
            Player.name,
            func.count(Score.id).label("num_scores"),
            func.avg(Score.value).label("avg_score"),
        )
        .join(Score, Player.id == Score.player_id)
        .group_by(Player.id)
        .___(func.count(Score.id) > 2)  # Quelle clause pour filtrer après GROUP BY ?
    )
    print("\n⭐ Joueurs actifs (>2 scores) :")
    for row in session.execute(stmt):
        print(f"  {row.name}: {row.num_scores} scores (moy: {row.avg_score:.0f})")


# ============================================================
# PARTIE 2 : UPDATE et DELETE
# ============================================================

with Session(engine) as session:
    # UPDATE : augmenter le prix des RPGs de 10%
    stmt = (
        ___(Game)  # Quelle fonction pour UPDATE ?
        .where(Game.genre == "rpg")
        .values(price=Game.price * 1.1)
    )
    session.execute(stmt)
    session.commit()
    
    # Vérifier
    rpgs = session.scalars(select(Game).where(Game.genre == "rpg")).all()
    print("\n📈 RPGs après augmentation :")
    for g in rpgs:
        print(f"  {g.title}: {g.price:.2f}€")
    
    # DELETE : supprimer les scores inférieurs à 8000
    stmt = (
        ___(Score)  # Quelle fonction pour DELETE ?
        .where(Score.value < 8000)
    )
    result = session.execute(stmt)
    session.commit()
    print(f"\n🗑️ Scores supprimés : {result.rowcount}")


# ============================================================
# CHECK FINAL
# ============================================================

if __name__ == "__main__":
    print("\n✅ Exercice terminé avec succès !")
