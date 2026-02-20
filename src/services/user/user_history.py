"""User history service."""
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from src.database.repositories.user_repo import UserRepository
from src.database.repositories.transaction_repo import TransactionRepository
from src.database.repositories.game_repo import BetRepository
from src.database.repositories.payment_repo import PaymentRepository


class UserHistoryService:
    """User history service."""
    
    def __init__(self, db: Session):
        """
        Initialize user history service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.transaction_repo = TransactionRepository(db)
        self.bet_repo = BetRepository(db)
        self.payment_repo = PaymentRepository(db)
    
    def get_transaction_history(
        self,
        user_id: int,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get user transaction history.
        
        Args:
            user_id: User ID
            limit: Maximum number of records
        
        Returns:
            List of transactions
        """
        transactions = self.transaction_repo.get_user_transactions(user_id, limit=limit)
        
        return [
            {
                "id": t.id,
                "type": t.transaction_type.value if t.transaction_type else None,
                "amount": float(t.amount),
                "currency": t.currency,
                "balance_before": float(t.balance_before),
                "balance_after": float(t.balance_after),
                "description": t.description,
                "created_at": t.created_at.isoformat() if t.created_at else None,
            }
            for t in transactions
        ]
    
    def get_bet_history(
        self,
        user_id: int,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get user bet history.
        
        Args:
            user_id: User ID
            limit: Maximum number of records
        
        Returns:
            List of bets
        """
        bets = self.bet_repo.get_user_bets(user_id, limit=limit)
        
        return [
            {
                "id": bet.id,
                "round_id": bet.round_id,
                "amount_ton": float(bet.amount_ton or 0),
                "amount_stars": float(bet.amount_stars or 0),
                "currency": bet.currency,
                "status": bet.status.value if bet.status else None,
                "cashed_out_multiplier": (
                    float(bet.cashed_out_multiplier)
                    if bet.cashed_out_multiplier
                    else None
                ),
                "payout_ton": float(bet.payout_ton or 0),
                "payout_stars": float(bet.payout_stars or 0),
                "placed_at": bet.placed_at.isoformat() if bet.placed_at else None,
            }
            for bet in bets
        ]
    
    def get_payment_history(
        self,
        user_id: int,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get user payment history.
        
        Args:
            user_id: User ID
            limit: Maximum number of records
        
        Returns:
            List of payments
        """
        payments = self.payment_repo.get_user_payments(user_id, limit=limit)
        
        return [
            {
                "id": p.id,
                "type": p.payment_type.value if p.payment_type else None,
                "method": p.payment_method.value if p.payment_method else None,
                "amount": float(p.amount),
                "currency": p.currency,
                "fee_amount": float(p.fee_amount or 0),
                "net_amount": float(p.net_amount or 0),
                "status": p.status.value if p.status else None,
                "created_at": p.created_at.isoformat() if p.created_at else None,
            }
            for p in payments
        ]
