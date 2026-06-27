import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.database import get_db
from app.models.users import User
from app.models.game_sessions import GameSession
from app.models.game_histories import GameHistory
from app.models.leaderboard_entries import LeaderboardEntries
from app.models.chat_messages import ChatMessage
from app.utils.auth import get_password_hash

seed_router = APIRouter()

@seed_router.post("/seed")
def seed(db: Session = Depends(get_db)):
    # ---------- Users ----------
    users_data = [
        {
            "email": "alex.chen@example.com",
            "password_hash": get_password_hash("SecurePass1"),
            "display_name": "Alex Chen",
            "role": "player",
        },
        {
            "email": "maria.garcia@example.com",
            "password_hash": get_password_hash("SecurePass2"),
            "display_name": "Maria Garcia",
            "role": "player",
        },
        {
            "email": "james.kim@example.com",
            "password_hash": get_password_hash("SecurePass3"),
            "display_name": "James Kim",
            "role": "player",
        },
        {
            "email": "linda.park@example.com",
            "password_hash": get_password_hash("SecurePass4"),
            "display_name": "Linda Park",
            "role": "admin",
        },
        {
            "email": "roberto.sanchez@example.com",
            "password_hash": get_password_hash("SecurePass5"),
            "display_name": "Roberto Sanchez",
            "role": "player",
        },
    ]
    for user_dict in users_data:
        existing = db.query(User).filter(User.email == user_dict["email"]).first()
        if existing:
            continue
        user = User(**user_dict)
        db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()

    # ---------- Game Sessions ----------
    sessions_data = [
        {"title": "Morning Yoga", "description": "A calming start to the day", "board_theme": "zen"},
        {"title": "Evening HIIT", "description": "High intensity interval training", "board_theme": "gym"},
        {"title": "Strategy Blitz", "description": "Fast‑paced strategy game", "board_theme": "space"},
        {"title": "Puzzle Quest", "description": "Solve riddles and advance", "board_theme": "forest"},
        {"title": "Retro Arcade", "description": "Classic arcade fun", "board_theme": "retro"},
    ]
    for sess_dict in sessions_data:
        session = GameSession(**sess_dict)
        db.add(session)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()

    # Retrieve session ids for FK usage
    session_ids = [s.id for s in db.query(GameSession.id).all()]
    if not session_ids:
        raise HTTPException(status_code=500, detail="Failed to create game sessions")

    # ---------- Game Histories ----------
    histories_data = [
        {"game_id": session_ids[0], "action": "started", "timestamp": func.now()},
        {"game_id": session_ids[1], "action": "player_joined", "timestamp": func.now()},
        {"game_id": session_ids[2], "action": "move_made", "timestamp": func.now()},
        {"game_id": session_ids[3], "action": "puzzle_solved", "timestamp": func.now()},
        {"game_id": session_ids[4], "action": "high_score", "timestamp": func.now()},
    ]
    for hist_dict in histories_data:
        history = GameHistory(**hist_dict)
        db.add(history)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()

    # ---------- Leaderboard Entries ----------
    # Use the first five users created above
    user_ids = [u.id for u in db.query(User.id).limit(5).all()]
    leaderboard_data = [
        {"user_id": user_ids[0], "score": 1500.0},
        {"user_id": user_ids[1], "score": 1320.5},
        {"user_id": user_ids[2], "score": 1580.2},
        {"user_id": user_ids[3], "score": 1400.0},
        {"user_id": user_ids[4], "score": 1250.7},
    ]
    for entry_dict in leaderboard_data:
        entry = LeaderboardEntries(**entry_dict)
        db.add(entry)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()

    # ---------- Chat Messages ----------
    messages_data = [
        {"game_id": session_ids[0], "user_id": user_ids[0], "content": "Good luck everyone!", "timestamp": func.now()},
        {"game_id": session_ids[1], "user_id": user_ids[1], "content": "Ready to start?", "timestamp": func.now()},
        {"game_id": session_ids[2], "user_id": user_ids[2], "content": "Nice move!", "timestamp": func.now()},
        {"game_id": session_ids[3], "user_id": user_ids[3], "content": "I solved it!", "timestamp": func.now()},
        {"game_id": session_ids[4], "user_id": user_ids[4], "content": "High score!", "timestamp": func.now()},
    ]
    for msg_dict in messages_data:
        message = ChatMessage(**msg_dict)
        db.add(message)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()

    return {"detail": "Demo data seeded successfully"}