"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.connection import init_db
from src.api.middleware.security import setup_cors, security_headers_middleware
from src.api.routes import auth, game, payments, user
from src.api.routes.bonuses import bonuses
from src.api.routes.referrals import referrals
from src.api.routes.leaderboard import leaderboard

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="Crash Game API",
    description="Telegram Mini App Crash Game API",
    version="1.0.0"
)

# Setup CORS
setup_cors(app)

# Add security headers middleware
app.middleware("http")(security_headers_middleware)

# Include routers
app.include_router(auth.router)
app.include_router(game.router)
app.include_router(payments.router)
app.include_router(user.router)
app.include_router(bonuses.router)
app.include_router(referrals.router)
app.include_router(leaderboard.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Crash Game API", "version": "1.0.0"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
