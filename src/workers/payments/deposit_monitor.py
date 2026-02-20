"""Deposit monitor worker."""
from sqlalchemy.orm import Session
from src.database.repositories.payment_repo import PaymentRepository, PaymentStatus


class DepositMonitor:
    """Monitor deposits."""
    
    def __init__(self, db: Session):
        """Initialize deposit monitor."""
        self.db = db
        self.payment_repo = PaymentRepository(db)
    
    def check_pending_deposits(self):
        """Check and process pending deposits."""
        pending = self.payment_repo.get_pending_payments()
        # TODO: Implement deposit processing
        pass
