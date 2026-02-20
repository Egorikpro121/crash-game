"""Round manager worker."""
from sqlalchemy.orm import Session
from src.database.repositories.game_repo import GameRoundRepository


class RoundManager:
    """Manage game rounds."""
    
    def __init__(self, db: Session):
        """Initialize round manager."""
        self.db = db
        self.round_repo = GameRoundRepository(db)
    
    def process_rounds(self):
        """Process active rounds."""
        # TODO: Implement round processing
        pass
