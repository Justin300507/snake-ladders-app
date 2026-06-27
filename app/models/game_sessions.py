from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class GameSession(Base):
    __tablename__ = "game_sessions"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=True)
    description = Column(String(500), nullable=True)
    status = Column(String(20), nullable=False, default="waiting")
    board_theme = Column(String(50), nullable=True)
    max_players = Column(Integer, nullable=False, default=4)
    lobby_code = Column(String(6), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    winner_player_id = Column(Integer, ForeignKey("game_players.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("Users", back_populates="game_sessions", foreign_keys=[user_id])
    game_players = relationship("GamePlayer", back_populates="game", foreign_keys="GamePlayer.game_id", cascade="all, delete-orphan")
