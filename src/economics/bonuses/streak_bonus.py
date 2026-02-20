"""Streak bonus system."""
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.database.repositories.user_repo import UserRepository
from src.database.repositories.transaction_repo import TransactionRepository, TransactionType


class StreakBonus:
    """Handle streak bonuses for consecutive days."""
    
    def __init__(self, db: Session):
        """
        Initialize streak bonus handler.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.transaction_repo = TransactionRepository(db)
    
    def calculate_streak_days(self, user_id: int) -> int:
        """
        Calculate current streak of consecutive days with activity.
        
        Args:
            user_id: User ID
        
        Returns:
            Number of consecutive days
        """
        # Check transactions for daily activity
        transactions = self.transaction_repo.get_user_transactions(user_id)
        
        if not transactions:
            return 0
        
        # Group by date
        activity_dates = set()
        for transaction in transactions:
            if transaction.created_at:
                activity_dates.add(transaction.created_at.date())
        
        if not activity_dates:
            return 0
        
        # Calculate streak
        today = datetime.utcnow().date()
        streak = 0
        current_date = today
        
        while current_date in activity_dates:
            streak += 1
            current_date -= timedelta(days=1)
        
        return streak
    
    def calculate_streak_bonus(
        self,
        user_id: int,
        currency: str
    ) -> Decimal:
        """
        Calculate streak bonus based on consecutive days.
        
        Args:
            user_id: User ID
            currency: Currency
        
        Returns:
            Streak bonus amount
        """
        streak_days = self.calculate_streak_days(user_id)
        
        if streak_days == 0:
            return Decimal("0.0")
        
        # 0.01 TON per day, max 0.5 TON
        base_bonus = (
            Decimal("0.01") if currency == "TON"
            else Decimal("1")
        )
        max_bonus = (
            Decimal("0.5") if currency == "TON"
            else Decimal("50")
        )
        
        bonus = base_bonus * Decimal(streak_days)
        return min(bonus, max_bonus)
    
    def apply_streak_bonus(self, user_id: int, currency: str) -> Decimal:
        """
        Apply streak bonus to user.
        
        Args:
            user_id: User ID
            currency: Currency
        
        Returns:
            Bonus amount applied
        """
        bonus_amount = self.calculate_streak_bonus(user_id, currency)
        
        if bonus_amount > 0:
            user = self.user_repo.get_by_id(user_id)
            streak_days = self.calculate_streak_days(user_id)
            
            if currency == "TON":
                self.user_repo.update_balance(user_id, amount_ton=bonus_amount)
                balance_before = user.balance_ton
                balance_after = balance_before + bonus_amount
            else:
                self.user_repo.update_balance(user_id, amount_stars=bonus_amount)
                balance_before = user.balance_stars
                balance_after = balance_before + bonus_amount
            
            # Create transaction record
            self.transaction_repo.create(
                user_id=user_id,
                transaction_type=TransactionType.BONUS,
                currency=currency,
                amount=bonus_amount,
                balance_before=balance_before,
                balance_after=balance_after,
                description=f"Streak bonus ({streak_days} days): {bonus_amount} {currency}",
            )
        
        return bonus_amount
