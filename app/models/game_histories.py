from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class GameHistory(Base):
    __tablename__ = "game_histories"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, nullable=False)
    game_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=False)
    winner_player_id = Column(Integer, ForeignKey("game_players.id"), nullable=True)
    ended_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True)

    game = relationship("GameSession", lazy="joined")
    winner_player = relationship("GamePlayer", lazy="joined")
