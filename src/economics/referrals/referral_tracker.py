"""Referral tracking system."""
from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy.orm import Session

from src.database.repositories.user_repo import UserRepository


class ReferralTracker:
    """Track referral relationships and statistics."""
    
    def __init__(self, db: Session):
        """
        Initialize referral tracker.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
    
    def track_referral(self, referrer_id: int, referred_id: int):
        """
        Track a referral relationship.
        
        Args:
            referrer_id: User who referred
            referred_id: User who was referred
        """
        referrer = self.user_repo.get_by_id(referrer_id)
        if referrer:
            referrer.referral_count = (referrer.referral_count or 0) + 1
            self.db.commit()
    
    def get_referrals(self, referrer_id: int) -> List[Dict]:
        """
        Get all referrals for a user.
        
        Args:
            referrer_id: User ID
        
        Returns:
            List of referral records
        """
        # Get all users referred by this user
        referred_users = self.user_repo.get_by_referrer_id(referrer_id)
        
        referrals = []
        for user in referred_users:
            referrals.append({
                "user_id": user.id,
                "telegram_id": user.telegram_id,
                "username": user.username,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "total_deposited_ton": float(user.total_deposited_ton or 0),
                "total_deposited_stars": float(user.total_deposited_stars or 0),
            })
        
        return referrals
    
    def get_referral_statistics(self, referrer_id: int) -> Dict:
        """
        Get referral statistics for a user.
        
        Args:
            referrer_id: User ID
        
        Returns:
            Referral statistics
        """
        referrer = self.user_repo.get_by_id(referrer_id)
        if not referrer:
            return {}
        
        referrals = self.get_referrals(referrer_id)
        
        total_deposits_ton = sum(r["total_deposited_ton"] for r in referrals)
        total_deposits_stars = sum(r["total_deposited_stars"] for r in referrals)
        
        return {
            "referral_count": len(referrals),
            "total_referral_earnings_ton": float(referrer.total_referral_earnings_ton or 0),
            "total_referral_earnings_stars": float(referrer.total_referral_earnings_stars or 0),
            "total_referred_deposits_ton": total_deposits_ton,
            "total_referred_deposits_stars": total_deposits_stars,
            "referrals": referrals,
        }
