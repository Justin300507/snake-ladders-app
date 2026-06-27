from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

class MoveCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    player_id: int
    game_id: int
    dice_roll: int
    token_movement: int

class MoveUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)
    player_id: Optional[int] = None
    game_id: Optional[int] = None
    dice_roll: Optional[int] = None
    token_movement: Optional[int] = None

class MoveResponse(BaseModel):
    id: int
    title: str
    description: str
    player_id: int
    game_id: int
    dice_roll: int
    token_movement: int

    model_config = ConfigDict(from_attributes=True)

class MoveRead(MoveResponse):
    """Schema for reading a Move; identical to MoveResponse."""
    pass