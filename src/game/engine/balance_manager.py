"""Balance manager for crash game."""
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session

from src.database.models.user import User
from src.database.models.transaction import Transaction, TransactionType
from src.database.repositories.user_repo import UserRepository
from src.database.repositories.transaction_repo import TransactionRepository


class BalanceManager:
    """Manage user balances."""
    
    def __init__(self, db: Session):
        """
        Initialize balance manager.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.transaction_repo = TransactionRepository(db)
    
    def get_balance(self, user_id: int, currency: str) -> Decimal:
        """
        Get user balance.
        
        Args:
            user_id: User ID
            currency: Currency ("TON" or "STARS")
        
        Returns:
            Balance
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        if currency == "TON":
            return user.balance_ton
        elif currency == "STARS":
            return user.balance_stars
        else:
            raise ValueError(f"Invalid currency: {currency}")
    
    def deduct_balance(self, user_id: int, amount: Decimal, currency: str,
                      description: Optional[str] = None,
                      bet_id: Optional[int] = None,
                      round_id: Optional[int] = None) -> Decimal:
        """
        Deduct balance (for bets).
        
        Args:
            user_id: User ID
            amount: Amount to deduct
            currency: Currency
            description: Transaction description
            bet_id: Optional bet ID
            round_id: Optional round ID
        
        Returns:
            New balance
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        # Get current balance
        if currency == "TON":
            balance_before = user.balance_ton
            if balance_before < amount:
                raise ValueError("Insufficient balance")
            balance_after = balance_before - amount
            self.user_repo.update_balance(user_id, amount_ton=-amount)
        elif currency == "STARS":
            balance_before = user.balance_stars
            if balance_before < amount:
                raise ValueError("Insufficient balance")
            balance_after = balance_before - amount
            self.user_repo.update_balance(user_id, amount_stars=-amount)
        else:
            raise ValueError(f"Invalid currency: {currency}")
        
        # Create transaction
        self.transaction_repo.create(
            user_id=user_id,
            transaction_type=TransactionType.BET,
            currency=currency,
            amount=-amount,
            balance_before=balance_before,
            balance_after=balance_after,
            description=description or f"Bet: {amount} {currency}",
            bet_id=bet_id,
            round_id=round_id,
        )
        
        return balance_after
    
    def add_balance(self, user_id: int, amount: Decimal, currency: str,
                   description: Optional[str] = None,
                   bet_id: Optional[int] = None,
                   round_id: Optional[int] = None,
                   transaction_type: TransactionType = TransactionType.WIN) -> Decimal:
        """
        Add balance (for wins, deposits).
        
        Args:
            user_id: User ID
            amount: Amount to add
            currency: Currency
            description: Transaction description
            bet_id: Optional bet ID
            round_id: Optional round ID
            transaction_type: Transaction type
        
        Returns:
            New balance
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        # Get current balance
        if currency == "TON":
            balance_before = user.balance_ton
            balance_after = balance_before + amount
            self.user_repo.update_balance(user_id, amount_ton=amount)
        elif currency == "STARS":
            balance_before = user.balance_stars
            balance_after = balance_before + amount
            self.user_repo.update_balance(user_id, amount_stars=amount)
        else:
            raise ValueError(f"Invalid currency: {currency}")
        
        # Create transaction
        self.transaction_repo.create(
            user_id=user_id,
            transaction_type=transaction_type,
            currency=currency,
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_after,
            description=description or f"{transaction_type.value}: {amount} {currency}",
            bet_id=bet_id,
            round_id=round_id,
        )
        
        return balance_after
    
    def has_sufficient_balance(self, user_id: int, amount: Decimal, currency: str) -> bool:
        """
        Check if user has sufficient balance.
        
        Args:
            user_id: User ID
            amount: Required amount
            currency: Currency
        
        Returns:
            True if sufficient balance
        """
        try:
            balance = self.get_balance(user_id, currency)
            return balance >= amount
        except ValueError:
            return False
