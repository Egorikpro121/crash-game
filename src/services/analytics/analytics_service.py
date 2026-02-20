"""Analytics service."""
from sqlalchemy.orm import Session

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
