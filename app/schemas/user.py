from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserCreate(BaseModel):
    email: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    role: str = Field(default="player", min_length=1)


class UserUpdate(BaseModel):
    email: Optional[str] = Field(default=None, min_length=1)
    display_name: Optional[str] = Field(default=None, min_length=1)
    role: Optional[str] = Field(default=None, min_length=1)


class UserResponse(BaseModel):
    id: int
    email: str
    display_name: Optional[str] = None
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseModel):
    id: int
    email: str
    display_name: Optional[str] = None
    role: str

    model_config = ConfigDict(from_attributes=True)
