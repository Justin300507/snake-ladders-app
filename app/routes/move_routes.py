from fastapi import APIRouter, Depends, HTTPException, Query, Path, Response, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.moves import Move
from app.schemas.move import MoveCreate, MoveUpdate, MoveRead

move_router = APIRouter()


@move_router.get("/moves", response_model=dict)
def list_moves(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    player_id: Optional[int] = Query(None, ge=1),
    game_id: Optional[int] = Query(None, ge=1),
    db: Session = Depends(get_db),
):
    query = db.query(Move)
    if player_id is not None:
        query = query.filter(Move.player_id == player_id)
    if game_id is not None:
        query = query.filter(Move.game_id == game_id)
    total = query.count()
    items = query.offset(offset).limit(limit).all()
    return {"items": [MoveRead.model_validate(item) for item in items], "total": total}


@move_router.get("/moves/{move_id}", response_model=MoveRead)
def get_move(
    move_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    move = db.query(Move).filter(Move.id == move_id).first()
    if not move:
        raise HTTPException(status_code=404, detail="Not found")
    return MoveRead.model_validate(move)


@move_router.post("/moves", response_model=MoveRead, status_code=status.HTTP_201_CREATED)
def create_move(
    move_in: MoveCreate,
    db: Session = Depends(get_db),
):
    new_move = Move(
        dice_value=move_in.dice_value,
        from_position=move_in.from_position,
        to_position=move_in.to_position,
        player_id=move_in.player_id,
        game_id=move_in.game_id,
    )
    db.add(new_move)
    db.commit()
    db.refresh(new_move)
    return MoveRead.model_validate(new_move)


@move_router.put("/moves/{move_id}", response_model=MoveRead)
def update_move(
    move_in: MoveUpdate,
    move_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    move = db.query(Move).filter(Move.id == move_id).first()
    if not move:
        raise HTTPException(status_code=404, detail="Not found")
    for field, value in move_in.model_dump(exclude_unset=True).items():
        setattr(move, field, value)
    db.commit()
    db.refresh(move)
    return MoveRead.model_validate(move)


@move_router.delete("/moves/{move_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_move(
    move_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    move = db.query(Move).filter(Move.id == move_id).first()
    if not move:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(move)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
