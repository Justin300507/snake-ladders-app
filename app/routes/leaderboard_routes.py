from fastapi import APIRouter, Depends, HTTPException, Query, Path, Response, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.leaderboard_entries import LeaderboardEntries
from app.models.users import User

from pydantic import BaseModel, Field, ConfigDict

leaderboard_router = APIRouter()

class LeaderboardEntryCreate(BaseModel):
    user_id: int = Field(..., ge=1)
    wins: Optional[int] = Field(default=0, ge=0)
    losses: Optional[int] = Field(default=0, ge=0)
    rating: Optional[float] = Field(default=1000.0, ge=0)

    model_config = ConfigDict(from_attributes=True)

class LeaderboardEntryUpdate(BaseModel):
    wins: Optional[int] = Field(default=None, ge=0)
    losses: Optional[int] = Field(default=None, ge=0)
    rating: Optional[float] = Field(default=None, ge=0)

    model_config = ConfigDict(from_attributes=True)

class LeaderboardEntryResponse(BaseModel):
    id: int
    user_id: int
    wins: int
    losses: int
    rating: float

    model_config = ConfigDict(from_attributes=True)

@leaderboard_router.get("/leaderboard", response_model=dict)
def list_leaderboard(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    search: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None, ge=0),
    max_rating: Optional[float] = Query(None, ge=0),
    db: Session = Depends(get_db),
):
    query = db.query(LeaderboardEntries).join(User, LeaderboardEntries.user_id == User.id)
    if search:
        query = query.filter(User.display_name.ilike(f"%{search}%"))
    if min_rating is not None:
        query = query.filter(LeaderboardEntries.rating >= min_rating)
    if max_rating is not None:
        query = query.filter(LeaderboardEntries.rating <= max_rating)
    total = query.count()
    entries = query.offset(offset).limit(limit).all()
    items = [LeaderboardEntryResponse.from_orm(e).model_dump() for e in entries]
    return {"items": items, "total": total}

@leaderboard_router.get("/leaderboard/{entry_id}", response_model=LeaderboardEntryResponse)
def get_leaderboard_entry(
    entry_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    entry = db.query(LeaderboardEntries).filter(LeaderboardEntries.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    return LeaderboardEntryResponse.from_orm(entry)

@leaderboard_router.post("/leaderboard", response_model=LeaderboardEntryResponse, status_code=status.HTTP_201_CREATED)
def create_leaderboard_entry(
    entry_in: LeaderboardEntryCreate,
    db: Session = Depends(get_db),
):
    entry = LeaderboardEntries(**entry_in.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return LeaderboardEntryResponse.from_orm(entry)

@leaderboard_router.put("/leaderboard/{entry_id}", response_model=LeaderboardEntryResponse)
def update_leaderboard_entry(
    entry_in: LeaderboardEntryUpdate,
    entry_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    entry = db.query(LeaderboardEntries).filter(LeaderboardEntries.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    update_data = entry_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(entry, field, value)
    db.commit()
    db.refresh(entry)
    return LeaderboardEntryResponse.from_orm(entry)

@leaderboard_router.delete("/leaderboard/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_leaderboard_entry(
    entry_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    entry = db.query(LeaderboardEntries).filter(LeaderboardEntries.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(entry)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
