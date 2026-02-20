"""Crash probability calculations."""
from decimal import Decimal
import math
from typing import Dict


class CrashProbability:
    """Calculate crash probabilities for different multipliers."""
    
    def __init__(self, house_edge: Decimal = Decimal("0.01")):
        """
        Initialize crash probability calculator.
        
        Args:
            house_edge: House edge percentage
        """
        self.house_edge = house_edge
    
    def calculate_crash_probability(self, multiplier: Decimal) -> Decimal:
        """
        Calculate probability of crashing at or before multiplier.
        
        Args:
            multiplier: Target multiplier
        
        Returns:
            Probability (0.0 to 1.0)
        """
        # Simplified probability model
        # Higher multipliers have lower probability
        # Formula: P(crash <= x) = 1 - (1 / (x * (1 + house_edge)))
        
        if multiplier <= Decimal("1.0"):
            return Decimal("1.0")
        
        probability = Decimal("1.0") - (Decimal("1.0") / (multiplier * (Decimal("1.0") + self.house_edge)))
        
        # Ensure probability is between 0 and 1
        return max(Decimal("0.0"), min(Decimal("1.0"), probability))
    
    def calculate_survival_probability(self, multiplier: Decimal) -> Decimal:
        """
        Calculate probability of surviving past multiplier.
        
        Args:
            multiplier: Target multiplier
        
        Returns:
            Survival probability (0.0 to 1.0)
        """
        return Decimal("1.0") - self.calculate_crash_probability(multiplier)
    
    def get_expected_value(self, bet_amount: Decimal, multiplier: Decimal) -> Decimal:
        """
        Calculate expected value of a bet.
        
        Args:
            bet_amount: Amount bet
            multiplier: Target multiplier
        
        Returns:
            Expected value
        """
        survival_prob = self.calculate_survival_probability(multiplier)
        payout = bet_amount * multiplier
        
        # Expected value = (probability * payout) - bet_amount
        expected_value = (survival_prob * payout) - bet_amount
        
        return expected_value
    
    def get_house_edge_impact(self, multiplier: Decimal) -> Decimal:
        """
        Calculate house edge impact on a multiplier.
        
        Args:
            multiplier: Multiplier
        
        Returns:
            House edge impact
        """
        # House edge reduces expected payout
        fair_multiplier = multiplier / (Decimal("1.0") - self.house_edge)
        return multiplier - fair_multiplier
    
    def get_probability_table(self, multipliers: list[Decimal]) -> Dict[Decimal, Decimal]:
        """
        Get probability table for multiple multipliers.
        
        Args:
            multipliers: List of multipliers
        
        Returns:
            Dictionary mapping multiplier to probability
        """
        return {
            mult: self.calculate_crash_probability(mult)
            for mult in multipliers
        }
