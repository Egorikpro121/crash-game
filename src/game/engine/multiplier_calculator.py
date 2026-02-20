"""Multiplier calculator for crash game."""
from decimal import Decimal
from typing import Optional
from datetime import datetime, timedelta

from src.game.engine.provably_fair import ProvablyFair


class MultiplierCalculator:
    """Calculate multipliers for crash game."""
    
    def __init__(self, base_speed_ms: int = 100):
        """
        Initialize multiplier calculator.
        
        Args:
            base_speed_ms: Milliseconds per 0.01x multiplier increase
        """
        self.base_speed_ms = base_speed_ms
    
    def calculate_current_multiplier(self, crash_point: Decimal, 
                                    start_time: datetime,
                                    current_time: Optional[datetime] = None) -> Decimal:
        """
        Calculate current multiplier based on elapsed time.
        
        Args:
            crash_point: Final crash multiplier
            start_time: Round start time
            current_time: Current time (defaults to now)
        
        Returns:
            Current multiplier
        """
        if current_time is None:
            current_time = datetime.utcnow()
        
        elapsed_ms = int((current_time - start_time).total_seconds() * 1000)
        
        return ProvablyFair.calculate_multiplier_at_time(
            crash_point, elapsed_ms, self.base_speed_ms
        )
    
    def has_crashed(self, crash_point: Decimal, start_time: datetime,
                   current_time: Optional[datetime] = None) -> bool:
        """
        Check if round has crashed.
        
        Args:
            crash_point: Final crash multiplier
            start_time: Round start time
            current_time: Current time (defaults to now)
        
        Returns:
            True if round has crashed
        """
        current_multiplier = self.calculate_current_multiplier(
            crash_point, start_time, current_time
        )
        return current_multiplier >= crash_point
    
    def get_time_until_multiplier(self, target_multiplier: Decimal,
                                 start_time: datetime,
                                 crash_point: Decimal) -> Optional[int]:
        """
        Calculate milliseconds until target multiplier is reached.
        
        Args:
            target_multiplier: Target multiplier
            start_time: Round start time
            crash_point: Final crash multiplier
        
        Returns:
            Milliseconds until target multiplier, or None if already passed or unreachable
        """
        if target_multiplier >= crash_point:
            return None
        
        # Calculate time needed: (multiplier - 1) * base_speed_ms / 0.01
        multiplier_diff = target_multiplier - Decimal("1.0")
        ms_needed = int(multiplier_diff * Decimal("100") * Decimal(str(self.base_speed_ms)))
        
        elapsed_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        
        if elapsed_ms >= ms_needed:
            return None
        
        return ms_needed - elapsed_ms
    
    def get_multiplier_at_time(self, crash_point: Decimal, elapsed_ms: int) -> Decimal:
        """
        Get multiplier at specific elapsed time.
        
        Args:
            crash_point: Final crash multiplier
            elapsed_ms: Milliseconds elapsed
        
        Returns:
            Multiplier at that time
        """
        return ProvablyFair.calculate_multiplier_at_time(
            crash_point, elapsed_ms, self.base_speed_ms
        )
