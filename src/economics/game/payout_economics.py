"""Payout economics calculations."""
from decimal import Decimal
from typing import Dict, List
from sqlalchemy.orm import Session

from src.database.repositories.game_repo import BetRepository
from src.economics.core.payout_calculator import PayoutCalculator


class PayoutEconomics:
    """Calculate payout economics."""
    
    def __init__(self, db: Session):
        """
        Initialize payout economics calculator.
        
        Args:
            db: Database session
        """
        self.db = db
        self.bet_repo = BetRepository(db)
        self.payout_calculator = PayoutCalculator()
    
    def calculate_bet_payout(
        self,
        bet_id: int,
        multiplier: Decimal
    ) -> Dict:
        """
        Calculate payout for a specific bet.
        
        Args:
            bet_id: Bet ID
            multiplier: Multiplier at cashout
        
        Returns:
            Payout breakdown
        """
        bet = self.bet_repo.get_by_id(bet_id)
        if not bet:
            return {}
        
        bet_amount = (
            bet.amount_ton if bet.currency == "TON"
            else bet.amount_stars
        ) or Decimal("0.0")
        
        payout = self.payout_calculator.calculate_payout(bet_amount, multiplier)
        profit = self.payout_calculator.calculate_profit(bet_amount, payout)
        roi = self.payout_calculator.calculate_roi(bet_amount, payout)
        
        return {
            "bet_id": bet_id,
            "bet_amount": float(bet_amount),
            "currency": bet.currency,
            "multiplier": float(multiplier),
            "payout": float(payout),
            "profit": float(profit),
            "roi": float(roi),
        }
    
    def calculate_total_payouts(
        self,
        bets: List[tuple[Decimal, Decimal]],
        currency: str
    ) -> Dict:
        """
        Calculate total payouts for multiple bets.
        
        Args:
            bets: List of (bet_amount, multiplier) tuples
            currency: Currency
        
        Returns:
            Total payouts breakdown
        """
        total_payout = self.payout_calculator.calculate_total_payout(bets)
        total_bet = sum(bet_amount for bet_amount, _ in bets)
        total_profit = total_payout - total_bet
        
        return {
            "currency": currency,
            "total_bet": float(total_bet),
            "total_payout": float(total_payout),
            "total_profit": float(total_profit),
            "bets_count": len(bets),
        }
