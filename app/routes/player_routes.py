from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.database import get_db
from app.utils.auth import oauth2_scheme
from app.models.players import Player  # noqa: F401
from app.schemas.player import PlayerCreate, PlayerUpdate, PlayerRead

# ---------- Router ----------
player_router = APIRouter()

@player_router.get("/players", response_model=dict)
def list_players(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    search: Optional[str] = Query(None),
    game_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    query = db.query(Player)
    if search:
        query = query.filter(Player.display_name.ilike(f"%{search}%"))
    if game_id is not None:
        query = query.filter(Player.game_id == game_id)
    total = query.with_entities(func.count()).scalar()
    items = query.offset(offset).limit(limit).all()
    return {"items": [PlayerRead.from_orm(p) for p in items], "total": total}

@player_router.get("/players/{player_id}", response_model=PlayerRead)
def get_player(
    player_id: int = Path(...),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Not found")
    return PlayerRead.from_orm(player)

@player_router.post("/players", response_model=PlayerRead, status_code=status.HTTP_201_CREATED)
def create_player(
    player_in: PlayerCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    player = Player(
        display_name=player_in.display_name,
        game_id=player_in.game_id,
        position=player_in.position or 0,
        turn_order=player_in.turn_order,
        is_ai=player_in.is_ai,
    )
    db.add(player)
    db.commit()
    db.refresh(player)
    return PlayerRead.from_orm(player)

@player_router.put("/players/{player_id}", response_model=PlayerRead)
def update_player(
    player_in: PlayerUpdate,
    player_id: int = Path(...),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Not found")
    update_data = player_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(player, field, value)
    db.commit()
    db.refresh(player)
    return PlayerRead.from_orm(player)

@player_router.delete("/players/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player(
    player_id: int = Path(...),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(player)
    db.commit()
    return None
