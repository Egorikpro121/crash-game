"""Leaderboard models for rankings."""
from sqlalchemy import Column, Integer, BigInteger, String, Numeric, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal

from src.database.connection import Base


class Leaderboard(Base):
    """Leaderboard model for tracking user rankings."""
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    
    # Rankings
    rank = Column(Integer, nullable=True, index=True)
    
    # Metrics
    total_won_ton = Column(Numeric(20, 9), default=Decimal("0.0"), nullable=False)
    total_won_stars = Column(Numeric(20, 2), default=Decimal("0.0"), nullable=False)
    biggest_win_ton = Column(Numeric(20, 9), default=Decimal("0.0"), nullable=False)
    biggest_win_stars = Column(Numeric(20, 2), default=Decimal("0.0"), nullable=False)
    biggest_multiplier = Column(Numeric(10, 2), default=Decimal("0.0"), nullable=False)
    total_bets = Column(Integer, default=0, nullable=False)
    win_rate = Column(Numeric(5, 2), default=Decimal("0.0"), nullable=False)  # Percentage
    
    # Timestamps
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    
    def __repr__(self):
        return f"<Leaderboard(id={self.id}, user_id={self.user_id}, rank={self.rank})>"
    
    def to_dict(self):
        """Convert leaderboard entry to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "rank": self.rank,
            "total_won_ton": float(self.total_won_ton),
            "total_won_stars": float(self.total_won_stars),
            "biggest_win_ton": float(self.biggest_win_ton),
            "biggest_win_stars": float(self.biggest_win_stars),
            "biggest_multiplier": float(self.biggest_multiplier),
            "total_bets": self.total_bets,
            "win_rate": float(self.win_rate),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
