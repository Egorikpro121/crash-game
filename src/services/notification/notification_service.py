"""Notification service."""
from sqlalchemy.orm import Session

class NotificationService:
    def __init__(self, db: Session):
        self.db = db
    
    def send_notification(self, user_id: int, message: str):
        # TODO: Implement notification sending
        pass
