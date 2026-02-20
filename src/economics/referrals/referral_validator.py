"""Referral validation system."""
from typing import Optional, Tuple
from sqlalchemy.orm import Session

from src.database.repositories.user_repo import UserRepository


class ReferralValidator:
    """Validate referral operations."""
    
    def __init__(self, db: Session):
        """
        Initialize referral validator.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
    
    def validate_referral_code(self, referral_code: str) -> Tuple[bool, Optional[str]]:
        """
        Validate referral code.
        
        Args:
            referral_code: Referral code to validate
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not referral_code or len(referral_code) < 4:
            return False, "Invalid referral code format"
        
        referrer = self.user_repo.get_by_referral_code(referral_code)
        if not referrer:
            return False, "Referral code not found"
        
        if referrer.is_banned:
            return False, "Referrer is banned"
        
        return True, None
    
    def validate_referral_registration(
        self,
        referrer_id: int,
        referred_id: int
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate referral registration.
        
        Args:
            referrer_id: User who referred
            referred_id: User who was referred
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if referrer_id == referred_id:
            return False, "Cannot refer yourself"
        
        referrer = self.user_repo.get_by_id(referrer_id)
        if not referrer:
            return False, "Referrer not found"
        
        if referrer.is_banned:
            return False, "Referrer is banned"
        
        referred = self.user_repo.get_by_id(referred_id)
        if not referred:
            return False, "Referred user not found"
        
        if referred.referred_by_id:
            return False, "User already has a referrer"
        
        return True, None
