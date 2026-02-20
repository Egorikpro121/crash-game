"""Game service - main game operations."""
from typing import Optional, Dict
from sqlalchemy.orm import Session

from src.database.repositories.game_repo import GameRoundRepository, BetRepository
from src.game.engine.game_session import GameSession


class GameService:
    """Main game service."""
    
    def __init__(self, db: Session):
        """
        Initialize game service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.round_repo = GameRoundRepository(db)
        self.bet_repo = BetRepository(db)
        self.game_session = GameSession(db)
    
    def get_active_round(self) -> Optional[Dict]:
        """
        Get currently active round.
        
        Returns:
            Active round data or None
        """
        round_obj = self.round_repo.get_active_round()
        if not round_obj:
            return None
        
        return {
            "id": round_obj.id,
            "status": round_obj.status.value if round_obj.status else None,
            "started_at": round_obj.started_at.isoformat() if round_obj.started_at else None,
        }
    
    def get_round_status(self, round_id: int) -> Optional[Dict]:
        """
        Get round status.
        
        Args:
            round_id: Round ID
        
        Returns:
            Round status data
        """
        round_obj = self.round_repo.get_by_id(round_id)
        if not round_obj:
            return None
        
        return {
            "id": round_obj.id,
            "status": round_obj.status.value if round_obj.status else None,
            "crash_multiplier": (
                float(round_obj.crash_multiplier)
                if round_obj.crash_multiplier
                else None
            ),
            "started_at": round_obj.started_at.isoformat() if round_obj.started_at else None,
            "crashed_at": round_obj.crashed_at.isoformat() if round_obj.crashed_at else None,
        }
