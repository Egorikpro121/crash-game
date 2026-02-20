"""User analytics service."""
from decimal import Decimal
from typing import Dict, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.database.repositories.user_repo import UserRepository
from src.database.repositories.transaction_repo import TransactionRepository
from src.economics.analytics.user_lifetime_value import UserLifetimeValue


class UserAnalyticsService:
    """User analytics service."""
    
    def __init__(self, db: Session):
        """
        Initialize user analytics service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.transaction_repo = TransactionRepository(db)
        self.ltv_calculator = UserLifetimeValue(db)
    
    def get_user_activity(
        self,
        user_id: int,
        days: int = 30
    ) -> Dict:
        """
        Get user activity for period.
        
        Args:
            user_id: User ID
            days: Number of days
        
        Returns:
            Activity breakdown
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        transactions = self.transaction_repo.get_user_transactions(user_id)
        period_transactions = [
            t for t in transactions
            if t.created_at and t.created_at >= start_date
        ]
        
        return {
            "user_id": user_id,
            "period_days": days,
            "transactions_count": len(period_transactions),
            "transactions": [
                {
                    "id": t.id,
                    "type": t.transaction_type.value if t.transaction_type else None,
                    "amount": float(t.amount),
                    "currency": t.currency,
                    "created_at": t.created_at.isoformat() if t.created_at else None,
                }
                for t in period_transactions
            ],
        }
    
    def get_user_ltv(self, user_id: int) -> Dict:
        """
        Get user lifetime value.
        
        Args:
            user_id: User ID
        
        Returns:
            LTV breakdown
        """
        return self.ltv_calculator.calculate_user_ltv(user_id)
    
    def get_user_retention(
        self,
        user_id: int
    ) -> Dict:
        """
        Get user retention metrics.
        
        Args:
            user_id: User ID
        
        Returns:
            Retention metrics
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return {}
        
        days_since_registration = (
            (datetime.utcnow() - user.created_at).days
            if user.created_at
            else 0
        )
        
        days_since_last_login = (
            (datetime.utcnow() - user.last_login_at).days
            if user.last_login_at
            else None
        )
        
        return {
            "user_id": user_id,
            "days_since_registration": days_since_registration,
            "days_since_last_login": days_since_last_login,
            "is_active": user.is_active,
        }
