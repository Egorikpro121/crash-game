"""House profit calculations."""
from decimal import Decimal
from typing import Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.database.repositories.game_repo import GameRoundRepository
from src.economics.core.profit_tracker import ProfitTracker


class HouseProfit:
    """Calculate house profit."""
    
    def __init__(self, db: Session):
        """
        Initialize house profit calculator.
        
        Args:
            db: Database session
        """
        self.db = db
        self.round_repo = GameRoundRepository(db)
        self.profit_tracker = ProfitTracker(db)
    
    def calculate_round_profit(self, round_id: int) -> Dict:
        """
        Calculate profit from a specific round.
        
        Args:
            round_id: Round ID
        
        Returns:
            Profit breakdown
        """
        return self.profit_tracker.calculate_round_profit(round_id)
    
    def calculate_daily_profit(self, date: Optional[datetime] = None) -> Dict:
        """
        Calculate profit for a specific day.
        
        Args:
            date: Date to calculate for
        
        Returns:
            Daily profit breakdown
        """
        return self.profit_tracker.calculate_daily_profit(date)
    
    def calculate_total_profit(self) -> Dict:
        """
        Calculate total platform profit.
        
        Returns:
            Total profit breakdown
        """
        return self.profit_tracker.calculate_total_profit()
    
    def get_profit_statistics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """
        Get profit statistics for a period.
        
        Args:
            start_date: Start date
            end_date: End date
        
        Returns:
            Profit statistics
        """
        rounds = self.round_repo.get_latest_rounds(limit=10000)
        
        if start_date:
            rounds = [r for r in rounds if r.crashed_at and r.crashed_at >= start_date]
        if end_date:
            rounds = [r for r in rounds if r.crashed_at and r.crashed_at <= end_date]
        
        total_profit_ton = Decimal("0.0")
        total_profit_stars = Decimal("0.0")
        total_bets_ton = Decimal("0.0")
        total_bets_stars = Decimal("0.0")
        
        for round_obj in rounds:
            total_bets_ton += round_obj.total_bet_amount_ton or Decimal("0.0")
            total_bets_stars += round_obj.total_bet_amount_stars or Decimal("0.0")
            
            profit_ton = (round_obj.total_bet_amount_ton or Decimal("0.0")) - (round_obj.total_payout_ton or Decimal("0.0"))
            profit_stars = (round_obj.total_bet_amount_stars or Decimal("0.0")) - (round_obj.total_payout_stars or Decimal("0.0"))
            
            total_profit_ton += profit_ton
            total_profit_stars += profit_stars
        
        return {
            "rounds_count": len(rounds),
            "total_bets_ton": float(total_bets_ton),
            "total_bets_stars": float(total_bets_stars),
            "total_profit_ton": float(total_profit_ton),
            "total_profit_stars": float(total_profit_stars),
            "average_profit_per_round": float(
                (total_profit_ton + total_profit_stars) / Decimal(str(len(rounds)))
            ) if rounds else 0.0,
        }
