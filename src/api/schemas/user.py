"""User Pydantic schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""
    telegram_user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema."""
    referral_code: Optional[str] = None


class UserResponse(UserBase):
    """User response schema."""
    id: int
    balance_ton: Decimal
    balance_stars: Decimal
    total_deposited_ton: Decimal
    total_deposited_stars: Decimal
    total_won_ton: Decimal
    total_won_stars: Decimal
    total_bets: int
    total_cashouts: int
    biggest_multiplier: Decimal
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserBalance(BaseModel):
    """User balance schema."""
    balance_ton: Decimal
    balance_stars: Decimal


class UserStatistics(BaseModel):
    """User statistics schema."""
    total_bets: int
    total_cashouts: int
    total_won_ton: Decimal
    total_won_stars: Decimal
    total_lost_ton: Decimal
    total_lost_stars: Decimal
    biggest_win_ton: Decimal
    biggest_win_stars: Decimal
    biggest_multiplier: Decimal
    win_rate: Decimal
