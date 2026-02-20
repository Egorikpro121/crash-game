"""Game models for crash game."""
from sqlalchemy import Column, Integer, BigInteger, String, Numeric, DateTime, Boolean, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal
import enum

from src.database.connection import Base


class GameRoundStatus(str, enum.Enum):
    """Status of a game round."""
    PENDING = "pending"  # Round created but not started
    ACTIVE = "active"    # Round is currently running
    CRASHED = "crashed"  # Round has crashed
    CANCELLED = "cancelled"  # Round was cancelled


class BetStatus(str, enum.Enum):
    """Status of a bet."""
    PENDING = "pending"      # Bet placed, waiting for round to start
    ACTIVE = "active"        # Bet is active in round
    CASHED_OUT = "cashed_out"  # Bet was cashed out
    CRASHED = "crashed"      # Round crashed before cashout
    CANCELLED = "cancelled"  # Bet was cancelled


class GameRound(Base):
    """Game round model representing a single crash game round."""
    __tablename__ = "game_rounds"

    id = Column(Integer, primary_key=True, index=True)
    
    # Provably Fair
    server_seed_hash = Column(String(64), nullable=False, index=True)  # Hash of server_seed before round
    server_seed = Column(String(64), nullable=True)  # Revealed after round ends
    client_seed = Column(String(64), nullable=True)  # Optional client seed
    combined_seed = Column(String(64), nullable=True)  # hash(server_seed + client_seed + round_id)
    
    # Game data
    crash_multiplier = Column(Numeric(10, 2), nullable=True)  # Final crash multiplier
    duration_ms = Column(Integer, nullable=True)  # Duration of round in milliseconds
    
    # Status
    status = Column(SQLEnum(GameRoundStatus), default=GameRoundStatus.PENDING, nullable=False, index=True)
    
    # Timestamps
    started_at = Column(DateTime(timezone=True), nullable=True)
    crashed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Statistics
    total_bets = Column(Integer, default=0, nullable=False)
    total_bet_amount_ton = Column(Numeric(20, 9), default=Decimal("0.0"), nullable=False)
    total_bet_amount_stars = Column(Numeric(20, 2), default=Decimal("0.0"), nullable=False)
    total_payout_ton = Column(Numeric(20, 9), default=Decimal("0.0"), nullable=False)
    total_payout_stars = Column(Numeric(20, 2), default=Decimal("0.0"), nullable=False)
    
    # Relationships
    bets = relationship("Bet", back_populates="round", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<GameRound(id={self.id}, status={self.status}, crash_multiplier={self.crash_multiplier})>"
    
    def to_dict(self):
        """Convert round to dictionary."""
        return {
            "id": self.id,
            "server_seed_hash": self.server_seed_hash,
            "server_seed": self.server_seed,
            "client_seed": self.client_seed,
            "crash_multiplier": float(self.crash_multiplier) if self.crash_multiplier else None,
            "duration_ms": self.duration_ms,
            "status": self.status.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "crashed_at": self.crashed_at.isoformat() if self.crashed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "total_bets": self.total_bets,
            "total_bet_amount_ton": float(self.total_bet_amount_ton),
            "total_bet_amount_stars": float(self.total_bet_amount_stars),
        }


class Bet(Base):
    """Bet model representing a user's bet in a game round."""
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    round_id = Column(Integer, ForeignKey("game_rounds.id"), nullable=False, index=True)
    
    # Bet details
    amount_ton = Column(Numeric(20, 9), nullable=True)
    amount_stars = Column(Numeric(20, 2), nullable=True)
    currency = Column(String(10), nullable=False)  # "TON" or "STARS"
    
    # Auto cashout
    auto_cashout_multiplier = Column(Numeric(5, 2), nullable=True)
    auto_cashout_enabled = Column(Boolean, default=False, nullable=False)
    
    # Cashout details
    cashed_out_multiplier = Column(Numeric(5, 2), nullable=True)
    payout_ton = Column(Numeric(20, 9), nullable=True)
    payout_stars = Column(Numeric(20, 2), nullable=True)
    profit_ton = Column(Numeric(20, 9), nullable=True)
    profit_stars = Column(Numeric(20, 2), nullable=True)
    
    # Status
    status = Column(SQLEnum(BetStatus), default=BetStatus.PENDING, nullable=False, index=True)
    
    # Timestamps
    placed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    cashed_out_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="bets")
    round = relationship("GameRound", back_populates="bets")
    
    def __repr__(self):
        return f"<Bet(id={self.id}, user_id={self.user_id}, round_id={self.round_id}, status={self.status})>"
    
    def to_dict(self):
        """Convert bet to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "round_id": self.round_id,
            "amount_ton": float(self.amount_ton) if self.amount_ton else None,
            "amount_stars": float(self.amount_stars) if self.amount_stars else None,
            "currency": self.currency,
            "auto_cashout_multiplier": float(self.auto_cashout_multiplier) if self.auto_cashout_multiplier else None,
            "auto_cashout_enabled": self.auto_cashout_enabled,
            "cashed_out_multiplier": float(self.cashed_out_multiplier) if self.cashed_out_multiplier else None,
            "payout_ton": float(self.payout_ton) if self.payout_ton else None,
            "payout_stars": float(self.payout_stars) if self.payout_stars else None,
            "profit_ton": float(self.profit_ton) if self.profit_ton else None,
            "profit_stars": float(self.profit_stars) if self.profit_stars else None,
            "status": self.status.value,
            "placed_at": self.placed_at.isoformat() if self.placed_at else None,
            "cashed_out_at": self.cashed_out_at.isoformat() if self.cashed_out_at else None,
        }
