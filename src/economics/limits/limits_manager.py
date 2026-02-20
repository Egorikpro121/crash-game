"""Limits manager - manages all limit types."""
from decimal import Decimal
from typing import Dict
from sqlalchemy.orm import Session

from src.economics.limits.bet_limits import BetLimits
from src.economics.limits.withdrawal_limits import WithdrawalLimits
from src.economics.limits.deposit_limits import DepositLimits
from src.economics.limits.limits_validator import LimitsValidator


class LimitsManager:
    """Manage all limit types."""
    
    def __init__(self, db: Session):
        """
        Initialize limits manager.
        
        Args:
            db: Database session
        """
        self.db = db
        self.bet_limits = BetLimits()
        self.withdrawal_limits = WithdrawalLimits()
        self.deposit_limits = DepositLimits()
        self.validator = LimitsValidator(db)
    
    def get_all_limits(self) -> Dict:
        """
        Get all limit values.
        
        Returns:
            Dictionary with all limits
        """
        return {
            "bet": {
                "min_ton": float(self.bet_limits.MIN_BET_TON),
                "max_ton": float(self.bet_limits.MAX_BET_TON),
                "min_stars": float(self.bet_limits.MIN_BET_STARS),
                "max_stars": float(self.bet_limits.MAX_BET_STARS),
            },
            "withdrawal": {
                "min_ton": float(self.withdrawal_limits.MIN_WITHDRAWAL_TON),
                "max_ton": float(self.withdrawal_limits.MAX_WITHDRAWAL_TON),
                "max_daily_ton": float(self.withdrawal_limits.MAX_DAILY_WITHDRAWAL_TON),
                "min_stars": float(self.withdrawal_limits.MIN_WITHDRAWAL_STARS),
                "max_stars": float(self.withdrawal_limits.MAX_WITHDRAWAL_STARS),
                "max_daily_stars": float(self.withdrawal_limits.MAX_DAILY_WITHDRAWAL_STARS),
            },
            "deposit": {
                "min_ton": float(self.deposit_limits.MIN_DEPOSIT_TON),
                "max_ton": float(self.deposit_limits.MAX_DEPOSIT_TON),
                "max_daily_ton": float(self.deposit_limits.MAX_DAILY_DEPOSIT_TON),
                "min_stars": float(self.deposit_limits.MIN_DEPOSIT_STARS),
                "max_stars": float(self.deposit_limits.MAX_DEPOSIT_STARS),
                "max_daily_stars": float(self.deposit_limits.MAX_DAILY_DEPOSIT_STARS),
            },
        }
