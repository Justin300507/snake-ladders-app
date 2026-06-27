from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class GameHistory(Base):
    __tablename__ = "game_histories"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=False)
    winner_player_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ended_at = Column(DateTime, nullable=False)
    duration_seconds = Column(Integer, nullable=False)

    game = relationship("GameSession" )
    winner = relationship("User" )
