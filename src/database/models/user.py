"""User model for crash game."""
from sqlalchemy import Column, Integer, BigInteger, String, Numeric, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal

from src.database.connection import Base


class User(Base):
    """User model representing a Telegram user."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_user_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String(255), nullable=True, index=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    
    # Balances (stored as Decimal for precision)
    balance_ton = Column(Numeric(20, 9), default=Decimal("0.0"), nullable=False)
    balance_stars = Column(Numeric(20, 2), default=Decimal("0.0"), nullable=False)
    
    # Statistics
    total_deposited_ton = Column(Numeric(20, 9), default=Decimal("0.0"), nullable=False)
    total_deposited_stars = Column(Numeric(20, 2), default=Decimal("0.0"), nullable=False)
    total_withdrawn_ton = Column(Numeric(20, 9), default=Decimal("0.0"), nullable=False)
    total_withdrawn_stars = Column(Numeric(20, 2), default=Decimal("0.0"), nullable=False)
    total_won_ton = Column(Numeric(20, 9), default=Decimal("0.0"), nullable=False)
    total_won_stars = Column(Numeric(20, 2), default=Decimal("0.0"), nullable=False)
    total_lost_ton = Column(Numeric(20, 9), default=Decimal("0.0"), nullable=False)
    total_lost_stars = Column(Numeric(20, 2), default=Decimal("0.0"), nullable=False)
    
    # Game statistics
    total_bets = Column(Integer, default=0, nullable=False)
    total_cashouts = Column(Integer, default=0, nullable=False)
    biggest_win_ton = Column(Numeric(20, 9), default=Decimal("0.0"), nullable=False)
    biggest_win_stars = Column(Numeric(20, 2), default=Decimal("0.0"), nullable=False)
    biggest_multiplier = Column(Numeric(10, 2), default=Decimal("0.0"), nullable=False)
    
    # Settings
    auto_cashout_enabled = Column(Boolean, default=False, nullable=False)
    default_auto_cashout_multiplier = Column(Numeric(5, 2), nullable=True)
    sound_enabled = Column(Boolean, default=True, nullable=False)
    notifications_enabled = Column(Boolean, default=True, nullable=False)
    
    # Referral system
    referral_code = Column(String(32), unique=True, nullable=True, index=True)
    referred_by_id = Column(Integer, nullable=True, index=True)
    referral_earnings_ton = Column(Numeric(20, 9), default=Decimal("0.0"), nullable=False)
    referral_earnings_stars = Column(Numeric(20, 2), default=Decimal("0.0"), nullable=False)
    
    # Security
    is_active = Column(Boolean, default=True, nullable=False)
    is_banned = Column(Boolean, default=False, nullable=False)
    ban_reason = Column(Text, nullable=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    bets = relationship("Bet", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, telegram_user_id={self.telegram_user_id}, username={self.username})>"
    
    def to_dict(self):
        """Convert user to dictionary."""
        return {
            "id": self.id,
            "telegram_user_id": self.telegram_user_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "balance_ton": float(self.balance_ton),
            "balance_stars": float(self.balance_stars),
            "total_deposited_ton": float(self.total_deposited_ton),
            "total_deposited_stars": float(self.total_deposited_stars),
            "total_withdrawn_ton": float(self.total_withdrawn_ton),
            "total_withdrawn_stars": float(self.total_withdrawn_stars),
            "total_won_ton": float(self.total_won_ton),
            "total_won_stars": float(self.total_won_stars),
            "total_lost_ton": float(self.total_lost_ton),
            "total_lost_stars": float(self.total_lost_stars),
            "total_bets": self.total_bets,
            "total_cashouts": self.total_cashouts,
            "biggest_win_ton": float(self.biggest_win_ton),
            "biggest_win_stars": float(self.biggest_win_stars),
            "biggest_multiplier": float(self.biggest_multiplier),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
