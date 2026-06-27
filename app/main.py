from fastapi import FastAPI

# Model imports
from app.models.game_sessions import *  # noqa: F401
from app.models.game_histories import *  # noqa: F401
from app.models.users import *  # noqa: F401
from app.models.leaderboard_entries import *  # noqa: F401
from app.models.chat_messages import *  # noqa: F401
from app.models.game_players import *  # noqa: F401
from app.models.moves import *  # noqa: F401
from app.models.teams import *  # noqa: F401

# Router imports
from app.routes.stats_routes import stats_router
from app.routes.auth_routes import auth_router
from app.routes.seed_routes import seed_router
from app.routes.user_routes import user_router
from app.routes.game_routes import game_router
from app.routes.player_routes import player_router
from app.routes.move_routes import move_router
from app.routes.leaderboard_routes import leaderboard_router

# Database imports
from app.database import Base, engine

app = FastAPI()

# CORS (required for frontend access)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health endpoint (required for deployment health checks)
@app.get("/health")
def health():
    return {"status": "ok"}

# Create tables
Base.metadata.create_all(bind=engine)

# Router registrations
app.include_router(stats_router)
app.include_router(auth_router)
app.include_router(seed_router)
app.include_router(user_router)
app.include_router(game_router)
app.include_router(player_router)
app.include_router(move_router)
app.include_router(leaderboard_router)
