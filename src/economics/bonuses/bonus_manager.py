"""Bonus manager - coordinates all bonus types."""
from decimal import Decimal
from typing import Dict, List
from sqlalchemy.orm import Session

from src.economics.bonuses.first_deposit import FirstDepositBonus
from src.economics.bonuses.daily_bonus import DailyBonus
from src.economics.bonuses.activity_bonus import ActivityBonus
from src.economics.bonuses.streak_bonus import StreakBonus
from src.economics.bonuses.vip_bonus import VIPBonus


class BonusManager:
    """Manage all bonus types."""
    
    def __init__(self, db: Session):
        """
        Initialize bonus manager.
        
        Args:
            db: Database session
        """
        self.db = db
        self.first_deposit = FirstDepositBonus(db)
        self.daily = DailyBonus(db)
        self.activity = ActivityBonus(db)
        self.streak = StreakBonus(db)
        self.vip = VIPBonus(db)
    
    def get_available_bonuses(self, user_id: int, currency: str) -> Dict[str, Decimal]:
        """
        Get all available bonuses for user.
        
        Args:
            user_id: User ID
            currency: Currency
        
        Returns:
            Dictionary with available bonuses
        """
        return {
            "daily": self.daily.get_available_bonus(currency) if not self.daily.has_claimed_today(user_id) else Decimal("0.0"),
            "activity": self.activity.calculate_activity_bonus(user_id, currency),
            "streak": self.streak.calculate_streak_bonus(user_id, currency),
            "vip": self.vip.calculate_vip_bonus(user_id, currency),
        }
    
    def claim_all_available(self, user_id: int, currency: str) -> Dict[str, Decimal]:
        """
        Claim all available bonuses.
        
        Args:
            user_id: User ID
            currency: Currency
        
        Returns:
            Dictionary with claimed bonuses
        """
        claimed = {}
        
        # Daily bonus
        daily_amount = self.daily.claim_daily_bonus(user_id, currency)
        if daily_amount > 0:
            claimed["daily"] = daily_amount
        
        # Activity bonus
        activity_amount = self.activity.apply_activity_bonus(user_id, currency)
        if activity_amount > 0:
            claimed["activity"] = activity_amount
        
        # Streak bonus
        streak_amount = self.streak.apply_streak_bonus(user_id, currency)
        if streak_amount > 0:
            claimed["streak"] = streak_amount
        
        # VIP bonus
        vip_amount = self.vip.apply_vip_bonus(user_id, currency)
        if vip_amount > 0:
            claimed["vip"] = vip_amount
        
        return claimed
    
    def apply_first_deposit_bonus(
        self,
        user_id: int,
        deposit_amount: Decimal,
        currency: str,
        payment_id: int
    ) -> Decimal:
        """
        Apply first deposit bonus.
        
        Args:
            user_id: User ID
            deposit_amount: Deposit amount
            currency: Currency
            payment_id: Payment ID
        
        Returns:
            Bonus amount
        """
        return self.first_deposit.apply_bonus(user_id, deposit_amount, currency, payment_id)
