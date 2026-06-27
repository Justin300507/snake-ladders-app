from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class LeaderboardCreate(BaseModel):
    display_name: str = Field(min_length=1)
    rating: int = Field(default=0, ge=0)
    wins: int = Field(default=0, ge=0)
    losses: int = Field(default=0, ge=0)


class LeaderboardUpdate(BaseModel):
    display_name: Optional[str] = Field(default=None, min_length=1)
    rating: Optional[int] = Field(default=None, ge=0)
    wins: Optional[int] = Field(default=None, ge=0)
    losses: Optional[int] = Field(default=None, ge=0)


class LeaderboardResponse(BaseModel):
    id: int
    user_id: int
    display_name: str
    rating: int
    wins: int
    losses: int

    model_config = ConfigDict(from_attributes=True)
