"""Module 08 — Solution exercice à trou #1"""

from sqlalchemy import create_engine, String, Integer, Float, ForeignKey, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

class Base(DeclarativeBase): pass

class Game(Base):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    genre: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column(Float)
    year: Mapped[int] = mapped_column(Integer)
    scores: Mapped[list["Score"]] = relationship(back_populates="game")
    def __repr__(self) -> str: return f"Game(id={self.id}, title={self.title!r})"

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

with Session(engine) as session:
    session.add_all([
        Game(title="Zelda TOTK", genre="rpg", price=59.99, year=2023),
        Game(title="Doom Eternal", genre="fps", price=29.99, year=2020),
        Game(title="Celeste", genre="platformer", price=9.99, year=2018),
        Game(title="Hades", genre="rpg", price=24.99, year=2020),
        Game(title="Portal 2", genre="puzzle", price=9.99, year=2011),
    ])
    session.add_all([Player(name="Alice", level=42), Player(name="Bob", level=15), Player(name="Charlie", level=30)])
    session.commit()
    session.add_all([
        Score(value=15000, player_id=1, game_id=1), Score(value=12000, player_id=1, game_id=4),
        Score(value=9000, player_id=2, game_id=2), Score(value=18000, player_id=3, game_id=1),
        Score(value=7500, player_id=2, game_id=5),
    ])
    session.commit()

print("✅ Data insérée !")

with Session(engine) as session:
    stmt = select(Game)
    all_games = session.scalars(stmt).all()
    print(f"\n📋 Tous les jeux ({len(all_games)}):")
    for g in all_games: print(f"  {g}")

    stmt = select(Game).where(Game.genre == "rpg")
    rpg_games = session.scalars(stmt).all()
    print(f"\n🎮 RPGs: {[g.title for g in rpg_games]}")

    stmt = select(Game).where(Game.price < 20)
    cheap_games = session.scalars(stmt).all()
    print(f"💰 Jeux < 20€: {[g.title for g in cheap_games]}")

    stmt = select(Game).order_by(Game.price.desc())
    sorted_games = session.scalars(stmt).all()
    print(f"📊 Par prix desc: {[(g.title, g.price) for g in sorted_games]}")

    stmt = select(Game).where(Game.title == "Zelda TOTK")
    zelda = session.scalars(stmt).first()
    print(f"\n🗡️ Zelda: {zelda}")

    game = session.get(Game, 1)
    print(f"🎯 Game #1: {game}")

    alice = session.get(Player, 1)
    print(f"\n👤 {alice.name} a {len(alice.scores)} scores :")
    for score in alice.scores:
        print(f"  {score.game.title}: {score.value}")

print("\n✅ Exercice terminé avec succès !")
