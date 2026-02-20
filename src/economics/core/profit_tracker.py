"""Profit tracking for the platform."""
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from sqlalchemy.orm import Session

from src.database.repositories.game_repo import GameRoundRepository
from src.database.repositories.payment_repo import PaymentRepository
from src.database.repositories.transaction_repo import TransactionRepository


class ProfitTracker:
    """Track platform profit."""
    
    def __init__(self, db: Session):
        """
        Initialize profit tracker.
        
        Args:
            db: Database session
        """
        self.db = db
        self.round_repo = GameRoundRepository(db)
        self.payment_repo = PaymentRepository(db)
        self.transaction_repo = TransactionRepository(db)
    
    def calculate_round_profit(self, round_id: int) -> Dict[str, Decimal]:
        """
        Calculate profit from a specific round.
        
        Args:
            round_id: Round ID
        
        Returns:
            Dictionary with profit breakdown
        """
        round_obj = self.round_repo.get_by_id(round_id)
        if not round_obj:
            return {
                "total_bets": Decimal("0.0"),
                "total_payouts": Decimal("0.0"),
                "profit": Decimal("0.0"),
            }
        
        total_bets_ton = round_obj.total_bet_amount_ton or Decimal("0.0")
        total_bets_stars = round_obj.total_bet_amount_stars or Decimal("0.0")
        total_payouts_ton = round_obj.total_payout_ton or Decimal("0.0")
        total_payouts_stars = round_obj.total_payout_stars or Decimal("0.0")
        
        profit_ton = total_bets_ton - total_payouts_ton
        profit_stars = total_bets_stars - total_payouts_stars
        
        return {
            "total_bets_ton": total_bets_ton,
            "total_bets_stars": total_bets_stars,
            "total_payouts_ton": total_payouts_ton,
            "total_payouts_stars": total_payouts_stars,
            "profit_ton": profit_ton,
            "profit_stars": profit_stars,
            "total_profit": profit_ton + profit_stars,  # Simplified
        }
    
    def calculate_daily_profit(self, date: Optional[datetime] = None) -> Dict[str, Decimal]:
        """
        Calculate profit for a specific day.
        
        Args:
            date: Date to calculate for (defaults to today)
        
        Returns:
            Daily profit breakdown
        """
        if date is None:
            date = datetime.utcnow()
        
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        
        # Get all rounds for the day
        rounds = self.round_repo.get_latest_rounds(limit=10000)  # Large limit
        daily_rounds = [
            r for r in rounds
            if r.crashed_at and start_date <= r.crashed_at < end_date
        ]
        
        total_bets_ton = Decimal("0.0")
        total_bets_stars = Decimal("0.0")
        total_payouts_ton = Decimal("0.0")
        total_payouts_stars = Decimal("0.0")
        
        for round_obj in daily_rounds:
            total_bets_ton += round_obj.total_bet_amount_ton or Decimal("0.0")
            total_bets_stars += round_obj.total_bet_amount_stars or Decimal("0.0")
            total_payouts_ton += round_obj.total_payout_ton or Decimal("0.0")
            total_payouts_stars += round_obj.total_payout_stars or Decimal("0.0")
        
        profit_ton = total_bets_ton - total_payouts_ton
        profit_stars = total_bets_stars - total_payouts_stars
        
        return {
            "date": date.date().isoformat(),
            "total_bets_ton": total_bets_ton,
            "total_bets_stars": total_bets_stars,
            "total_payouts_ton": total_payouts_ton,
            "total_payouts_stars": total_payouts_stars,
            "profit_ton": profit_ton,
            "profit_stars": profit_stars,
            "rounds_count": len(daily_rounds),
        }
    
    def calculate_total_profit(self) -> Dict[str, Decimal]:
        """
        Calculate total platform profit.
        
        Returns:
            Total profit breakdown
        """
        rounds = self.round_repo.get_latest_rounds(limit=10000)
        
        total_bets_ton = Decimal("0.0")
        total_bets_stars = Decimal("0.0")
        total_payouts_ton = Decimal("0.0")
        total_payouts_stars = Decimal("0.0")
        
        for round_obj in rounds:
            total_bets_ton += round_obj.total_bet_amount_ton or Decimal("0.0")
            total_bets_stars += round_obj.total_bet_amount_stars or Decimal("0.0")
            total_payouts_ton += round_obj.total_payout_ton or Decimal("0.0")
            total_payouts_stars += round_obj.total_payout_stars or Decimal("0.0")
        
        profit_ton = total_bets_ton - total_payouts_ton
        profit_stars = total_bets_stars - total_payouts_stars
        
        return {
            "total_bets_ton": total_bets_ton,
            "total_bets_stars": total_bets_stars,
            "total_payouts_ton": total_payouts_ton,
            "total_payouts_stars": total_payouts_stars,
            "profit_ton": profit_ton,
            "profit_stars": profit_stars,
            "total_rounds": len(rounds),
        }
    
    def calculate_commission_revenue(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Decimal]:
        """
        Calculate revenue from commissions.
        
        Args:
            start_date: Start date
            end_date: End date
        
        Returns:
            Commission revenue breakdown
        """
        payments = self.payment_repo.get_pending_payments()
        
        if start_date:
            payments = [p for p in payments if p.created_at >= start_date]
        if end_date:
            payments = [p for p in payments if p.created_at <= end_date]
        
        total_commission_ton = Decimal("0.0")
        total_commission_stars = Decimal("0.0")
        
        for payment in payments:
            if payment.payment_type.value == "withdrawal":
                if payment.currency == "TON":
                    total_commission_ton += payment.fee_amount or Decimal("0.0")
                else:
                    total_commission_stars += payment.fee_amount or Decimal("0.0")
        
        return {
            "commission_ton": total_commission_ton,
            "commission_stars": total_commission_stars,
            "total_commission": total_commission_ton + total_commission_stars,
        }
