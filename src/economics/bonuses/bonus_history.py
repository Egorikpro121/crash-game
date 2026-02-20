"""Bonus history tracking."""
from decimal import Decimal
from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy.orm import Session

from src.database.repositories.transaction_repo import TransactionRepository, TransactionType


class BonusHistory:
    """Track bonus history."""
    
    def __init__(self, db: Session):
        """
        Initialize bonus history tracker.
        
        Args:
            db: Database session
        """
        self.db = db
        self.transaction_repo = TransactionRepository(db)
    
    def get_user_bonus_history(
        self,
        user_id: int,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get user's bonus history.
        
        Args:
            user_id: User ID
            limit: Maximum number of records
        
        Returns:
            List of bonus records
        """
        transactions = self.transaction_repo.get_user_transactions(
            user_id, TransactionType.BONUS
        )
        
        bonuses = []
        for transaction in transactions[:limit]:
            bonus_type = self._extract_bonus_type(transaction.description or "")
            
            bonuses.append({
                "id": transaction.id,
                "type": bonus_type,
                "amount": transaction.amount,
                "currency": transaction.currency,
                "description": transaction.description,
                "created_at": transaction.created_at.isoformat() if transaction.created_at else None,
            })
        
        return bonuses
    
    def get_bonus_statistics(self, user_id: int) -> Dict:
        """
        Get bonus statistics for user.
        
        Args:
            user_id: User ID
        
        Returns:
            Bonus statistics
        """
        transactions = self.transaction_repo.get_user_transactions(
            user_id, TransactionType.BONUS
        )
        
        total_ton = Decimal("0.0")
        total_stars = Decimal("0.0")
        by_type = {}
        
        for transaction in transactions:
            bonus_type = self._extract_bonus_type(transaction.description or "")
            
            if transaction.currency == "TON":
                total_ton += transaction.amount
            else:
                total_stars += transaction.amount
            
            if bonus_type not in by_type:
                by_type[bonus_type] = {
                    "count": 0,
                    "total_ton": Decimal("0.0"),
                    "total_stars": Decimal("0.0"),
                }
            
            by_type[bonus_type]["count"] += 1
            if transaction.currency == "TON":
                by_type[bonus_type]["total_ton"] += transaction.amount
            else:
                by_type[bonus_type]["total_stars"] += transaction.amount
        
        return {
            "total_bonuses_ton": total_ton,
            "total_bonuses_stars": total_stars,
            "total_count": len(transactions),
            "by_type": by_type,
        }
    
    def _extract_bonus_type(self, description: str) -> str:
        """Extract bonus type from description."""
        description_lower = description.lower()
        
        if "first deposit" in description_lower:
            return "first_deposit"
        elif "daily" in description_lower:
            return "daily"
        elif "activity" in description_lower:
            return "activity"
        elif "streak" in description_lower:
            return "streak"
        elif "vip" in description_lower:
            return "vip"
        
        return "unknown"
