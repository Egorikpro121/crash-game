"""House edge calculation for crash game."""
from decimal import Decimal
from typing import Optional


class HouseEdgeCalculator:
    """Calculate house edge for the game."""
    
    def __init__(self, house_edge_percent: Decimal = Decimal("0.01")):
        """
        Initialize house edge calculator.
        
        Args:
            house_edge_percent: House edge percentage (default 1% = 0.01)
        """
        self.house_edge = house_edge_percent
    
    def calculate_expected_multiplier(self, base_multiplier: Decimal) -> Decimal:
        """
        Calculate expected multiplier with house edge applied.
        
        Args:
            base_multiplier: Base multiplier without house edge
        
        Returns:
            Expected multiplier with house edge
        """
        # House edge reduces the expected multiplier
        # Formula: expected_multiplier = base_multiplier * (1 - house_edge)
        return base_multiplier * (Decimal("1.0") - self.house_edge)
    
    def calculate_house_profit(self, total_bets: Decimal, total_payouts: Decimal) -> Decimal:
        """
        Calculate house profit from a round.
        
        Args:
            total_bets: Total amount bet in round
            total_payouts: Total amount paid out
        
        Returns:
            House profit
        """
        return total_bets - total_payouts
    
    def calculate_house_profit_percentage(self, total_bets: Decimal, total_payouts: Decimal) -> Decimal:
        """
        Calculate house profit as percentage.
        
        Args:
            total_bets: Total amount bet
            total_payouts: Total amount paid out
        
        Returns:
            Profit percentage
        """
        if total_bets == 0:
            return Decimal("0.0")
        return (total_bets - total_payouts) / total_bets * Decimal("100")
    
    def adjust_crash_multiplier(self, base_multiplier: Decimal) -> Decimal:
        """
        Adjust crash multiplier to account for house edge.
        
        Args:
            base_multiplier: Base multiplier from provably fair
        
        Returns:
            Adjusted multiplier
        """
        # House edge is built into the crash probability distribution
        # This method can be used for verification
        return base_multiplier
    
    def get_house_edge(self) -> Decimal:
        """Get current house edge."""
        return self.house_edge
    
    def set_house_edge(self, house_edge_percent: Decimal):
        """
        Set house edge.
        
        Args:
            house_edge_percent: New house edge percentage
        """
        if house_edge_percent < 0 or house_edge_percent > Decimal("0.1"):
            raise ValueError("House edge must be between 0 and 10%")
        self.house_edge = house_edge_percent
