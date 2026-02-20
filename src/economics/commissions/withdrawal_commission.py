"""Withdrawal commission system."""
from decimal import Decimal
from datetime import datetime
from typing import Optional, Dict
from sqlalchemy.orm import Session

from src.economics.core.commission_calculator import CommissionCalculator
from src.database.repositories.payment_repo import PaymentRepository, PaymentType


class WithdrawalCommission:
    """Handle withdrawal commissions."""
    
    def __init__(self, db: Session):
        """
        Initialize withdrawal commission handler.
        
        Args:
            db: Database session
        """
        self.db = db
        self.calculator = CommissionCalculator()
        self.payment_repo = PaymentRepository(db)
    
    def calculate_commission(
        self,
        withdrawal_amount: Decimal,
        currency: str
    ) -> Decimal:
        """
        Calculate withdrawal commission.
        
        Args:
            withdrawal_amount: Withdrawal amount
            currency: Currency
        
        Returns:
            Commission amount
        """
        return self.calculator.calculate_withdrawal_commission(
            withdrawal_amount, currency
        )
    
    def calculate_net_amount(
        self,
        withdrawal_amount: Decimal,
        currency: str
    ) -> Decimal:
        """
        Calculate net withdrawal amount after commission.
        
        Args:
            withdrawal_amount: Gross withdrawal amount
            currency: Currency
        
        Returns:
            Net amount
        """
        return self.calculator.calculate_net_withdrawal_amount(
            withdrawal_amount, currency
        )
    
    def get_total_commissions(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Decimal]:
        """
        Get total withdrawal commissions in period.
        
        Args:
            start_date: Start date
            end_date: End date
        
        Returns:
            Total commissions breakdown
        """
        payments = self.payment_repo.get_pending_payments()
        
        if start_date:
            payments = [p for p in payments if p.created_at >= start_date]
        if end_date:
            payments = [p for p in payments if p.created_at <= end_date]
        
        total_ton = Decimal("0.0")
        total_stars = Decimal("0.0")
        
        for payment in payments:
            if payment.payment_type == PaymentType.WITHDRAWAL:
                if payment.currency == "TON":
                    total_ton += payment.fee_amount or Decimal("0.0")
                else:
                    total_stars += payment.fee_amount or Decimal("0.0")
        
        return {
            "total_ton": total_ton,
            "total_stars": total_stars,
            "total": total_ton + total_stars,
        }
