"""Referral models."""
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal

from src.database.connection import Base


class Referral(Base):
    """Referral model."""
    __tablename__ = "referrals"
    
    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    referred_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    total_earnings_ton = Column(Numeric(20, 9), default=Decimal("0.0"))
    total_earnings_stars = Column(Numeric(20, 2), default=Decimal("0.0"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    referrer = relationship("User", foreign_keys=[referrer_id])
    referred = relationship("User", foreign_keys=[referred_id])
