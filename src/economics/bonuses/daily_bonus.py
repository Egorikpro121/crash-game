"""Daily bonus system."""
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.database.repositories.user_repo import UserRepository
from src.database.repositories.transaction_repo import TransactionRepository, TransactionType
from src.economics.core.bonus_calculator import BonusCalculator


class DailyBonus:
    """Handle daily bonuses."""
    
    def __init__(self, db: Session):
        """
        Initialize daily bonus handler.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.transaction_repo = TransactionRepository(db)
        self.bonus_calculator = BonusCalculator()
    
    def has_claimed_today(self, user_id: int) -> bool:
        """
        Check if user has claimed daily bonus today.
        
        Args:
            user_id: User ID
        
        Returns:
            True if already claimed
        """
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Check transactions for today's bonus
        transactions = self.transaction_repo.get_user_transactions(
            user_id, TransactionType.BONUS
        )
        
        for transaction in transactions:
            if transaction.description and "Daily bonus" in transaction.description:
                if transaction.created_at >= today_start:
                    return True
        
        return False
    
    def claim_daily_bonus(self, user_id: int, currency: str) -> Decimal:
        """
        Claim daily bonus for user.
        
        Args:
            user_id: User ID
            currency: Currency
        
        Returns:
            Bonus amount claimed
        """
        if self.has_claimed_today(user_id):
            return Decimal("0.0")
        
        bonus_amount = self.bonus_calculator.get_daily_bonus_amount(currency)
        
        if bonus_amount > 0:
            user = self.user_repo.get_by_id(user_id)
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
                description=f"Daily bonus: {bonus_amount} {currency}",
            )
        
        return bonus_amount
    
    def get_available_bonus(self, currency: str) -> Decimal:
        """
        Get available daily bonus amount.
        
        Args:
            currency: Currency
        
        Returns:
            Available bonus amount
        """
        return self.bonus_calculator.get_daily_bonus_amount(currency)
