"""Revenue tracking system."""
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, Optional
from sqlalchemy.orm import Session

from src.database.repositories.payment_repo import PaymentRepository, PaymentType
from src.database.repositories.game_repo import GameRoundRepository
from src.economics.commissions.commission_tracker import CommissionTracker


class RevenueTracker:
    """Track platform revenue."""
    
    def __init__(self, db: Session):
        """
        Initialize revenue tracker.
        
        Args:
            db: Database session
        """
        self.db = db
        self.payment_repo = PaymentRepository(db)
        self.round_repo = GameRoundRepository(db)
        self.commission_tracker = CommissionTracker(db)
    
    def get_daily_revenue(
        self,
        date: Optional[datetime] = None
    ) -> Dict:
        """
        Get daily revenue breakdown.
        
        Args:
            date: Date to check (defaults to today)
        
        Returns:
            Daily revenue breakdown
        """
        if date is None:
            date = datetime.utcnow()
        
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        
        # Get deposits
        deposits = self.payment_repo.get_pending_payments()
        daily_deposits = [
            p for p in deposits
            if p.payment_type == PaymentType.DEPOSIT
            and p.created_at and start_date <= p.created_at < end_date
        ]
        
        deposits_ton = sum(p.amount for p in daily_deposits if p.currency == "TON")
        deposits_stars = sum(p.amount for p in daily_deposits if p.currency == "STARS")
        
        # Get house profit from rounds
        rounds = self.round_repo.get_latest_rounds(limit=10000)
        daily_rounds = [
            r for r in rounds
            if r.crashed_at and start_date <= r.crashed_at < end_date
        ]
        
        house_profit_ton = sum(
            (r.total_bet_amount_ton or Decimal("0.0")) - (r.total_payout_ton or Decimal("0.0"))
            for r in daily_rounds
        )
        house_profit_stars = sum(
            (r.total_bet_amount_stars or Decimal("0.0")) - (r.total_payout_stars or Decimal("0.0"))
            for r in daily_rounds
        )
        
        # Get commissions
        commissions = self.commission_tracker.get_daily_commissions(date)
        
        return {
            "date": date.date().isoformat(),
            "deposits_ton": float(deposits_ton),
            "deposits_stars": float(deposits_stars),
            "house_profit_ton": float(house_profit_ton),
            "house_profit_stars": float(house_profit_stars),
            "commissions_ton": float(commissions["withdrawal_commissions_ton"]),
            "commissions_stars": float(commissions["withdrawal_commissions_stars"]),
            "total_revenue_ton": float(deposits_ton + house_profit_ton + commissions["withdrawal_commissions_ton"]),
            "total_revenue_stars": float(deposits_stars + house_profit_stars + commissions["withdrawal_commissions_stars"]),
            "rounds_count": len(daily_rounds),
        }
    
    def get_total_revenue(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """
        Get total revenue for a period.
        
        Args:
            start_date: Start date
            end_date: End date
        
        Returns:
            Total revenue breakdown
        """
        # Get deposits
        deposits = self.payment_repo.get_pending_payments()
        if start_date:
            deposits = [p for p in deposits if p.created_at >= start_date]
        if end_date:
            deposits = [p for p in deposits if p.created_at <= end_date]
        
        deposits_ton = sum(
            p.amount for p in deposits
            if p.payment_type == PaymentType.DEPOSIT and p.currency == "TON"
        )
        deposits_stars = sum(
            p.amount for p in deposits
            if p.payment_type == PaymentType.DEPOSIT and p.currency == "STARS"
        )
        
        # Get house profit
        rounds = self.round_repo.get_latest_rounds(limit=10000)
        if start_date:
            rounds = [r for r in rounds if r.crashed_at and r.crashed_at >= start_date]
        if end_date:
            rounds = [r for r in rounds if r.crashed_at and r.crashed_at <= end_date]
        
        house_profit_ton = sum(
            (r.total_bet_amount_ton or Decimal("0.0")) - (r.total_payout_ton or Decimal("0.0"))
            for r in rounds
        )
        house_profit_stars = sum(
            (r.total_bet_amount_stars or Decimal("0.0")) - (r.total_payout_stars or Decimal("0.0"))
            for r in rounds
        )
        
        # Get commissions
        commissions = self.commission_tracker.get_total_commissions(start_date, end_date)
        
        return {
            "deposits_ton": float(deposits_ton),
            "deposits_stars": float(deposits_stars),
            "house_profit_ton": float(house_profit_ton),
            "house_profit_stars": float(house_profit_stars),
            "commissions_ton": float(commissions["withdrawal_commissions_ton"]),
            "commissions_stars": float(commissions["withdrawal_commissions_stars"]),
            "total_revenue_ton": float(deposits_ton + house_profit_ton + commissions["withdrawal_commissions_ton"]),
            "total_revenue_stars": float(deposits_stars + house_profit_stars + commissions["withdrawal_commissions_stars"]),
            "rounds_count": len(rounds),
        }
