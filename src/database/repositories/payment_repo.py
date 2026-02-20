"""Payment repository for database operations."""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

from src.database.models.payment import Payment, PaymentType, PaymentStatus, PaymentMethod


class PaymentRepository:
    """Repository for payment operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, payment_id: int) -> Optional[Payment]:
        """Get payment by ID."""
        return self.db.query(Payment).filter(Payment.id == payment_id).first()
    
    def get_by_external_tx_hash(self, tx_hash: str) -> Optional[Payment]:
        """Get payment by external transaction hash."""
        return self.db.query(Payment).filter(Payment.external_tx_hash == tx_hash).first()
    
    def get_by_stars_payment_id(self, payment_id: str) -> Optional[Payment]:
        """Get payment by Stars payment ID."""
        return self.db.query(Payment).filter(Payment.stars_payment_id == payment_id).first()
    
    def get_user_payments(self, user_id: int, payment_type: Optional[PaymentType] = None,
                         limit: int = 100) -> List[Payment]:
        """Get user's payments."""
        query = self.db.query(Payment).filter(Payment.user_id == user_id)
        
        if payment_type:
            query = query.filter(Payment.payment_type == payment_type)
        
        return query.order_by(desc(Payment.created_at)).limit(limit).all()
    
    def get_pending_payments(self, payment_method: Optional[PaymentMethod] = None) -> List[Payment]:
        """Get pending payments."""
        query = self.db.query(Payment).filter(Payment.status == PaymentStatus.PENDING)
        
        if payment_method:
            query = query.filter(Payment.payment_method == payment_method)
        
        return query.order_by(Payment.created_at).all()
    
    def create_deposit(self, user_id: int, amount: Decimal, currency: str,
                      payment_method: PaymentMethod, ton_address: Optional[str] = None,
                      stars_invoice_id: Optional[str] = None) -> Payment:
        """Create a deposit payment."""
        payment = Payment(
            user_id=user_id,
            payment_type=PaymentType.DEPOSIT,
            payment_method=payment_method,
            amount=amount,
            currency=currency,
            fee_amount=Decimal("0.0"),  # No fee for deposits
            net_amount=amount,
            status=PaymentStatus.PENDING,
            ton_address=ton_address,
            stars_invoice_id=stars_invoice_id,
        )
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment
    
    def create_withdrawal(self, user_id: int, amount: Decimal, currency: str,
                         payment_method: PaymentMethod, fee_amount: Decimal,
                         ton_address: Optional[str] = None) -> Payment:
        """Create a withdrawal payment."""
        payment = Payment(
            user_id=user_id,
            payment_type=PaymentType.WITHDRAWAL,
            payment_method=payment_method,
            amount=amount,
            currency=currency,
            fee_amount=fee_amount,
            net_amount=amount - fee_amount,
            status=PaymentStatus.PENDING,
            ton_address=ton_address,
        )
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment
    
    def update_status(self, payment_id: int, status: PaymentStatus,
                     external_tx_hash: Optional[str] = None,
                     error_message: Optional[str] = None) -> Payment:
        """Update payment status."""
        payment = self.get_by_id(payment_id)
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")
        
        payment.status = status
        
        if external_tx_hash:
            payment.external_tx_hash = external_tx_hash
            if payment.payment_method == PaymentMethod.TON:
                payment.ton_tx_hash = external_tx_hash
        
        if error_message:
            payment.error_message = error_message
            payment.retry_count += 1
        
        if status == PaymentStatus.PROCESSING:
            payment.processed_at = datetime.utcnow()
        elif status == PaymentStatus.COMPLETED:
            payment.completed_at = datetime.utcnow()
        elif status == PaymentStatus.FAILED:
            payment.failed_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(payment)
        return payment
