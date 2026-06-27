from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class GameCreate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    board_theme: Optional[str] = None
    max_players: int = Field(default=4, ge=2, le=8)

    model_config = ConfigDict(from_attributes=True)


class GameUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    board_theme: Optional[str] = None
    max_players: Optional[int] = Field(default=None, ge=2, le=8)

    model_config = ConfigDict(from_attributes=True)


class GameRead(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    lobby_code: str
    status: str
    board_theme: Optional[str] = None
    max_players: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
