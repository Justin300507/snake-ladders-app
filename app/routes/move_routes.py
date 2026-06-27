from fastapi import APIRouter, Depends, HTTPException, Query, Path, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from app.database import get_db
from app.utils.auth import get_current_user
from app.models.move import Move

from app.schemas.move import MoveCreate, MoveUpdate, MoveRead

move_router = APIRouter()


@move_router.get("/moves", response_model=dict)
def get_moves(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    player_id: Optional[int] = Query(None),
    game_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    query = db.query(Move)
    count_query = db.query(func.count(Move.id))
    if player_id is not None:
        query = query.filter(Move.player_id == player_id)
        count_query = count_query.filter(Move.player_id == player_id)
    if game_id is not None:
        query = query.filter(Move.game_id == game_id)
        count_query = count_query.filter(Move.game_id == game_id)
    total = count_query.scalar()
    items = query.offset(offset).limit(limit).all()
    return {"items": items, "total": total}


@move_router.get("/moves/{move_id}", response_model=MoveRead)
def get_move(
    move_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    move = db.query(Move).filter(Move.id == move_id).first()
    if not move:
        raise HTTPException(status_code=404, detail="Not found")
    return move


@move_router.post("/moves", response_model=MoveRead, status_code=status.HTTP_201_CREATED)
def create_move(
    move_in: MoveCreate,
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    move = Move(**move_in.model_dump())
    db.add(move)
    db.commit()
    db.refresh(move)
    return move


@move_router.put("/moves/{move_id}", response_model=MoveRead)
def update_move(
    move_in: MoveUpdate,
    move_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    move = db.query(Move).filter(Move.id == move_id).first()
    if not move:
        raise HTTPException(status_code=404, detail="Not found")
    update_data = move_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(move, field, value)
    db.commit()
    db.refresh(move)
    return move


@move_router.delete("/moves/{move_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_move(
    move_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    move = db.query(Move).filter(Move.id == move_id).first()
    if not move:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(move)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
