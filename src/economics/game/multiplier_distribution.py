"""Multiplier distribution system for crash game."""
from decimal import Decimal
import random
from typing import Dict, List


class MultiplierDistribution:
    """Manage multiplier distribution probabilities."""
    
    # Distribution targets:
    # 30% of rounds crash before 2x
    # 50% of rounds crash between 2x and 5x
    # 20% of rounds crash above 5x
    
    CRASH_BEFORE_2X_PROBABILITY = Decimal("0.30")
    CRASH_2X_TO_5X_PROBABILITY = Decimal("0.50")
    CRASH_ABOVE_5X_PROBABILITY = Decimal("0.20")
    
    def get_distribution_weights(self) -> Dict[str, Decimal]:
        """
        Get distribution weights for multiplier ranges.
        
        Returns:
            Dictionary with distribution weights
        """
        return {
            "before_2x": self.CRASH_BEFORE_2X_PROBABILITY,
            "2x_to_5x": self.CRASH_2X_TO_5X_PROBABILITY,
            "above_5x": self.CRASH_ABOVE_5X_PROBABILITY,
        }
    
    def get_target_range(self) -> tuple[Decimal, Decimal]:
        """
        Get target multiplier range based on distribution.
        
        Returns:
            Tuple of (min_multiplier, max_multiplier)
        """
        rand = random.random()
        
        if rand < float(self.CRASH_BEFORE_2X_PROBABILITY):
            # Crash before 2x: 1.00 - 1.99
            return Decimal("1.00"), Decimal("1.99")
        elif rand < float(self.CRASH_BEFORE_2X_PROBABILITY + self.CRASH_2X_TO_5X_PROBABILITY):
            # Crash between 2x and 5x: 2.00 - 4.99
            return Decimal("2.00"), Decimal("4.99")
        else:
            # Crash above 5x: 5.00 - 10.00+
            return Decimal("5.00"), Decimal("10.00")
    
    def adjust_crash_point(
        self,
        base_crash_point: Decimal,
        house_edge: Decimal = Decimal("0.01")
    ) -> Decimal:
        """
        Adjust crash point to maintain distribution while applying house edge.
        
        Args:
            base_crash_point: Base crash point from provably fair
            house_edge: House edge percentage
        
        Returns:
            Adjusted crash point
        """
        # House edge is already built into provably fair calculation
        # This method can be used for verification/adjustment if needed
        return base_crash_point
    
    def get_expected_multiplier(self) -> Decimal:
        """
        Calculate expected multiplier based on distribution.
        
        Returns:
            Expected multiplier
        """
        # Weighted average: 0.30 * 1.5 + 0.50 * 3.5 + 0.20 * 7.5
        expected = (
            self.CRASH_BEFORE_2X_PROBABILITY * Decimal("1.5") +
            self.CRASH_2X_TO_5X_PROBABILITY * Decimal("3.5") +
            self.CRASH_ABOVE_5X_PROBABILITY * Decimal("7.5")
        )
        return expected
    
    def get_statistics(self, crash_points: List[Decimal]) -> Dict:
        """
        Get statistics from actual crash points.
        
        Args:
            crash_points: List of crash multipliers
        
        Returns:
            Statistics dictionary
        """
        if not crash_points:
            return {
                "total_rounds": 0,
                "before_2x": 0,
                "2x_to_5x": 0,
                "above_5x": 0,
                "average_multiplier": Decimal("0.0"),
            }
        
        before_2x = sum(1 for cp in crash_points if cp < Decimal("2.0"))
        between_2x_5x = sum(1 for cp in crash_points if Decimal("2.0") <= cp < Decimal("5.0"))
        above_5x = sum(1 for cp in crash_points if cp >= Decimal("5.0"))
        
        total = len(crash_points)
        avg_multiplier = sum(crash_points) / Decimal(str(total))
        
        return {
            "total_rounds": total,
            "before_2x": before_2x,
            "before_2x_percent": float(Decimal(str(before_2x)) / Decimal(str(total)) * Decimal("100")),
            "2x_to_5x": between_2x_5x,
            "2x_to_5x_percent": float(Decimal(str(between_2x_5x)) / Decimal(str(total)) * Decimal("100")),
            "above_5x": above_5x,
            "above_5x_percent": float(Decimal(str(above_5x)) / Decimal(str(total)) * Decimal("100")),
            "average_multiplier": avg_multiplier,
        }
