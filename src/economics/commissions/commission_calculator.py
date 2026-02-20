"""Commission calculator wrapper."""
from decimal import Decimal
from sqlalchemy.orm import Session

from src.economics.core.commission_calculator import CommissionCalculator as CoreCalculator


class CommissionCalculator:
    """Wrapper for commission calculations."""
    
    def __init__(self, db: Session):
        """
        Initialize commission calculator.
        
        Args:
            db: Database session
        """
        self.db = db
        self.core = CoreCalculator()
    
    def calculate_withdrawal_commission(
        self,
        amount: Decimal,
        currency: str
    ) -> Decimal:
        """
        Calculate withdrawal commission.
        
        Args:
            amount: Withdrawal amount
            currency: Currency
        
        Returns:
            Commission amount
        """
        return self.core.calculate_withdrawal_commission(amount, currency)
    
    def calculate_deposit_commission(
        self,
        amount: Decimal,
        currency: str
    ) -> Decimal:
        """
        Calculate deposit commission.
        
        Args:
            amount: Deposit amount
            currency: Currency
        
        Returns:
            Commission amount
        """
        return self.core.calculate_deposit_commission(amount, currency)
    
    def get_commission_rate(self, payment_type: str) -> Decimal:
        """
        Get commission rate for payment type.
        
        Args:
            payment_type: "deposit" or "withdrawal"
        
        Returns:
            Commission rate
        """
        if payment_type == "withdrawal":
            return self.core.withdrawal_commission_percent
        elif payment_type == "deposit":
            return self.core.deposit_commission_percent
        return Decimal("0.0")
