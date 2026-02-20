"""Payout calculation for bets."""
from decimal import Decimal
from typing import Optional


class PayoutCalculator:
    """Calculate payouts for bets."""
    
    def calculate_payout(
        self,
        bet_amount: Decimal,
        multiplier: Decimal
    ) -> Decimal:
        """
        Calculate payout for a bet.
        
        Args:
            bet_amount: Amount bet
            multiplier: Multiplier at cashout
        
        Returns:
            Payout amount
        """
        return bet_amount * multiplier
    
    def calculate_profit(
        self,
        bet_amount: Decimal,
        payout: Decimal
    ) -> Decimal:
        """
        Calculate profit from a bet.
        
        Args:
            bet_amount: Amount bet
            payout: Payout amount
        
        Returns:
            Profit (can be negative if lost)
        """
        return payout - bet_amount
    
    def calculate_roi(
        self,
        bet_amount: Decimal,
        payout: Decimal
    ) -> Decimal:
        """
        Calculate Return on Investment (ROI).
        
        Args:
            bet_amount: Amount bet
            payout: Payout amount
        
        Returns:
            ROI percentage
        """
        if bet_amount == 0:
            return Decimal("0.0")
        
        profit = payout - bet_amount
        return (profit / bet_amount) * Decimal("100")
    
    def calculate_total_payout(
        self,
        bets: list[tuple[Decimal, Decimal]]  # List of (bet_amount, multiplier)
    ) -> Decimal:
        """
        Calculate total payout for multiple bets.
        
        Args:
            bets: List of (bet_amount, multiplier) tuples
        
        Returns:
            Total payout
        """
        total = Decimal("0.0")
        for bet_amount, multiplier in bets:
            total += self.calculate_payout(bet_amount, multiplier)
        return total
    
    def calculate_house_edge_impact(
        self,
        total_bets: Decimal,
        total_payouts: Decimal
    ) -> Decimal:
        """
        Calculate house edge impact on payouts.
        
        Args:
            total_bets: Total amount bet
            total_payouts: Total amount paid out
        
        Returns:
            House edge impact (profit)
        """
        return total_bets - total_payouts
