from fastapi import APIRouter, Depends, HTTPException, Query, Path, Response, status
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.game_players import GamePlayer
from app.utils.auth import get_current_user
from app.schemas.player import PlayerCreate, PlayerUpdate, PlayerRead

player_router = APIRouter()

@player_router.get("/players", response_model=dict)
def list_players(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    display_name: Optional[str] = Query(None),
    game_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = db.query(GamePlayer)
    if display_name:
        query = query.filter(GamePlayer.display_name.ilike(f"%{display_name}%"))
    if game_id:
        query = query.filter(GamePlayer.game_id == game_id)
    total = query.count()
    players: List[GamePlayer] = query.offset(offset).limit(limit).all()
    return {"items": [PlayerRead.model_validate(p) for p in players], "total": total}


@player_router.get("/players/{player_id}", response_model=PlayerRead)
def get_player(
    player_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    player = db.query(GamePlayer).filter(GamePlayer.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Not found")
    return PlayerRead.model_validate(player)


@player_router.post("/players", response_model=PlayerRead, status_code=status.HTTP_201_CREATED)
def create_player(
    player_in: PlayerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    player_data = player_in.model_dump()
    player_data["user_id"] = current_user.id
    player = GamePlayer(**player_data)
    db.add(player)
    db.commit()
    db.refresh(player)
    return PlayerRead.model_validate(player)


@player_router.put("/players/{player_id}", response_model=PlayerRead)
def update_player(
    player_in: PlayerUpdate,
    player_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    player = db.query(GamePlayer).filter(GamePlayer.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Not found")
    for field, value in player_in.model_dump(exclude_unset=True).items():
        setattr(player, field, value)
    db.commit()
    db.refresh(player)
    return PlayerRead.model_validate(player)


@player_router.delete("/players/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player(
    player_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    player = db.query(GamePlayer).filter(GamePlayer.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(player)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
