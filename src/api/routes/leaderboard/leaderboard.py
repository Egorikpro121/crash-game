"""Leaderboard API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.connection import get_db
from src.services.leaderboard import LeaderboardService

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/top")
def get_top_earners(
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get top earners."""
    service = LeaderboardService(db)
    return service.get_top_earners(limit)
