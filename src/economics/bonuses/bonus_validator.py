"""Bonus validation system."""
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session

from src.database.repositories.user_repo import UserRepository
from src.database.repositories.transaction_repo import TransactionRepository, TransactionType


class BonusValidator:
    """Validate bonus eligibility and amounts."""
    
    def __init__(self, db: Session):
        """
        Initialize bonus validator.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.transaction_repo = TransactionRepository(db)
    
    def validate_first_deposit_bonus(
        self,
        user_id: int,
        deposit_amount: Decimal,
        currency: str
    ) -> tuple[bool, Optional[str]]:
        """
        Validate first deposit bonus eligibility.
        
        Args:
            user_id: User ID
            deposit_amount: Deposit amount
            currency: Currency
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False, "User not found"
        
        # Check minimum deposit
        min_deposit = Decimal("0.1") if currency == "TON" else Decimal("10")
        if deposit_amount < min_deposit:
            return False, f"Minimum deposit is {min_deposit} {currency}"
        
        # Check if already received first deposit bonus
        if currency == "TON":
            if user.total_deposited_ton > Decimal("0.0"):
                return False, "First deposit bonus already claimed"
        else:
            if user.total_deposited_stars > Decimal("0.0"):
                return False, "First deposit bonus already claimed"
        
        return True, None
    
    def validate_daily_bonus(
        self,
        user_id: int
    ) -> tuple[bool, Optional[str]]:
        """
        Validate daily bonus eligibility.
        
        Args:
            user_id: User ID
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False, "User not found"
        
        # Check if already claimed today
        from src.economics.bonuses.daily_bonus import DailyBonus
        daily_bonus = DailyBonus(self.db)
        
        if daily_bonus.has_claimed_today(user_id):
            return False, "Daily bonus already claimed today"
        
        return True, None
    
    def validate_bonus_amount(
        self,
        bonus_amount: Decimal,
        currency: str,
        bonus_type: str
    ) -> tuple[bool, Optional[str]]:
        """
        Validate bonus amount.
        
        Args:
            bonus_amount: Bonus amount
            currency: Currency
            bonus_type: Type of bonus
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if bonus_amount <= 0:
            return False, "Bonus amount must be positive"
        
        # Maximum bonus limits
        max_bonuses = {
            "daily": Decimal("1.0") if currency == "TON" else Decimal("100"),
            "activity": Decimal("0.5") if currency == "TON" else Decimal("50"),
            "streak": Decimal("1.0") if currency == "TON" else Decimal("100"),
            "vip": Decimal("5.0") if currency == "TON" else Decimal("500"),
        }
        
        max_bonus = max_bonuses.get(bonus_type)
        if max_bonus and bonus_amount > max_bonus:
            return False, f"Bonus amount exceeds maximum of {max_bonus} {currency}"
        
        return True, None
