"""Transaction repository for database operations."""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
import json

from src.database.models.transaction import Transaction, TransactionType


class TransactionRepository:
    """Repository for transaction operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """Get transaction by ID."""
        return self.db.query(Transaction).filter(Transaction.id == transaction_id).first()
    
    def get_user_transactions(self, user_id: int, transaction_type: Optional[TransactionType] = None,
                            currency: Optional[str] = None, limit: int = 100) -> List[Transaction]:
        """Get user's transactions."""
        query = self.db.query(Transaction).filter(Transaction.user_id == user_id)
        
        if transaction_type:
            query = query.filter(Transaction.transaction_type == transaction_type)
        
        if currency:
            query = query.filter(Transaction.currency == currency)
        
        return query.order_by(desc(Transaction.created_at)).limit(limit).all()
    
    def create(self, user_id: int, transaction_type: TransactionType, currency: str,
              amount: Decimal, balance_before: Decimal, balance_after: Decimal,
              description: Optional[str] = None, payment_id: Optional[int] = None,
              bet_id: Optional[int] = None, round_id: Optional[int] = None,
              metadata: Optional[dict] = None) -> Transaction:
        """Create a new transaction."""
        transaction = Transaction(
            user_id=user_id,
            payment_id=payment_id,
            bet_id=bet_id,
            round_id=round_id,
            transaction_type=transaction_type,
            currency=currency,
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_after,
            description=description,
            metadata_json=json.dumps(metadata) if metadata else None,
        )
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction
    
    def get_user_balance_history(self, user_id: int, currency: str,
                                start_date: Optional[datetime] = None,
                                end_date: Optional[datetime] = None) -> List[Transaction]:
        """Get user's balance history."""
        query = self.db.query(Transaction).filter(
            and_(
                Transaction.user_id == user_id,
                Transaction.currency == currency
            )
        )
        
        if start_date:
            query = query.filter(Transaction.created_at >= start_date)
        if end_date:
            query = query.filter(Transaction.created_at <= end_date)
        
        return query.order_by(Transaction.created_at).all()
