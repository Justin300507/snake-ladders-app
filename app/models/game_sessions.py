from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class GameSession(Base):
    __tablename__ = "game_sessions"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    status = Column(String(20), nullable=False)
    board_theme = Column(String(50), nullable=True)
    max_players = Column(Integer, nullable=False)
    lobby_code = Column(String(6), nullable=False, unique=True)
    winner_player_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    winner_player = relationship(
        "User",
        foreign_keys=[winner_player_id]
    )