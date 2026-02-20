"""Limits validator - validates all types of limits."""
from decimal import Decimal
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from src.economics.limits.bet_limits import BetLimits
from src.economics.limits.withdrawal_limits import WithdrawalLimits
from src.economics.limits.deposit_limits import DepositLimits
from src.database.repositories.payment_repo import PaymentRepository, PaymentType
from src.database.repositories.user_repo import UserRepository


class LimitsValidator:
    """Validate all types of limits."""
    
    def __init__(self, db: Session):
        """
        Initialize limits validator.
        
        Args:
            db: Database session
        """
        self.db = db
        self.bet_limits = BetLimits()
        self.withdrawal_limits = WithdrawalLimits()
        self.deposit_limits = DepositLimits()
        self.payment_repo = PaymentRepository(db)
        self.user_repo = UserRepository(db)
    
    def validate_bet(
        self,
        amount: Decimal,
        currency: str,
        user_id: int
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate bet amount and user balance.
        
        Args:
            amount: Bet amount
            currency: Currency
            user_id: User ID
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate bet limits
        is_valid, error = self.bet_limits.validate_bet_amount(amount, currency)
        if not is_valid:
            return False, error
        
        # Validate user balance
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False, "User not found"
        
        balance = (
            user.balance_ton if currency == "TON"
            else user.balance_stars
        )
        
        if balance < amount:
            return False, f"Insufficient balance. Available: {balance} {currency}"
        
        return True, None
    
    def validate_withdrawal(
        self,
        amount: Decimal,
        currency: str,
        user_id: int
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate withdrawal amount and limits.
        
        Args:
            amount: Withdrawal amount
            currency: Currency
            user_id: User ID
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate withdrawal limits
        is_valid, error = self.withdrawal_limits.validate_withdrawal_amount(
            amount, currency
        )
        if not is_valid:
            return False, error
        
        # Validate user balance
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False, "User not found"
        
        balance = (
            user.balance_ton if currency == "TON"
            else user.balance_stars
        )
        
        if balance < amount:
            return False, f"Insufficient balance. Available: {balance} {currency}"
        
        # Validate daily limit
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_withdrawals = self.payment_repo.get_user_payments(
            user_id, PaymentType.WITHDRAWAL
        )
        daily_total = sum(
            p.amount for p in today_withdrawals
            if p.created_at and p.created_at >= today_start
            and p.currency == currency
        )
        
        is_valid, error = self.withdrawal_limits.validate_daily_limit(
            Decimal(str(daily_total)), amount, currency
        )
        if not is_valid:
            return False, error
        
        return True, None
    
    def validate_deposit(
        self,
        amount: Decimal,
        currency: str,
        user_id: Optional[int] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate deposit amount and limits.
        
        Args:
            amount: Deposit amount
            currency: Currency
            user_id: User ID (optional)
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate deposit limits
        is_valid, error = self.deposit_limits.validate_deposit_amount(
            amount, currency
        )
        if not is_valid:
            return False, error
        
        # Validate daily limit if user_id provided
        if user_id:
            today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            today_deposits = self.payment_repo.get_user_payments(
                user_id, PaymentType.DEPOSIT
            )
            daily_total = sum(
                p.amount for p in today_deposits
                if p.created_at and p.created_at >= today_start
                and p.currency == currency
            )
            
            is_valid, error = self.deposit_limits.validate_daily_limit(
                Decimal(str(daily_total)), amount, currency
            )
            if not is_valid:
                return False, error
        
        return True, None
