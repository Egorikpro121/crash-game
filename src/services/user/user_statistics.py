"""User statistics service."""
from decimal import Decimal
from typing import Dict, Optional
from sqlalchemy.orm import Session

from src.database.repositories.user_repo import UserRepository
from src.database.models.user import User


class UserStatisticsService:
    """User statistics service."""
    
    def __init__(self, db: Session):
        """
        Initialize user statistics service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
    
    def get_user_statistics(self, user_id: int) -> Optional[Dict]:
        """
        Get comprehensive statistics for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            Statistics dictionary
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None
        
        return {
            "user_id": user_id,
            "balance_ton": float(user.balance_ton or Decimal("0.0")),
            "balance_stars": float(user.balance_stars or Decimal("0.0")),
            "total_deposited_ton": float(user.total_deposited_ton or Decimal("0.0")),
            "total_deposited_stars": float(user.total_deposited_stars or Decimal("0.0")),
            "total_withdrawn_ton": float(user.total_withdrawn_ton or Decimal("0.0")),
            "total_withdrawn_stars": float(user.total_withdrawn_stars or Decimal("0.0")),
            "total_won_ton": float(user.total_won_ton or Decimal("0.0")),
            "total_won_stars": float(user.total_won_stars or Decimal("0.0")),
            "total_lost_ton": float(user.total_lost_ton or Decimal("0.0")),
            "total_lost_stars": float(user.total_lost_stars or Decimal("0.0")),
            "total_bets": user.total_bets or 0,
            "total_cashouts": user.total_cashouts or 0,
            "biggest_win_ton": float(user.biggest_win_ton or Decimal("0.0")),
            "biggest_win_stars": float(user.biggest_win_stars or Decimal("0.0")),
            "biggest_multiplier": float(user.biggest_multiplier or Decimal("0.0")),
            "win_rate": self._calculate_win_rate(user),
        }
    
    def _calculate_win_rate(self, user: User) -> float:
        """Calculate win rate."""
        total_bets = user.total_bets or 0
        if total_bets == 0:
            return 0.0
        
        cashouts = user.total_cashouts or 0
        return (cashouts / total_bets) * 100.0
    
    def update_statistics(
        self,
        user_id: int,
        **kwargs
    ) -> User:
        """
        Update user statistics.
        
        Args:
            user_id: User ID
            **kwargs: Statistics to update
        
        Returns:
            Updated user
        """
        return self.user_repo.update_statistics(user_id, **kwargs)
