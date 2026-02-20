"""Deposit commission system."""
from decimal import Decimal
from sqlalchemy.orm import Session

from src.economics.core.commission_calculator import CommissionCalculator


class DepositCommission:
    """Handle deposit commissions (usually 0%)."""
    
    def __init__(self, db: Session):
        """
        Initialize deposit commission handler.
        
        Args:
            db: Database session
        """
        self.db = db
        self.calculator = CommissionCalculator()
    
    def calculate_commission(
        self,
        deposit_amount: Decimal,
        currency: str
    ) -> Decimal:
        """
        Calculate deposit commission (usually 0).
        
        Args:
            deposit_amount: Deposit amount
            currency: Currency
        
        Returns:
            Commission amount (usually 0)
        """
        return self.calculator.calculate_deposit_commission(
            deposit_amount, currency
        )
    
    def calculate_net_amount(
        self,
        deposit_amount: Decimal,
        currency: str
    ) -> Decimal:
        """
        Calculate net deposit amount (same as gross, no commission).
        
        Args:
            deposit_amount: Deposit amount
            currency: Currency
        
        Returns:
            Net amount (same as deposit_amount)
        """
        commission = self.calculate_commission(deposit_amount, currency)
        return deposit_amount - commission
