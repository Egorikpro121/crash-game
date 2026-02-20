"""Commission tracking system."""
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, Optional
from sqlalchemy.orm import Session

from src.database.repositories.payment_repo import PaymentRepository, PaymentType


class CommissionTracker:
    """Track commission revenue."""
    
    def __init__(self, db: Session):
        """
        Initialize commission tracker.
        
        Args:
            db: Database session
        """
        self.db = db
        self.payment_repo = PaymentRepository(db)
    
    def get_daily_commissions(
        self,
        date: Optional[datetime] = None
    ) -> Dict[str, Decimal]:
        """
        Get commissions for a specific day.
        
        Args:
            date: Date to check (defaults to today)
        
        Returns:
            Daily commissions breakdown
        """
        if date is None:
            date = datetime.utcnow()
        
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        
        payments = self.payment_repo.get_pending_payments()
        daily_payments = [
            p for p in payments
            if p.created_at and start_date <= p.created_at < end_date
        ]
        
        withdrawal_commissions_ton = Decimal("0.0")
        withdrawal_commissions_stars = Decimal("0.0")
        
        for payment in daily_payments:
            if payment.payment_type == PaymentType.WITHDRAWAL:
                if payment.currency == "TON":
                    withdrawal_commissions_ton += payment.fee_amount or Decimal("0.0")
                else:
                    withdrawal_commissions_stars += payment.fee_amount or Decimal("0.0")
        
        return {
            "date": date.date().isoformat(),
            "withdrawal_commissions_ton": withdrawal_commissions_ton,
            "withdrawal_commissions_stars": withdrawal_commissions_stars,
            "total_commissions": withdrawal_commissions_ton + withdrawal_commissions_stars,
        }
    
    def get_total_commissions(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Decimal]:
        """
        Get total commissions in period.
        
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
        
        withdrawal_commissions_ton = Decimal("0.0")
        withdrawal_commissions_stars = Decimal("0.0")
        
        for payment in payments:
            if payment.payment_type == PaymentType.WITHDRAWAL:
                if payment.currency == "TON":
                    withdrawal_commissions_ton += payment.fee_amount or Decimal("0.0")
                else:
                    withdrawal_commissions_stars += payment.fee_amount or Decimal("0.0")
        
        return {
            "withdrawal_commissions_ton": withdrawal_commissions_ton,
            "withdrawal_commissions_stars": withdrawal_commissions_stars,
            "total_commissions": withdrawal_commissions_ton + withdrawal_commissions_stars,
            "payments_count": len(payments),
        }
