"""Bonus models."""
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, Text, Enum
from sqlalchemy.sql import func
from datetime import datetime
from decimal import Decimal
import enum

from src.database.connection import Base


class BonusType(enum.Enum):
    """Bonus type enum."""
    FIRST_DEPOSIT = "first_deposit"
    DAILY = "daily"
    ACTIVITY = "activity"
    STREAK = "streak"
    VIP = "vip"


class Bonus(Base):
    """Bonus model."""
    __tablename__ = "bonuses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    bonus_type = Column(Enum(BonusType), nullable=False)
    amount_ton = Column(Numeric(20, 9), default=Decimal("0.0"))
    amount_stars = Column(Numeric(20, 2), default=Decimal("0.0"))
    currency = Column(String(10), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_claimed = Column(Boolean, default=False, nullable=False)
