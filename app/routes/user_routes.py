from fastapi import APIRouter, Depends, HTTPException, Query, Path, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.users import User
from app.schemas.user import UserCreate, UserUpdate
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.utils.auth import get_password_hash


class UserRead(BaseModel):
    id: int
    email: str
    username: str
    display_name: str
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


user_router = APIRouter()


@user_router.get("/users", response_model=dict)
def list_users(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    search: Optional[str] = Query(None, description="Search by display_name"),
    role: Optional[str] = Query(None, description="Filter by role"),
    db: Session = Depends(get_db),
):
    query = db.query(User)
    if search:
        query = query.filter(User.display_name.ilike(f"%{search}%"))
    if role:
        query = query.filter(User.role == role)
    total = query.with_entities(func.count()).scalar()
    users = query.offset(offset).limit(limit).all()
    return {"items": [UserRead.from_orm(u) for u in users], "total": total}


@user_router.get("/users/{user_id}", response_model=UserRead)
def get_user(
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    return UserRead.from_orm(user)


@user_router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    hashed = get_password_hash(user_in.password)
    user = User(
        email=user_in.email,
        username=user_in.username,
        password_hash=hashed,
        display_name=user_in.display_name,
        role=user_in.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead.from_orm(user)


@user_router.put("/users/{user_id}", response_model=UserRead)
def update_user(
    user_in: UserUpdate,
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    if user_in.email is not None:
        user.email = user_in.email
    if user_in.username is not None:
        user.username = user_in.username
    if user_in.password is not None:
        user.password_hash = get_password_hash(user_in.password)
    if user_in.display_name is not None:
        user.display_name = user_in.display_name
    if user_in.role is not None:
        user.role = user_in.role
    db.commit()
    db.refresh(user)
    return UserRead.from_orm(user)


@user_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
