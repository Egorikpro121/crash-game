"""Referral calculation system."""
from decimal import Decimal
from sqlalchemy.orm import Session

from src.database.repositories.user_repo import UserRepository
from src.database.repositories.transaction_repo import TransactionRepository, TransactionType


class ReferralCalculator:
    """Calculate referral payouts."""
    
    REFERRAL_COMMISSION_PERCENT = Decimal("0.05")  # 5%
    
    def __init__(self, db: Session):
        """
        Initialize referral calculator.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.transaction_repo = TransactionRepository(db)
    
    def calculate_referral_payout(
        self,
        deposit_amount: Decimal,
        currency: str
    ) -> Decimal:
        """
        Calculate referral payout from deposit.
        
        Args:
            deposit_amount: Deposit amount
            currency: Currency
        
        Returns:
            Referral payout amount (5% of deposit)
        """
        return deposit_amount * self.REFERRAL_COMMISSION_PERCENT
    
    def apply_referral_payout(
        self,
        referrer_id: int,
        referred_id: int,
        payout_amount: Decimal,
        currency: str
    ) -> Decimal:
        """
        Apply referral payout to referrer.
        
        Args:
            referrer_id: User who referred
            referred_id: User who made deposit
            payout_amount: Payout amount
            currency: Currency
        
        Returns:
            Payout amount applied
        """
        referrer = self.user_repo.get_by_id(referrer_id)
        if not referrer:
            return Decimal("0.0")
        
        # Add payout to referrer balance
        if currency == "TON":
            self.user_repo.update_balance(referrer_id, amount_ton=payout_amount)
            balance_before = referrer.balance_ton
            balance_after = balance_before + payout_amount
        else:
            self.user_repo.update_balance(referrer_id, amount_stars=payout_amount)
            balance_before = referrer.balance_stars
            balance_after = balance_before + payout_amount
        
        # Update referrer statistics
        if currency == "TON":
            referrer.total_referral_earnings_ton = (
                (referrer.total_referral_earnings_ton or Decimal("0.0")) + payout_amount
            )
        else:
            referrer.total_referral_earnings_stars = (
                (referrer.total_referral_earnings_stars or Decimal("0.0")) + payout_amount
            )
        
        referrer.referral_count = (referrer.referral_count or 0) + 1
        
        self.db.commit()
        
        # Create transaction record
        self.transaction_repo.create(
            user_id=referrer_id,
            transaction_type=TransactionType.REFERRAL,
            currency=currency,
            amount=payout_amount,
            balance_before=balance_before,
            balance_after=balance_after,
            description=f"Referral payout from user {referred_id}: {payout_amount} {currency}",
        )
        
        return payout_amount
