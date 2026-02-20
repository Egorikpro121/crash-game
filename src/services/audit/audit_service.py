"""Audit service."""
from sqlalchemy.orm import Session

class AuditService:
    def __init__(self, db: Session):
        self.db = db
    
    def log_action(self, user_id: int, action: str, resource: str):
        # TODO: Implement audit logging
        pass
