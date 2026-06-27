from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class LeaderboardCreate(BaseModel):
    user_id: int
    wins: int = 0
    losses: int = 0
    rating: float = 1000.0


class LeaderboardUpdate(BaseModel):
    wins: Optional[int] = None
    losses: Optional[int] = None
    rating: Optional[float] = None


class LeaderboardRead(BaseModel):
    id: int
    user_id: int
    wins: int
    losses: int
    rating: float

    model_config = ConfigDict(from_attributes=True)
