"""Referral management system."""
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session

from src.database.repositories.user_repo import UserRepository
from src.economics.referrals.referral_calculator import ReferralCalculator
from src.economics.referrals.referral_tracker import ReferralTracker


class ReferralManager:
    """Manage referral system."""
    
    def __init__(self, db: Session):
        """
        Initialize referral manager.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.calculator = ReferralCalculator(db)
        self.tracker = ReferralTracker(db)
    
    def create_referral_code(self, user_id: int) -> str:
        """
        Create referral code for user.
        
        Args:
            user_id: User ID
        
        Returns:
            Referral code
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Generate referral code from user ID
        import hashlib
        code = hashlib.sha256(f"{user_id}_{user.telegram_user_id}".encode()).hexdigest()[:8].upper()
        
        # Update user referral code
        user.referral_code = code
        self.db.commit()
        
        return code
    
    def get_referral_code(self, user_id: int) -> Optional[str]:
        """
        Get user's referral code.
        
        Args:
            user_id: User ID
        
        Returns:
            Referral code or None
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None
        
        if not user.referral_code:
            return self.create_referral_code(user_id)
        
        return user.referral_code
    
    def register_referral(
        self,
        referrer_id: int,
        referred_id: int
    ) -> bool:
        """
        Register a referral relationship.
        
        Args:
            referrer_id: User who referred
            referred_id: User who was referred
        
        Returns:
            True if successful
        """
        if referrer_id == referred_id:
            return False
        
        referred_user = self.user_repo.get_by_id(referred_id)
        if not referred_user:
            return False
        
        # Check if already has referrer
        if referred_user.referred_by_id:
            return False
        
        # Set referrer
        referred_user.referred_by_id = referrer_id
        self.db.commit()
        
        # Track referral
        self.tracker.track_referral(referrer_id, referred_id)
        
        return True
    
    def process_referral_payout(
        self,
        referrer_id: int,
        referred_id: int,
        deposit_amount: Decimal,
        currency: str
    ) -> Decimal:
        """
        Process referral payout when referred user makes deposit.
        
        Args:
            referrer_id: User who referred
            referred_id: User who made deposit
            deposit_amount: Deposit amount
            currency: Currency
        
        Returns:
            Referral payout amount
        """
        payout = self.calculator.calculate_referral_payout(
            deposit_amount, currency
        )
        
        if payout > 0:
            self.calculator.apply_referral_payout(
                referrer_id, referred_id, payout, currency
            )
        
        return payout
