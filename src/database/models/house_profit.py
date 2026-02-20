"""House profit model."""
from sqlalchemy import Column, Integer, Numeric, DateTime
from sqlalchemy.sql import func
from datetime import datetime
from decimal import Decimal

from src.database.connection import Base


class HouseProfit(Base):
    """House profit tracking model."""
    __tablename__ = "house_profit"
    
    id = Column(Integer, primary_key=True, index=True)
    round_id = Column(Integer, nullable=True, index=True)
    profit_ton = Column(Numeric(20, 9), default=Decimal("0.0"))
    profit_stars = Column(Numeric(20, 2), default=Decimal("0.0"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
