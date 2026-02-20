"""First deposit bonus system."""
from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session

from src.database.repositories.user_repo import UserRepository
from src.database.repositories.payment_repo import PaymentRepository, PaymentType
from src.database.repositories.transaction_repo import TransactionRepository, TransactionType
from src.economics.core.bonus_calculator import BonusCalculator


class FirstDepositBonus:
    """Handle first deposit bonuses."""
    
    def __init__(self, db: Session):
        """
        Initialize first deposit bonus handler.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.payment_repo = PaymentRepository(db)
        self.transaction_repo = TransactionRepository(db)
        self.bonus_calculator = BonusCalculator()
    
    def is_eligible(self, user_id: int, currency: str) -> bool:
        """
        Check if user is eligible for first deposit bonus.
        
        Args:
            user_id: User ID
            currency: Currency
        
        Returns:
            True if eligible
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False
        
        # Check if user has made any deposits before
        if currency == "TON":
            return user.total_deposited_ton == Decimal("0.0")
        else:
            return user.total_deposited_stars == Decimal("0.0")
    
    def calculate_bonus(self, deposit_amount: Decimal, currency: str) -> Decimal:
        """
        Calculate first deposit bonus amount.
        
        Args:
            deposit_amount: Deposit amount
            currency: Currency
        
        Returns:
            Bonus amount
        """
        return self.bonus_calculator.calculate_first_deposit_bonus(
            deposit_amount, currency
        )
    
    def apply_bonus(
        self,
        user_id: int,
        deposit_amount: Decimal,
        currency: str,
        payment_id: int
    ) -> Decimal:
        """
        Apply first deposit bonus to user account.
        
        Args:
            user_id: User ID
            deposit_amount: Deposit amount
            currency: Currency
            payment_id: Payment ID
        
        Returns:
            Bonus amount applied
        """
        if not self.is_eligible(user_id, currency):
            return Decimal("0.0")
        
        bonus_amount = self.calculate_bonus(deposit_amount, currency)
        
        if bonus_amount > 0:
            # Add bonus to user balance
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
                description=f"First deposit bonus: {bonus_amount} {currency}",
                payment_id=payment_id,
            )
        
        return bonus_amount
