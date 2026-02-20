"""Leaderboard service."""
from sqlalchemy.orm import Session
from src.database.repositories.user_repo import UserRepository

class LeaderboardService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def get_top_earners(self, limit: int = 100):
        return self.user_repo.get_top_earners(limit)
