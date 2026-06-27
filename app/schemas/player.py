from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class PlayerCreate(BaseModel):
    display_name: str = Field(min_length=1)
    game_id: int
    is_ai: bool = False
    position: Optional[int] = None
    turn_order: Optional[int] = None

class PlayerUpdate(BaseModel):
    display_name: Optional[str] = Field(default=None, min_length=1)
    is_ai: Optional[bool] = None
    position: Optional[int] = None
    turn_order: Optional[int] = None

class PlayerResponse(BaseModel):
    id: int
    display_name: str
    game_id: int
    is_ai: bool
    position: Optional[int] = None
    turn_order: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

# Alias used by routes expecting a "PlayerRead" schema
class PlayerRead(BaseModel):
    id: int
    display_name: str
    game_id: int
    is_ai: bool
    position: Optional[int] = None
    turn_order: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
