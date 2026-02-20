"""Transaction model for tracking all balance changes."""
from sqlalchemy import Column, Integer, BigInteger, String, Numeric, DateTime, Boolean, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal
import enum

from src.database.connection import Base


class TransactionType(str, enum.Enum):
    """Type of transaction."""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    BET = "bet"
    WIN = "win"
    LOSS = "loss"
    REFUND = "refund"
    BONUS = "bonus"
    REFERRAL = "referral"
    FEE = "fee"


class Transaction(Base):
    """Transaction model for tracking all balance changes."""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=True, index=True)
    bet_id = Column(Integer, ForeignKey("bets.id"), nullable=True, index=True)
    round_id = Column(Integer, ForeignKey("game_rounds.id"), nullable=True, index=True)
    
    # Transaction details
    transaction_type = Column(SQLEnum(TransactionType), nullable=False, index=True)
    currency = Column(String(10), nullable=False)  # "TON" or "STARS"
    amount = Column(Numeric(20, 9), nullable=False)  # Positive for credits, negative for debits
    balance_before = Column(Numeric(20, 9), nullable=False)
    balance_after = Column(Numeric(20, 9), nullable=False)
    
    # Description
    description = Column(Text, nullable=True)
    metadata_json = Column(Text, nullable=True)  # JSON string with additional data
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    payment = relationship("Payment", back_populates="transaction")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, user_id={self.user_id}, type={self.transaction_type}, amount={self.amount})>"
    
    def to_dict(self):
        """Convert transaction to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "payment_id": self.payment_id,
            "bet_id": self.bet_id,
            "round_id": self.round_id,
            "transaction_type": self.transaction_type.value,
            "currency": self.currency,
            "amount": float(self.amount),
            "balance_before": float(self.balance_before),
            "balance_after": float(self.balance_after),
            "description": self.description,
            "metadata_json": self.metadata_json,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
