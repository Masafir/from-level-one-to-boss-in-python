"""
Module 08 — Exercice à trou #1
🎯 Thème : Modèles SQLAlchemy et CRUD basique

Complète les ___ pour que le code fonctionne.
Exécute avec : pip install sqlalchemy
              python 01_a_trou.py
"""

from sqlalchemy import create_engine, String, Integer, Float, ForeignKey, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

# ============================================================
# PARTIE 1 : Définir le modèle
# ============================================================

class Base(___):  # De quelle classe hériter pour la base SQLAlchemy ?
    pass


class Game(Base):
    ___  = "games"  # Quel attribut spécial pour le nom de la table ?
    
    id: Mapped[int] = mapped_column(___=True)  # Clé primaire ?
    title: Mapped[str] = mapped_column(String(200))
    genre: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column(Float)
    year: Mapped[int] = mapped_column(Integer)
    
    # Relation one-to-many vers Score
    scores: Mapped[list["Score"]] = ___(back_populates="game")
    
    def __repr__(self) -> str:
        return f"Game(id={self.id}, title={self.title!r})"


class Player(Base):
    __tablename__ = "players"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[___] = mapped_column(String(100), unique=True)  # Quel type Python ?
    level: Mapped[int] = mapped_column(default=1)
    
    scores: Mapped[list["Score"]] = relationship(back_populates="player")


class Score(Base):
    __tablename__ = "scores"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int] = mapped_column()
    
    # Clés étrangères
    player_id: Mapped[int] = mapped_column(___(  "players.id"))  # Quel type pour FK ?
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    
    # Relations
    player: Mapped["Player"] = relationship(___="scores")  # Quel paramètre ?
    game: Mapped["Game"] = relationship(back_populates="scores")


# ============================================================
# PARTIE 2 : Créer l'engine et les tables
# ============================================================

engine = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.___(engine)  # Quelle méthode pour créer les tables ?


# ============================================================
# PARTIE 3 : CRUD
# ============================================================

# CREATE
with Session(engine) as session:
    games = [
        Game(title="Zelda TOTK", genre="rpg", price=59.99, year=2023),
        Game(title="Doom Eternal", genre="fps", price=29.99, year=2020),
        Game(title="Celeste", genre="platformer", price=9.99, year=2018),
        Game(title="Hades", genre="rpg", price=24.99, year=2020),
        Game(title="Portal 2", genre="puzzle", price=9.99, year=2011),
    ]
    session.___( games)  # Quelle méthode pour ajouter plusieurs objets ?
    
    players = [
        Player(name="Alice", level=42),
        Player(name="Bob", level=15),
        Player(name="Charlie", level=30),
    ]
    session.add_all(players)
    session.___()  # Quelle méthode pour sauvegarder ?

    # Ajouter des scores
    scores = [
        Score(value=15000, player_id=1, game_id=1),
        Score(value=12000, player_id=1, game_id=4),
        Score(value=9000, player_id=2, game_id=2),
        Score(value=18000, player_id=3, game_id=1),
        Score(value=7500, player_id=2, game_id=5),
    ]
    session.add_all(scores)
    session.commit()

print("✅ Data insérée !")


# READ
with Session(engine) as session:
    # Tous les jeux
    stmt = ___(Game)  # Quelle fonction pour un SELECT ?
    all_games = session.scalars(stmt).all()
    print(f"\n📋 Tous les jeux ({len(all_games)}):")
    for g in all_games:
        print(f"  {g}")
    
    # Filtrer : jeux RPG
    stmt = select(Game).___(Game.genre == "rpg")  # Quelle méthode pour WHERE ?
    rpg_games = session.scalars(stmt).all()
    print(f"\n🎮 RPGs: {[g.title for g in rpg_games]}")
    
    # Filtrer : jeux à moins de 20€
    stmt = select(Game).where(Game.price ___ 20)  # Quel opérateur ?
    cheap_games = session.scalars(stmt).all()
    print(f"💰 Jeux < 20€: {[g.title for g in cheap_games]}")
    
    # Trier par prix décroissant
    stmt = select(Game).order_by(Game.price.___)  # Quel ordre ?
    sorted_games = session.scalars(stmt).all()
    print(f"📊 Par prix desc: {[(g.title, g.price) for g in sorted_games]}")
    
    # Premier résultat
    stmt = select(Game).where(Game.title == "Zelda TOTK")
    zelda = session.scalars(stmt).___()  # Quelle méthode pour un seul résultat ?
    print(f"\n🗡️ Zelda: {zelda}")
    
    # Par ID
    game = session.___(Game, 1)  # Quelle méthode pour chercher par PK ?
    print(f"🎯 Game #1: {game}")
    
    # Relations : scores d'un joueur
    alice = session.get(Player, 1)
    print(f"\n👤 {alice.name} a {len(alice.scores)} scores :")
    for score in alice.scores:
        print(f"  {score.game.title}: {score.value}")


# ============================================================
# CHECK FINAL
# ============================================================

if __name__ == "__main__":
    print("\n✅ Exercice terminé avec succès !")
