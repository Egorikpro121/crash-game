"""Game repository for database operations."""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

from src.database.models.game import GameRound, Bet, GameRoundStatus, BetStatus


class GameRoundRepository:
    """Repository for game round operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, round_id: int) -> Optional[GameRound]:
        """Get round by ID."""
        return self.db.query(GameRound).filter(GameRound.id == round_id).first()
    
    def get_active_round(self) -> Optional[GameRound]:
        """Get currently active round."""
        return self.db.query(GameRound).filter(
            GameRound.status == GameRoundStatus.ACTIVE
        ).first()
    
    def get_pending_round(self) -> Optional[GameRound]:
        """Get pending round."""
        return self.db.query(GameRound).filter(
            GameRound.status == GameRoundStatus.PENDING
        ).order_by(desc(GameRound.created_at)).first()
    
    def get_latest_rounds(self, limit: int = 100) -> List[GameRound]:
        """Get latest completed rounds."""
        return self.db.query(GameRound).filter(
            GameRound.status == GameRoundStatus.CRASHED
        ).order_by(desc(GameRound.crashed_at)).limit(limit).all()
    
    def create(self, server_seed_hash: str, client_seed: Optional[str] = None) -> GameRound:
        """Create a new game round."""
        round_obj = GameRound(
            server_seed_hash=server_seed_hash,
            client_seed=client_seed,
            status=GameRoundStatus.PENDING,
        )
        self.db.add(round_obj)
        self.db.commit()
        self.db.refresh(round_obj)
        return round_obj
    
    def start_round(self, round_id: int, combined_seed: str) -> GameRound:
        """Start a round."""
        round_obj = self.get_by_id(round_id)
        if not round_obj:
            raise ValueError(f"Round {round_id} not found")
        
        round_obj.status = GameRoundStatus.ACTIVE
        round_obj.combined_seed = combined_seed
        round_obj.started_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(round_obj)
        return round_obj
    
    def crash_round(self, round_id: int, crash_multiplier: Decimal,
                   server_seed: str, duration_ms: int) -> GameRound:
        """Crash a round."""
        round_obj = self.get_by_id(round_id)
        if not round_obj:
            raise ValueError(f"Round {round_id} not found")
        
        round_obj.status = GameRoundStatus.CRASHED
        round_obj.crash_multiplier = crash_multiplier
        round_obj.server_seed = server_seed
        round_obj.duration_ms = duration_ms
        round_obj.crashed_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(round_obj)
        return round_obj
    
    def update_statistics(self, round_id: int, **kwargs) -> GameRound:
        """Update round statistics."""
        round_obj = self.get_by_id(round_id)
        if not round_obj:
            raise ValueError(f"Round {round_id} not found")
        
        for key, value in kwargs.items():
            if hasattr(round_obj, key):
                setattr(round_obj, key, value)
        
        self.db.commit()
        self.db.refresh(round_obj)
        return round_obj


class BetRepository:
    """Repository for bet operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, bet_id: int) -> Optional[Bet]:
        """Get bet by ID."""
        return self.db.query(Bet).filter(Bet.id == bet_id).first()
    
    def get_by_user_and_round(self, user_id: int, round_id: int) -> Optional[Bet]:
        """Get bet by user and round."""
        return self.db.query(Bet).filter(
            and_(Bet.user_id == user_id, Bet.round_id == round_id)
        ).first()
    
    def get_active_bets_by_round(self, round_id: int) -> List[Bet]:
        """Get all active bets for a round."""
        return self.db.query(Bet).filter(
            and_(
                Bet.round_id == round_id,
                Bet.status == BetStatus.ACTIVE
            )
        ).all()
    
    def get_user_bets(self, user_id: int, limit: int = 100) -> List[Bet]:
        """Get user's bets."""
        return self.db.query(Bet).filter(
            Bet.user_id == user_id
        ).order_by(desc(Bet.placed_at)).limit(limit).all()
    
    def create(self, user_id: int, round_id: int, amount_ton: Optional[Decimal],
              amount_stars: Optional[Decimal], currency: str,
              auto_cashout_multiplier: Optional[Decimal] = None) -> Bet:
        """Create a new bet."""
        bet = Bet(
            user_id=user_id,
            round_id=round_id,
            amount_ton=amount_ton,
            amount_stars=amount_stars,
            currency=currency,
            auto_cashout_multiplier=auto_cashout_multiplier,
            auto_cashout_enabled=auto_cashout_multiplier is not None,
            status=BetStatus.PENDING,
        )
        self.db.add(bet)
        self.db.commit()
        self.db.refresh(bet)
        return bet
    
    def activate_bet(self, bet_id: int) -> Bet:
        """Activate a bet when round starts."""
        bet = self.get_by_id(bet_id)
        if not bet:
            raise ValueError(f"Bet {bet_id} not found")
        
        bet.status = BetStatus.ACTIVE
        self.db.commit()
        self.db.refresh(bet)
        return bet
    
    def cashout_bet(self, bet_id: int, multiplier: Decimal,
                   payout_ton: Optional[Decimal], payout_stars: Optional[Decimal]) -> Bet:
        """Cash out a bet."""
        bet = self.get_by_id(bet_id)
        if not bet:
            raise ValueError(f"Bet {bet_id} not found")
        
        bet.status = BetStatus.CASHED_OUT
        bet.cashed_out_multiplier = multiplier
        bet.payout_ton = payout_ton
        bet.payout_stars = payout_stars
        
        if payout_ton:
            bet.profit_ton = payout_ton - (bet.amount_ton or Decimal("0"))
        if payout_stars:
            bet.profit_stars = payout_stars - (bet.amount_stars or Decimal("0"))
        
        bet.cashed_out_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(bet)
        return bet
    
    def crash_bet(self, bet_id: int) -> Bet:
        """Mark bet as crashed."""
        bet = self.get_by_id(bet_id)
        if not bet:
            raise ValueError(f"Bet {bet_id} not found")
        
        bet.status = BetStatus.CRASHED
        self.db.commit()
        self.db.refresh(bet)
        return bet
