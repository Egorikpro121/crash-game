"""Game statistics analytics."""
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, Optional
from sqlalchemy.orm import Session

from src.database.repositories.game_repo import GameRoundRepository
from src.economics.game.multiplier_distribution import MultiplierDistribution


class GameStatistics:
    """Generate game statistics."""
    
    def __init__(self, db: Session):
        """
        Initialize game statistics generator.
        
        Args:
            db: Database session
        """
        self.db = db
        self.round_repo = GameRoundRepository(db)
        self.multiplier_dist = MultiplierDistribution()
    
    def get_round_statistics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """
        Get statistics for rounds in period.
        
        Args:
            start_date: Start date
            end_date: End date
        
        Returns:
            Round statistics
        """
        rounds = self.round_repo.get_latest_rounds(limit=10000)
        
        if start_date:
            rounds = [r for r in rounds if r.crashed_at and r.crashed_at >= start_date]
        if end_date:
            rounds = [r for r in rounds if r.crashed_at and r.crashed_at <= end_date]
        
        if not rounds:
            return {
                "total_rounds": 0,
                "average_multiplier": Decimal("0.0"),
                "biggest_multiplier": Decimal("0.0"),
                "smallest_multiplier": Decimal("0.0"),
            }
        
        crash_points = [r.crash_multiplier for r in rounds if r.crash_multiplier]
        
        if not crash_points:
            return {
                "total_rounds": len(rounds),
                "average_multiplier": Decimal("0.0"),
            }
        
        avg_multiplier = sum(crash_points) / Decimal(str(len(crash_points)))
        biggest = max(crash_points)
        smallest = min(crash_points)
        
        # Distribution statistics
        dist_stats = self.multiplier_dist.get_statistics(crash_points)
        
        return {
            "total_rounds": len(rounds),
            "average_multiplier": float(avg_multiplier),
            "biggest_multiplier": float(biggest),
            "smallest_multiplier": float(smallest),
            "distribution": dist_stats,
        }
    
    def get_hourly_statistics(
        self,
        date: Optional[datetime] = None
    ) -> Dict:
        """
        Get hourly statistics for a day.
        
        Args:
            date: Date to analyze
        
        Returns:
            Hourly statistics
        """
        if date is None:
            date = datetime.utcnow()
        
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        
        rounds = self.round_repo.get_latest_rounds(limit=10000)
        daily_rounds = [
            r for r in rounds
            if r.crashed_at and start_date <= r.crashed_at < end_date
        ]
        
        hourly_stats = {}
        for hour in range(24):
            hour_start = start_date.replace(hour=hour)
            hour_end = hour_start + timedelta(hours=1)
            
            hour_rounds = [
                r for r in daily_rounds
                if r.crashed_at and hour_start <= r.crashed_at < hour_end
            ]
            
            if hour_rounds:
                crash_points = [r.crash_multiplier for r in hour_rounds if r.crash_multiplier]
                avg_multiplier = sum(crash_points) / Decimal(str(len(crash_points))) if crash_points else Decimal("0.0")
                
                hourly_stats[hour] = {
                    "rounds_count": len(hour_rounds),
                    "average_multiplier": float(avg_multiplier),
                }
            else:
                hourly_stats[hour] = {
                    "rounds_count": 0,
                    "average_multiplier": 0.0,
                }
        
        return {
            "date": date.date().isoformat(),
            "hourly_stats": hourly_stats,
        }
