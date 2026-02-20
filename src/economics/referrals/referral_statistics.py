"""Referral statistics system."""
from decimal import Decimal
from typing import Dict
from sqlalchemy.orm import Session

from src.database.repositories.user_repo import UserRepository
from src.economics.referrals.referral_tracker import ReferralTracker


class ReferralStatistics:
    """Generate referral statistics."""
    
    def __init__(self, db: Session):
        """
        Initialize referral statistics handler.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.tracker = ReferralTracker(db)
    
    def get_user_statistics(self, user_id: int) -> Dict:
        """
        Get comprehensive referral statistics for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            Referral statistics
        """
        return self.tracker.get_referral_statistics(user_id)
    
    def get_global_statistics(self) -> Dict:
        """
        Get global referral statistics.
        
        Returns:
            Global statistics
        """
        users = self.user_repo.get_active_users(limit=10000)
        
        total_referrals = 0
        total_referral_earnings_ton = Decimal("0.0")
        total_referral_earnings_stars = Decimal("0.0")
        users_with_referrals = 0
        
        for user in users:
            if user.referral_count and user.referral_count > 0:
                total_referrals += user.referral_count
                total_referral_earnings_ton += user.total_referral_earnings_ton or Decimal("0.0")
                total_referral_earnings_stars += user.total_referral_earnings_stars or Decimal("0.0")
                users_with_referrals += 1
        
        return {
            "total_referrals": total_referrals,
            "total_referral_earnings_ton": float(total_referral_earnings_ton),
            "total_referral_earnings_stars": float(total_referral_earnings_stars),
            "users_with_referrals": users_with_referrals,
            "total_users": len(users),
        }
