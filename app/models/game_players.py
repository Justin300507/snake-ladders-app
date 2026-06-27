from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class GamePlayer(Base):
    __tablename__ = "game_players"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, nullable=False)
    game_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_ai = Column(Boolean, nullable=False)
    position = Column(Integer, nullable=False)
    turn_order = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    game = relationship("GameSession", foreign_keys=[game_id])
    user = relationship("User", foreign_keys=[user_id])