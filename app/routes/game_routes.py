from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List

from app.database import get_db
from app.models.game_sessions import GameSession
from app.utils.auth import get_current_user
from app.schemas.game import GameCreate, GameUpdate, GameRead

game_router = APIRouter()


def _generate_unique_lobby_code(db: Session) -> str:
    import random, string
    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        exists = db.query(GameSession).filter(GameSession.lobby_code == code).first()
        if not exists:
            return code


@game_router.get("/games", response_model=dict)
def list_games(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    lobby_code: Optional[str] = Query(None),
    game_status: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
):
    query = db.query(GameSession)
    if lobby_code:
        query = query.filter(GameSession.lobby_code == lobby_code)
    if game_status:
        query = query.filter(GameSession.status == game_status)

    total = query.with_entities(func.count()).scalar()
    games: List[GameSession] = query.offset(offset).limit(limit).all()
    items = [GameRead.model_validate(g).model_dump() for g in games]
    return {"items": items, "total": total}


@game_router.get("/games/{game_id}", response_model=GameRead)
def get_game(
    game_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    game = db.query(GameSession).filter(GameSession.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Not found")
    return GameRead.model_validate(game)


@game_router.post("/games", response_model=GameRead, status_code=status.HTTP_201_CREATED)
def create_game(
    game_in: GameCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    lobby_code = _generate_unique_lobby_code(db)
    new_game = GameSession(
        title=game_in.title,
        description=game_in.description,
        board_theme=game_in.board_theme,
        max_players=game_in.max_players,
        lobby_code=lobby_code,
        user_id=current_user.id,
        status="waiting",
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return GameRead.model_validate(new_game)


@game_router.put("/games/{game_id}", response_model=GameRead)
def update_game(
    game_in: GameUpdate,
    game_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    game = db.query(GameSession).filter(GameSession.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Not found")
    for field, value in game_in.model_dump(exclude_unset=True).items():
        setattr(game, field, value)
    db.commit()
    db.refresh(game)
    return GameRead.model_validate(game)


@game_router.delete("/games/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game(
    game_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    game = db.query(GameSession).filter(GameSession.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Not found")
    if game.status and game.status.lower() == "started":
        raise HTTPException(status_code=400, detail="Cannot delete a game that has already started")
    db.delete(game)
    db.commit()
    return None