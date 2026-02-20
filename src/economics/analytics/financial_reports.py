"""Financial reports generation."""
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, Optional
from sqlalchemy.orm import Session

from src.economics.analytics.revenue_tracker import RevenueTracker
from src.economics.analytics.profit_analyzer import ProfitAnalyzer
from src.economics.core.profit_tracker import ProfitTracker
from src.economics.commissions.commission_tracker import CommissionTracker


class FinancialReports:
    """Generate financial reports."""
    
    def __init__(self, db: Session):
        """
        Initialize financial reports generator.
        
        Args:
            db: Database session
        """
        self.db = db
        self.revenue_tracker = RevenueTracker(db)
        self.profit_analyzer = ProfitAnalyzer(db)
        self.profit_tracker = ProfitTracker(db)
        self.commission_tracker = CommissionTracker(db)
    
    def generate_daily_report(
        self,
        date: Optional[datetime] = None
    ) -> Dict:
        """
        Generate daily financial report.
        
        Args:
            date: Date for report
        
        Returns:
            Daily report
        """
        revenue = self.revenue_tracker.get_daily_revenue(date)
        profit = self.profit_tracker.calculate_daily_profit(date)
        commissions = self.commission_tracker.get_daily_commissions(date)
        
        return {
            "date": date.date().isoformat() if date else datetime.utcnow().date().isoformat(),
            "revenue": revenue,
            "profit": profit,
            "commissions": commissions,
        }
    
    def generate_weekly_report(
        self,
        week_start: Optional[datetime] = None
    ) -> Dict:
        """
        Generate weekly financial report.
        
        Args:
            week_start: Week start date
        
        Returns:
            Weekly report
        """
        if week_start is None:
            week_start = datetime.utcnow() - timedelta(days=datetime.utcnow().weekday())
        
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        week_end = week_start + timedelta(days=7)
        
        revenue = self.revenue_tracker.get_total_revenue(week_start, week_end)
        profit_stats = self.profit_analyzer.get_profit_breakdown(week_start, week_end)
        commissions = self.commission_tracker.get_total_commissions(week_start, week_end)
        
        return {
            "period": {
                "start": week_start.isoformat(),
                "end": week_end.isoformat(),
            },
            "revenue": revenue,
            "profit": profit_stats,
            "commissions": commissions,
        }
    
    def generate_monthly_report(
        self,
        month: Optional[int] = None,
        year: Optional[int] = None
    ) -> Dict:
        """
        Generate monthly financial report.
        
        Args:
            month: Month (1-12)
            year: Year
        
        Returns:
            Monthly report
        """
        if month is None:
            month = datetime.utcnow().month
        if year is None:
            year = datetime.utcnow().year
        
        month_start = datetime(year, month, 1)
        if month == 12:
            month_end = datetime(year + 1, 1, 1)
        else:
            month_end = datetime(year, month + 1, 1)
        
        revenue = self.revenue_tracker.get_total_revenue(month_start, month_end)
        profit_stats = self.profit_analyzer.get_profit_breakdown(month_start, month_end)
        commissions = self.commission_tracker.get_total_commissions(month_start, month_end)
        
        return {
            "period": {
                "month": month,
                "year": year,
                "start": month_start.isoformat(),
                "end": month_end.isoformat(),
            },
            "revenue": revenue,
            "profit": profit_stats,
            "commissions": commissions,
        }
    
    def generate_summary_report(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """
        Generate summary report for period.
        
        Args:
            start_date: Start date
            end_date: End date
        
        Returns:
            Summary report
        """
        revenue = self.revenue_tracker.get_total_revenue(start_date, end_date)
        profit_stats = self.profit_analyzer.get_profit_breakdown(start_date, end_date)
        commissions = self.commission_tracker.get_total_commissions(start_date, end_date)
        
        return {
            "period": {
                "start": start_date.isoformat() if start_date else None,
                "end": end_date.isoformat() if end_date else None,
            },
            "revenue": revenue,
            "profit": profit_stats,
            "commissions": commissions,
        }
