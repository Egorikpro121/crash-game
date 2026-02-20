"""Payment Pydantic schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime


class DepositRequest(BaseModel):
    """Deposit request schema."""
    amount: Decimal = Field(..., gt=0, description="Deposit amount")
    currency: str = Field(..., pattern="^(TON|STARS)$", description="Currency")


class DepositResponse(BaseModel):
    """Deposit response schema."""
    payment_id: int
    address: Optional[str] = None  # TON address or Stars invoice link
    amount: Decimal
    currency: str
    status: str
    created_at: datetime


class WithdrawalRequest(BaseModel):
    """Withdrawal request schema."""
    amount: Decimal = Field(..., gt=0, description="Withdrawal amount")
    currency: str = Field(..., pattern="^(TON|STARS)$", description="Currency")
    address: str = Field(..., min_length=1, description="Withdrawal address")


class WithdrawalResponse(BaseModel):
    """Withdrawal response schema."""
    payment_id: int
    amount: Decimal
    currency: str
    fee_amount: Decimal
    net_amount: Decimal
    address: str
    status: str
    tx_hash: Optional[str] = None
    created_at: datetime


class PaymentHistory(BaseModel):
    """Payment history schema."""
    payment_id: int
    payment_type: str
    payment_method: str
    amount: Decimal
    currency: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
