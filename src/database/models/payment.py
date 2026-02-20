"""Payment models for deposits and withdrawals."""
from sqlalchemy import Column, Integer, BigInteger, String, Numeric, DateTime, Boolean, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal
import enum

from src.database.connection import Base


class PaymentType(str, enum.Enum):
    """Type of payment."""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


class PaymentStatus(str, enum.Enum):
    """Status of payment."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PaymentMethod(str, enum.Enum):
    """Payment method."""
    TON = "TON"
    STARS = "STARS"


class Payment(Base):
    """Payment model for deposits and withdrawals."""
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Payment details
    payment_type = Column(SQLEnum(PaymentType), nullable=False, index=True)
    payment_method = Column(SQLEnum(PaymentMethod), nullable=False)
    amount = Column(Numeric(20, 9), nullable=False)
    currency = Column(String(10), nullable=False)  # "TON" or "STARS"
    
    # Fees
    fee_amount = Column(Numeric(20, 9), default=Decimal("0.0"), nullable=False)
    net_amount = Column(Numeric(20, 9), nullable=False)  # amount - fee
    
    # Status
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False, index=True)
    
    # External references
    external_tx_hash = Column(String(128), nullable=True, index=True)  # TON transaction hash or Stars payment ID
    external_address = Column(String(128), nullable=True)  # TON address or Stars invoice ID
    
    # TON specific
    ton_address = Column(String(128), nullable=True)  # Deposit/withdrawal address
    ton_tx_hash = Column(String(128), nullable=True, index=True)
    ton_block_number = Column(BigInteger, nullable=True)
    
    # Stars specific
    stars_invoice_id = Column(String(128), nullable=True, index=True)
    stars_payment_id = Column(String(128), nullable=True, index=True)
    
    # Error handling
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    failed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="payments")
    transaction = relationship("Transaction", back_populates="payment", uselist=False)
    
    def __repr__(self):
        return f"<Payment(id={self.id}, user_id={self.user_id}, type={self.payment_type}, status={self.status})>"
    
    def to_dict(self):
        """Convert payment to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "payment_type": self.payment_type.value,
            "payment_method": self.payment_method.value,
            "amount": float(self.amount),
            "currency": self.currency,
            "fee_amount": float(self.fee_amount),
            "net_amount": float(self.net_amount),
            "status": self.status.value,
            "external_tx_hash": self.external_tx_hash,
            "external_address": self.external_address,
            "ton_address": self.ton_address,
            "ton_tx_hash": self.ton_tx_hash,
            "stars_invoice_id": self.stars_invoice_id,
            "stars_payment_id": self.stars_payment_id,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
