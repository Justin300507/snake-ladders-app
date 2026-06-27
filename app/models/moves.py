from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Move(Base):
    __tablename__ = "moves"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("game_players.id"), nullable=False)
    dice_value = Column(Integer, nullable=False)
    from_position = Column(Integer, nullable=False, default=0)
    to_position = Column(Integer, nullable=False, default=0)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)

    game = relationship("GameSession")
    player = relationship("GamePlayer")
