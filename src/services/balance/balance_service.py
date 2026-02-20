"""Balance service."""
from sqlalchemy.orm import Session
from src.database.repositories.user_repo import UserRepository

class BalanceService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def get_balance(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        return {"ton": user.balance_ton, "stars": user.balance_stars} if user else None
