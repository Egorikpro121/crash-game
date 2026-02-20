"""Activity bonus system."""
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.database.repositories.user_repo import UserRepository
from src.database.repositories.game_repo import BetRepository
from src.database.repositories.transaction_repo import TransactionRepository, TransactionType


class ActivityBonus:
    """Handle activity-based bonuses."""
    
    def __init__(self, db: Session):
        """
        Initialize activity bonus handler.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.bet_repo = BetRepository(db)
        self.transaction_repo = TransactionRepository(db)
    
    def calculate_activity_bonus(
        self,
        user_id: int,
        currency: str,
        period_days: int = 1
    ) -> Decimal:
        """
        Calculate activity bonus based on bets in period.
        
        Args:
            user_id: User ID
            currency: Currency
            period_days: Period in days to check
        
        Returns:
            Activity bonus amount
        """
        period_start = datetime.utcnow() - timedelta(days=period_days)
        
        # Get user bets in period
        bets = self.bet_repo.get_user_bets(user_id, limit=10000)
        period_bets = [
            bet for bet in bets
            if bet.placed_at >= period_start
        ]
        
        bets_count = len(period_bets)
        
        # Calculate bonus: 0.001 TON per bet, max 0.1 TON
        base_bonus = (
            Decimal("0.001") if currency == "TON"
            else Decimal("0.1")
        )
        max_bonus = (
            Decimal("0.1") if currency == "TON"
            else Decimal("10")
        )
        
        bonus = base_bonus * Decimal(bets_count)
        return min(bonus, max_bonus)
    
    def apply_activity_bonus(
        self,
        user_id: int,
        currency: str,
        period_days: int = 1
    ) -> Decimal:
        """
        Apply activity bonus to user.
        
        Args:
            user_id: User ID
            currency: Currency
            period_days: Period in days
        
        Returns:
            Bonus amount applied
        """
        bonus_amount = self.calculate_activity_bonus(user_id, currency, period_days)
        
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
                description=f"Activity bonus ({period_days} days): {bonus_amount} {currency}",
            )
        
        return bonus_amount
