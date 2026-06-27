from fastapi import APIRouter, Depends, HTTPException, Query, Path, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
import random, string

from app.database import get_db
from app.utils.auth import get_current_user, oauth2_scheme
from app.schemas.game import GameCreate, GameUpdate
from app.models.game_sessions import GameSession

# Helper to convert a GameSession model to a plain dict suitable for JSON response
def _game_to_dict(game: GameSession) -> dict:
    return {
        "id": game.id,
        "title": getattr(game, "title", None),
        "description": getattr(game, "description", None),
        "board_theme": getattr(game, "board_theme", None),
        "lobby_code": getattr(game, "lobby_code", None),
        "status": getattr(game, "status", None),
        "created_at": getattr(game, "created_at", None),
        "updated_at": getattr(game, "updated_at", None),
    }


game_router = APIRouter()

# ---------------------------------------------------------------------------
# GET /games - List game sessions (authenticated)
# ---------------------------------------------------------------------------
@game_router.get("/games", response_model=dict)
def list_games(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    lobby_code: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    query = db.query(GameSession)
    if lobby_code:
        query = query.filter(GameSession.lobby_code == lobby_code)
    if status:
        query = query.filter(GameSession.status == status)

    total = query.with_entities(func.count()).scalar()
    games: List[GameSession] = query.offset(offset).limit(limit).all()
    items = [_game_to_dict(g) for g in games]
    return {"items": items, "total": total}

# ---------------------------------------------------------------------------
# GET /games/{id} - Retrieve a specific game session (authenticated)
# ---------------------------------------------------------------------------
@game_router.get("/games/{game_id}", response_model=dict)
def get_game(
    game_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    game = db.query(GameSession).filter(GameSession.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Not found")
    return _game_to_dict(game)

# ---------------------------------------------------------------------------
# POST /games - Create a new game lobby (authenticated)
# ---------------------------------------------------------------------------
@game_router.post("/games", status_code=status.HTTP_201_CREATED, response_model=dict)
def create_game(
    game_in: GameCreate,
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    # Generate a unique 6‑character alphanumeric lobby code
    def _generate_code() -> str:
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    lobby_code = _generate_code()
    # Ensure uniqueness
    while db.query(GameSession).filter(GameSession.lobby_code == lobby_code).first():
        lobby_code = _generate_code()

    new_game = GameSession(
        title=game_in.title,
        description=game_in.description,
        board_theme=game_in.board_theme,
        lobby_code=lobby_code,
        status="pending",
        user_id=current_user.id,  # type: ignore[attr-defined]
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return _game_to_dict(new_game)

# ---------------------------------------------------------------------------
# PUT /games/{id} - Update mutable fields (authenticated)
# ---------------------------------------------------------------------------
@game_router.put("/games/{game_id}", response_model=dict)
def update_game(
    game_in: GameUpdate,
    game_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    game = db.query(GameSession).filter(GameSession.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Not found")
    # Only allow the owner to modify - simple ownership check
    if getattr(game, "user_id", None) != current_user.id:  # type: ignore[attr-defined]
        raise HTTPException(status_code=403, detail="Forbidden")
    if game_in.status is not None:
        game.status = game_in.status
    if game_in.board_theme is not None:
        game.board_theme = game_in.board_theme
    db.commit()
    db.refresh(game)
    return _game_to_dict(game)

# ---------------------------------------------------------------------------
# DELETE /games/{id} - Delete a game session before it starts (authenticated)
# ---------------------------------------------------------------------------
@game_router.delete("/games/{game_id}")
def delete_game(
    game_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: "User" = Depends(get_current_user),
):
    game = db.query(GameSession).filter(GameSession.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Not found")
    # Ownership check
    if getattr(game, "user_id", None) != current_user.id:  # type: ignore[attr-defined]
        raise HTTPException(status_code=403, detail="Forbidden")
    # Allow deletion only if the game has not started yet
    if getattr(game, "status", None) != "pending":
        raise HTTPException(status_code=400, detail="Cannot delete a game that has already started")
    db.delete(game)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
