"""Profit analysis system."""
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy.orm import Session

from src.economics.core.profit_tracker import ProfitTracker
from src.economics.game.house_profit import HouseProfit


class ProfitAnalyzer:
    """Analyze platform profit."""
    
    def __init__(self, db: Session):
        """
        Initialize profit analyzer.
        
        Args:
            db: Database session
        """
        self.db = db
        self.profit_tracker = ProfitTracker(db)
        self.house_profit = HouseProfit(db)
    
    def analyze_profit_trends(
        self,
        days: int = 30
    ) -> Dict:
        """
        Analyze profit trends over period.
        
        Args:
            days: Number of days to analyze
        
        Returns:
            Profit trends analysis
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        daily_profits = []
        current_date = start_date
        
        while current_date < end_date:
            daily_profit = self.profit_tracker.calculate_daily_profit(current_date)
            daily_profits.append(daily_profit)
            current_date += timedelta(days=1)
        
        if not daily_profits:
            return {
                "period_days": days,
                "average_daily_profit": Decimal("0.0"),
                "total_profit": Decimal("0.0"),
                "trend": "stable",
            }
        
        total_profit = sum(
            Decimal(str(p.get("profit_ton", 0))) + Decimal(str(p.get("profit_stars", 0)))
            for p in daily_profits
        )
        average_daily = total_profit / Decimal(str(len(daily_profits)))
        
        # Calculate trend
        first_half = daily_profits[:len(daily_profits)//2]
        second_half = daily_profits[len(daily_profits)//2:]
        
        first_half_profit = sum(
            Decimal(str(p.get("profit_ton", 0))) + Decimal(str(p.get("profit_stars", 0)))
            for p in first_half
        )
        second_half_profit = sum(
            Decimal(str(p.get("profit_ton", 0))) + Decimal(str(p.get("profit_stars", 0)))
            for p in second_half
        )
        
        if second_half_profit > first_half_profit * Decimal("1.1"):
            trend = "increasing"
        elif second_half_profit < first_half_profit * Decimal("0.9"):
            trend = "decreasing"
        else:
            trend = "stable"
        
        return {
            "period_days": days,
            "average_daily_profit": float(average_daily),
            "total_profit": float(total_profit),
            "trend": trend,
            "daily_profits": daily_profits,
        }
    
    def get_profit_breakdown(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """
        Get detailed profit breakdown.
        
        Args:
            start_date: Start date
            end_date: End date
        
        Returns:
            Profit breakdown
        """
        return self.house_profit.get_profit_statistics(start_date, end_date)
    
    def compare_periods(
        self,
        period1_start: datetime,
        period1_end: datetime,
        period2_start: datetime,
        period2_end: datetime
    ) -> Dict:
        """
        Compare profit between two periods.
        
        Args:
            period1_start: Period 1 start
            period1_end: Period 1 end
            period2_start: Period 2 start
            period2_end: Period 2 end
        
        Returns:
            Comparison analysis
        """
        period1_stats = self.house_profit.get_profit_statistics(period1_start, period1_end)
        period2_stats = self.house_profit.get_profit_statistics(period2_start, period2_end)
        
        period1_total = period1_stats["total_profit_ton"] + period1_stats["total_profit_stars"]
        period2_total = period2_stats["total_profit_ton"] + period2_stats["total_profit_stars"]
        
        change = period2_total - period1_total
        change_percent = (change / period1_total * 100) if period1_total > 0 else 0
        
        return {
            "period1": period1_stats,
            "period2": period2_stats,
            "change": change,
            "change_percent": change_percent,
        }
