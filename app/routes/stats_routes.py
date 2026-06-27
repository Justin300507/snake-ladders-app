from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.game_sessions import GameSession
from app.models.game_histories import GameHistory
from app.models.users import User
from app.models.leaderboard_entries import LeaderboardEntries
from app.models.chat_messages import ChatMessage

stats_router = APIRouter()

@stats_router.get("/stats/summary")
def get_stats_summary(db: Session = Depends(get_db)):
    """
    Return aggregate counts and key metrics for dashboard overview.
    """
    total_users = db.query(User).count()
    total_games = db.query(GameSession).count()
    total_histories = db.query(GameHistory).count()
    total_chat_messages = db.query(ChatMessage).count()
    total_leaderboard_entries = db.query(LeaderboardEntries).count()

    return {
        "total_users": total_users,
        "total_games": total_games,
        "total_histories": total_histories,
        "total_chat_messages": total_chat_messages,
        "total_leaderboard_entries": total_leaderboard_entries,
    }
