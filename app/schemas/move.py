from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class MoveCreate(BaseModel):
    player_id: int
    game_id: int
    dice_value: int = Field(ge=1, le=6)
    from_position: int = Field(ge=0)
    to_position: int = Field(ge=0)


class MoveUpdate(BaseModel):
    player_id: Optional[int] = None
    game_id: Optional[int] = None
    dice_value: Optional[int] = Field(default=None, ge=1, le=6)
    from_position: Optional[int] = Field(default=None, ge=0)
    to_position: Optional[int] = Field(default=None, ge=0)


class MoveRead(BaseModel):
    id: int
    player_id: int
    game_id: int
    dice_value: int
    from_position: int
    to_position: int
    timestamp: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)