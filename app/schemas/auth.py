from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class RegisterRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)
    display_name: Optional[str] = None
    role: Optional[str] = None

class LoginRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AuthCreate(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)
    display_name: Optional[str] = None
    role: Optional[str] = None

class AuthUpdate(BaseModel):
    email: Optional[str] = Field(default=None, min_length=1)
    password: Optional[str] = Field(default=None, min_length=1)
    display_name: Optional[str] = None
    role: Optional[str] = None

class AuthResponse(BaseModel):
    id: int
    email: str
    display_name: Optional[str] = None
    role: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
