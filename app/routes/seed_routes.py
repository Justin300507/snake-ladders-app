from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from datetime import datetime

from app.database import get_db
# bcrypt helper from utils
from app.utils.auth import get_password_hash

seed_router = APIRouter()

@seed_router.post("/seed")
def seed_database(db: Session = Depends(get_db)):
    """Populate the database with demo data.
    The endpoint is idempotent – repeated calls will not create duplicate rows.
    """
    added = {
        "users": 0,
        "games": 0,
        "sessions": 0,
        "players": 0,
        "histories": 0,
        "leaderboard": 0,
    }

    # ---------- Users ----------
    user_seeds = [
        {
            "username": "alexchen",
            "email": "alex.chen@example.com",
            "display_name": "Alex Chen",
            "role": "player",
            "password_hash": get_password_hash("SecurePass1"),
        },
        {
            "username": "mariagarcia",
            "email": "maria.garcia@example.com",
            "display_name": "Maria Garcia",
            "role": "player",
            "password_hash": get_password_hash("SecurePass2"),
        },
        {
            "username": "jameskim",
            "email": "james.kim@example.com",
            "display_name": "James Kim",
            "role": "player",
            "password_hash": get_password_hash("SecurePass3"),
        },
        {
            "username": "lindawong",
            "email": "linda.wong@example.com",
            "display_name": "Linda Wong",
            "role": "admin",
            "password_hash": get_password_hash("AdminPass1"),
        },
        {
            "username": "robertlee",
            "email": "robert.lee@example.com",
            "display_name": "Robert Lee",
            "role": "player",
            "password_hash": get_password_hash("SecurePass4"),
        },
    ]
    for u in user_seeds:
        # The generated users table does not have a 'username' column; omit it.
        user_data = {
            "email": u["email"],
            "display_name": u["display_name"],
            "role": u["role"],
            "password_hash": u["password_hash"],
        }
        try:
            db.execute(
                text(
                    "INSERT INTO users (email, display_name, role, password_hash) "
                    "VALUES (:email, :display_name, :role, :password_hash)"
                ),
                user_data,
            )
            added["users"] += 1
        except IntegrityError:
            db.rollback()
    db.commit()

    # ---------- Games ----------
    game_seeds = [
        {"title": "Space Conquest", "description": "Explore the galaxy and claim planets.", "board_theme": "space"},
        {"title": "Mystic Quest", "description": "A journey through enchanted lands.", "board_theme": "fantasy"},
        {"title": "City Builders", "description": "Develop your metropolis.", "board_theme": "urban"},
        {"title": "Pirate Cove", "description": "Sail the seas and hunt treasure.", "board_theme": "pirate"},
        {"title": "Dungeon Crawl", "description": "Delve into dungeons and defeat monsters.", "board_theme": "dungeon"},
    ]
    for g in game_seeds:
        try:
            db.execute(
                text(
                    "INSERT INTO games (title, description, board_theme) "
                    "VALUES (:title, :description, :board_theme)"
                ),
                g,
            )
            added["games"] += 1
        except IntegrityError:
            db.rollback()
    db.commit()

    # Retrieve first user and first game IDs for FK relations
    first_user_id = db.execute(text("SELECT id FROM users ORDER BY id LIMIT 1")).scalar()
    first_game_id = db.execute(text("SELECT id FROM games ORDER BY id LIMIT 1")).scalar()

    # ---------- Game Sessions ----------
    if first_game_id is not None:
        session_seeds = [
            {"game_id": first_game_id, "status": "active", "started_at": datetime.utcnow(), "ended_at": None},
            {"game_id": first_game_id, "status": "completed", "started_at": datetime.utcnow(), "ended_at": datetime.utcnow()},
            {"game_id": first_game_id, "status": "active", "started_at": datetime.utcnow(), "ended_at": None},
            {"game_id": first_game_id, "status": "pending", "started_at": datetime.utcnow(), "ended_at": None},
            {"game_id": first_game_id, "status": "active", "started_at": datetime.utcnow(), "ended_at": None},
        ]
        for s in session_seeds:
            try:
                db.execute(
                    text(
                        "INSERT INTO game_sessions (game_id, status, started_at, ended_at) "
                        "VALUES (:game_id, :status, :started_at, :ended_at)"
                    ),
                    s,
                )
                added["sessions"] += 1
            except IntegrityError:
                db.rollback()
        db.commit()

    # ---------- Game Players ----------
    if first_game_id is not None and first_user_id is not None:
        player_seeds = [
            {"game_id": first_game_id, "user_id": first_user_id, "is_host": True, "joined_at": datetime.utcnow()},
            {"game_id": first_game_id, "user_id": first_user_id, "is_host": False, "joined_at": datetime.utcnow()},
            {"game_id": first_game_id, "user_id": first_user_id, "is_host": False, "joined_at": datetime.utcnow()},
            {"game_id": first_game_id, "user_id": first_user_id, "is_host": False, "joined_at": datetime.utcnow()},
            {"game_id": first_game_id, "user_id": first_user_id, "is_host": False, "joined_at": datetime.utcnow()},
        ]
        for p in player_seeds:
            try:
                db.execute(
                    text(
                        "INSERT INTO game_players (game_id, user_id, is_host, joined_at) "
                        "VALUES (:game_id, :user_id, :is_host, :joined_at)"
                    ),
                    p,
                )
                added["players"] += 1
            except IntegrityError:
                db.rollback()
        db.commit()

    # ---------- Game Histories ----------
    if first_game_id is not None:
        history_seeds = []
        for i in range(1, 6):
            history_seeds.append(
                {
                    "game_id": first_game_id,
                    "move_number": i,
                    "dice_value": (i % 6) + 1,
                    "position": i * 10,
                    "timestamp": datetime.utcnow(),
                }
            )
        for h in history_seeds:
            try:
                db.execute(
                    text(
                        "INSERT INTO game_histories (game_id, move_number, dice_value, position, timestamp) "
                        "VALUES (:game_id, :move_number, :dice_value, :position, :timestamp)"
                    ),
                    h,
                )
                added["histories"] += 1
            except IntegrityError:
                db.rollback()
        db.commit()

    # ---------- Leaderboard Entries ----------
    if first_user_id is not None:
        leaderboard_seeds = [
            {"user_id": first_user_id, "score": 1500, "rank": 1},
            {"user_id": first_user_id, "score": 1200, "rank": 2},
            {"user_id": first_user_id, "score": 1100, "rank": 3},
            {"user_id": first_user_id, "score": 900, "rank": 4},
            {"user_id": first_user_id, "score": 800, "rank": 5},
        ]
        for l in leaderboard_seeds:
            try:
                db.execute(
                    text(
                        "INSERT INTO leaderboard_entries (user_id, score, rank) "
                        "VALUES (:user_id, :score, :rank)"
                    ),
                    l,
                )
                added["leaderboard"] += 1
            except IntegrityError:
                db.rollback()
        db.commit()

    return {"message": "Seed data inserted", "counts": added}
