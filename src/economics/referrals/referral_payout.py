"""Referral payout processing."""
from decimal import Decimal
from datetime import datetime
from typing import List, Dict
from sqlalchemy.orm import Session

from src.database.repositories.user_repo import UserRepository
from src.database.repositories.transaction_repo import TransactionRepository, TransactionType
from src.economics.referrals.referral_calculator import ReferralCalculator


class ReferralPayout:
    """Handle referral payouts."""
    
    def __init__(self, db: Session):
        """
        Initialize referral payout handler.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.transaction_repo = TransactionRepository(db)
        self.calculator = ReferralCalculator(db)
    
    def process_deposit_referral(
        self,
        user_id: int,
        deposit_amount: Decimal,
        currency: str
    ) -> Decimal:
        """
        Process referral payout when user makes deposit.
        
        Args:
            user_id: User who made deposit
            deposit_amount: Deposit amount
            currency: Currency
        
        Returns:
            Referral payout amount
        """
        user = self.user_repo.get_by_id(user_id)
        if not user or not user.referred_by_id:
            return Decimal("0.0")
        
        referrer_id = user.referred_by_id
        
        # Calculate and apply payout
        payout = self.calculator.apply_referral_payout(
            referrer_id, user_id, deposit_amount, currency
        )
        
        return payout
    
    def get_pending_payouts(self, referrer_id: int) -> List[Dict]:
        """
        Get pending referral payouts for a user.
        
        Args:
            referrer_id: User ID
        
        Returns:
            List of pending payouts
        """
        # Get all transactions of type REFERRAL for this user
        transactions = self.transaction_repo.get_user_transactions(
            referrer_id, TransactionType.REFERRAL
        )
        
        payouts = []
        for transaction in transactions:
            payouts.append({
                "id": transaction.id,
                "amount": transaction.amount,
                "currency": transaction.currency,
                "description": transaction.description,
                "created_at": transaction.created_at.isoformat() if transaction.created_at else None,
            })
        
        return payouts
    
    def get_total_payouts(self, referrer_id: int) -> Dict:
        """
        Get total referral payouts for a user.
        
        Args:
            referrer_id: User ID
        
        Returns:
            Total payouts breakdown
        """
        user = self.user_repo.get_by_id(referrer_id)
        if not user:
            return {
                "total_ton": Decimal("0.0"),
                "total_stars": Decimal("0.0"),
            }
        
        return {
            "total_ton": user.total_referral_earnings_ton or Decimal("0.0"),
            "total_stars": user.total_referral_earnings_stars or Decimal("0.0"),
        }
