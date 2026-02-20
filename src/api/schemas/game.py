"""Game Pydantic schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from datetime import datetime


class BetRequest(BaseModel):
    """Bet request schema."""
    amount: Decimal = Field(..., gt=0, description="Bet amount")
    currency: str = Field(..., pattern="^(TON|STARS)$", description="Currency")
    auto_cashout: Optional[Decimal] = Field(None, gt=1.0, description="Auto cashout multiplier")


class BetResponse(BaseModel):
    """Bet response schema."""
    bet_id: int
    round_id: int
    amount: Decimal
    currency: str
    auto_cashout_multiplier: Optional[Decimal]
    status: str
    placed_at: datetime
    
    class Config:
        from_attributes = True


class CashoutRequest(BaseModel):
    """Cashout request schema."""
    pass  # No parameters needed


class CashoutResponse(BaseModel):
    """Cashout response schema."""
    bet_id: int
    multiplier: Decimal
    payout: Decimal
    currency: str
    cashed_out_at: datetime


class RoundStatus(BaseModel):
    """Round status schema."""
    round_id: int
    status: str
    multiplier: Optional[Decimal]
    crash_point: Optional[Decimal]
    start_time: Optional[datetime]
    time_until_crash: Optional[int]  # milliseconds


class RoundHistory(BaseModel):
    """Round history schema."""
    round_id: int
    crash_multiplier: Decimal
    started_at: datetime
    crashed_at: datetime
    total_bets: int


class ActiveBet(BaseModel):
    """Active bet schema."""
    bet_id: int
    user_id: int
    amount: Decimal
    currency: str
    auto_cashout_multiplier: Optional[Decimal]
    placed_at: datetime
