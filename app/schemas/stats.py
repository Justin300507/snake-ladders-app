from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class StatsCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)


class StatsUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)


class StatsResponse(BaseModel):
    id: int
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)
