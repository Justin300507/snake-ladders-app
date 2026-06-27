from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from app.database import get_db
from app.models.leaderboard_entries import LeaderboardEntry
from app.models.users import Users
from app.schemas.leaderboard import LeaderboardCreate, LeaderboardUpdate, LeaderboardRead

leaderboard_router = APIRouter()


@leaderboard_router.get("/leaderboard", response_model=dict)
def list_leaderboard(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    search: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None, ge=0),
    max_rating: Optional[float] = Query(None, ge=0),
    db: Session = Depends(get_db),
):
    query = db.query(LeaderboardEntry)
    if search:
        query = query.join(Users, LeaderboardEntry.user_id == Users.id).filter(
            Users.display_name.ilike(f"%{search}%")
        )
    if min_rating is not None:
        query = query.filter(LeaderboardEntry.rating >= min_rating)
    if max_rating is not None:
        query = query.filter(LeaderboardEntry.rating <= max_rating)

    total = query.with_entities(func.count(LeaderboardEntry.id)).scalar()
    entries = query.offset(offset).limit(limit).all()
    return {"items": [LeaderboardRead.model_validate(e).model_dump() for e in entries], "total": total}


@leaderboard_router.get("/leaderboard/{entry_id}", response_model=LeaderboardRead)
def get_leaderboard_entry(
    entry_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    entry = db.query(LeaderboardEntry).filter(LeaderboardEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    return LeaderboardRead.model_validate(entry)


@leaderboard_router.post("/leaderboard", response_model=LeaderboardRead, status_code=status.HTTP_201_CREATED)
def create_leaderboard_entry(
    payload: LeaderboardCreate,
    db: Session = Depends(get_db),
):
    user = db.query(Users).filter(Users.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    entry = LeaderboardEntry(
        user_id=payload.user_id,
        wins=payload.wins,
        losses=payload.losses,
        rating=payload.rating,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return LeaderboardRead.model_validate(entry)


@leaderboard_router.put("/leaderboard/{entry_id}", response_model=LeaderboardRead)
def update_leaderboard_entry(
    payload: LeaderboardUpdate,
    entry_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    entry = db.query(LeaderboardEntry).filter(LeaderboardEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(entry, field, value)
    db.commit()
    db.refresh(entry)
    return LeaderboardRead.model_validate(entry)


@leaderboard_router.delete("/leaderboard/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_leaderboard_entry(
    entry_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    entry = db.query(LeaderboardEntry).filter(LeaderboardEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(entry)
    db.commit()
    return None