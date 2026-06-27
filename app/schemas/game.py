from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class GameCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    board_theme: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class GameUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    board_theme: Optional[str] = None
    status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class GameResponse(BaseModel):
    id: int
    title: str
    description: str
    lobby_code: str
    status: str
    board_theme: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
