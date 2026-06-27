from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from app.database import get_db
from app.models.users import Users
from app.schemas.user import UserCreate, UserUpdate, UserRead

user_router = APIRouter()


@user_router.get("/users", response_model=dict)
def list_users(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    search: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Users)
    if search:
        query = query.filter(Users.display_name.ilike(f"%{search}%"))
    if role:
        query = query.filter(Users.role == role)
    total = query.with_entities(func.count()).scalar()
    users = query.offset(offset).limit(limit).all()
    items = [UserRead.model_validate(u).model_dump() for u in users]
    return {"items": items, "total": total}


@user_router.get("/users/{user_id}", response_model=UserRead)
def get_user(
    user_id: int = Path(...),
    db: Session = Depends(get_db),
):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    return UserRead.model_validate(user)


@user_router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    user = Users(
        email=user_in.email,
        display_name=user_in.display_name,
        role=user_in.role,
        password_hash="",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead.model_validate(user)


@user_router.put("/users/{user_id}", response_model=UserRead)
def update_user(
    user_in: UserUpdate,
    user_id: int = Path(...),
    db: Session = Depends(get_db),
):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    for field, value in user_in.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return UserRead.model_validate(user)


@user_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int = Path(...),
    db: Session = Depends(get_db),
):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(user)
    db.commit()
    return