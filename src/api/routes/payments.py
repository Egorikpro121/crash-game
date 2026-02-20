"""Payment routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.api.middleware.auth import get_current_user
from src.api.schemas.payments import (
    DepositRequest, DepositResponse, WithdrawalRequest,
    WithdrawalResponse, PaymentHistory
)
from src.database.repositories.payment_repo import PaymentRepository, PaymentType, PaymentMethod
from src.payments.ton.transactions import TONTransactionProcessor
from src.payments.stars.integration import StarsIntegration

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/deposit", response_model=DepositResponse)
async def create_deposit(
    deposit_request: DepositRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a deposit.
    
    Args:
        deposit_request: Deposit request data
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Deposit response
    """
    payment_repo = PaymentRepository(db)
    
    if deposit_request.currency == "TON":
        # Create TON deposit
        ton_processor = TONTransactionProcessor(db)
        address = await ton_processor.ton_integration.create_deposit_address(current_user["id"])
        
        payment = payment_repo.create_deposit(
            current_user["id"],
            deposit_request.amount,
            deposit_request.currency,
            PaymentMethod.TON,
            ton_address=address
        )
        
        return DepositResponse(
            payment_id=payment.id,
            address=address,
            amount=payment.amount,
            currency=payment.currency,
            status=payment.status.value,
            created_at=payment.created_at
        )
    
    elif deposit_request.currency == "STARS":
        # Create Stars deposit
        stars_integration = StarsIntegration()
        invoice = await stars_integration.create_invoice(
            current_user["id"],
            deposit_request.amount
        )
        
        payment = payment_repo.create_deposit(
            current_user["id"],
            deposit_request.amount,
            deposit_request.currency,
            PaymentMethod.STARS,
            stars_invoice_id=invoice["invoice_id"]
        )
        
        return DepositResponse(
            payment_id=payment.id,
            address=invoice["invoice_link"],
            amount=payment.amount,
            currency=payment.currency,
            status=payment.status.value,
            created_at=payment.created_at
        )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid currency"
        )


@router.post("/withdraw", response_model=WithdrawalResponse)
async def create_withdrawal(
    withdrawal_request: WithdrawalRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a withdrawal.
    
    Args:
        withdrawal_request: Withdrawal request data
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Withdrawal response
    """
    payment_repo = PaymentRepository(db)
    
    # Calculate fee (0.5-1% with minimum)
    fee_percent = Decimal("0.01")  # 1%
    fee_amount = withdrawal_request.amount * fee_percent
    min_fee = Decimal("0.1") if withdrawal_request.currency == "TON" else Decimal("10")
    fee_amount = max(fee_amount, min_fee)
    
    if withdrawal_request.currency == "TON":
        payment = payment_repo.create_withdrawal(
            current_user["id"],
            withdrawal_request.amount,
            withdrawal_request.currency,
            PaymentMethod.TON,
            fee_amount,
            ton_address=withdrawal_request.address
        )
        
        # Process withdrawal
        ton_processor = TONTransactionProcessor(db)
        tx_hash = await ton_processor.process_withdrawal(payment.id)
        
        return WithdrawalResponse(
            payment_id=payment.id,
            amount=payment.amount,
            currency=payment.currency,
            fee_amount=payment.fee_amount,
            net_amount=payment.net_amount,
            address=withdrawal_request.address,
            status=payment.status.value,
            tx_hash=tx_hash,
            created_at=payment.created_at
        )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stars withdrawals not yet supported"
        )


@router.get("/history", response_model=list[PaymentHistory])
async def get_payment_history(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get payment history.
    
    Args:
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Payment history
    """
    payment_repo = PaymentRepository(db)
    payments = payment_repo.get_user_payments(current_user["id"])
    
    return [
        PaymentHistory(
            payment_id=p.id,
            payment_type=p.payment_type.value,
            payment_method=p.payment_method.value,
            amount=p.amount,
            currency=p.currency,
            status=p.status.value,
            created_at=p.created_at,
            completed_at=p.completed_at
        )
        for p in payments
    ]
