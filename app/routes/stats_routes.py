from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.users import Users
from app.models.game_sessions import GameSession
from app.models.moves import Move
from app.models.leaderboard_entries import LeaderboardEntry

stats_router = APIRouter()


@stats_router.get("/stats/summary")
def get_stats_summary(db: Session = Depends(get_db)):
    total_users = db.query(Users).count()
    active_games = db.query(GameSession).filter(GameSession.status == "active").count()

    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    moves_today = db.query(Move).filter(Move.timestamp >= today_start).count()

    avg_rating_result = db.query(func.avg(LeaderboardEntry.rating)).scalar()
    average_rating = float(avg_rating_result) if avg_rating_result else 0.0

    return {
        "total_users": total_users,
        "active_games": active_games,
        "moves_today": moves_today,
        "average_rating": average_rating,
    }
