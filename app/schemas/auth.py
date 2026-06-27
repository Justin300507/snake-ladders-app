from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class AuthCreate(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)
    display_name: Optional[str] = None
    role: Optional[str] = None

class AuthUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    display_name: Optional[str] = None
    role: Optional[str] = None

class AuthResponse(BaseModel):
    id: int
    email: str
    display_name: Optional[str] = None
    role: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)

class RegisterRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)
    display_name: Optional[str] = None
    role: Optional[str] = None

class Token(BaseModel):
    access_token: str = Field(min_length=1)
    token_type: str = Field(default="bearer", min_length=1)
    user_id: Optional[int] = None
    email: Optional[str] = None
    display_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
