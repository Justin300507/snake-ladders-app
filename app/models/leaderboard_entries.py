from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class LeaderboardEntries(Base):
    __tablename__ = "leaderboard_entries"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    wins = Column(Integer, nullable=False)
    losses = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)

    user = relationship("User", back_populates="leaderboard_entries")

# Alias to match expected import name
Leaderboard_entries = LeaderboardEntries