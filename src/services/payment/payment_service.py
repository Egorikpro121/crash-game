"""Payment service - main payment operations."""
from typing import Optional
from sqlalchemy.orm import Session
from src.database.repositories.payment_repo import PaymentRepository

class PaymentService:
    def __init__(self, db: Session):
        self.db = db
        self.payment_repo = PaymentRepository(db)
    
    def get_payment(self, payment_id: int):
        return self.payment_repo.get_by_id(payment_id)
