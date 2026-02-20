"""Round economics calculations."""
from decimal import Decimal
from typing import Dict, List
from sqlalchemy.orm import Session

from src.database.repositories.game_repo import GameRoundRepository, BetRepository
from src.economics.core.payout_calculator import PayoutCalculator
from src.economics.core.house_edge import HouseEdgeCalculator


class RoundEconomics:
    """Calculate economics for a game round."""
    
    def __init__(self, db: Session):
        """
        Initialize round economics calculator.
        
        Args:
            db: Database session
        """
        self.db = db
        self.round_repo = GameRoundRepository(db)
        self.bet_repo = BetRepository(db)
        self.payout_calculator = PayoutCalculator()
        self.house_edge = HouseEdgeCalculator()
    
    def calculate_round_economics(self, round_id: int) -> Dict:
        """
        Calculate complete economics for a round.
        
        Args:
            round_id: Round ID
        
        Returns:
            Economics breakdown
        """
        round_obj = self.round_repo.get_by_id(round_id)
        if not round_obj:
            return {}
        
        # Get all bets for round
        bets = self.bet_repo.get_active_bets_by_round(round_id)
        
        total_bets_ton = Decimal("0.0")
        total_bets_stars = Decimal("0.0")
        total_payouts_ton = Decimal("0.0")
        total_payouts_stars = Decimal("0.0")
        
        for bet in bets:
            if bet.currency == "TON":
                total_bets_ton += bet.amount_ton or Decimal("0.0")
                if bet.payout_ton:
                    total_payouts_ton += bet.payout_ton
            else:
                total_bets_stars += bet.amount_stars or Decimal("0.0")
                if bet.payout_stars:
                    total_payouts_stars += bet.payout_stars
        
        house_profit_ton = total_bets_ton - total_payouts_ton
        house_profit_stars = total_bets_stars - total_payouts_stars
        
        return {
            "round_id": round_id,
            "crash_multiplier": float(round_obj.crash_multiplier or Decimal("0.0")),
            "total_bets_ton": float(total_bets_ton),
            "total_bets_stars": float(total_bets_stars),
            "total_payouts_ton": float(total_payouts_ton),
            "total_payouts_stars": float(total_payouts_stars),
            "house_profit_ton": float(house_profit_ton),
            "house_profit_stars": float(house_profit_stars),
            "house_profit_percentage": float(
                self.house_edge.calculate_house_profit_percentage(
                    total_bets_ton + total_bets_stars,
                    total_payouts_ton + total_payouts_stars
                )
            ) if (total_bets_ton + total_bets_stars) > 0 else 0.0,
            "bets_count": len(bets),
        }
    
    def calculate_potential_payouts(
        self,
        round_id: int,
        current_multiplier: Decimal
    ) -> Dict:
        """
        Calculate potential payouts at current multiplier.
        
        Args:
            round_id: Round ID
            current_multiplier: Current multiplier
        
        Returns:
            Potential payouts breakdown
        """
        bets = self.bet_repo.get_active_bets_by_round(round_id)
        
        potential_payouts_ton = Decimal("0.0")
        potential_payouts_stars = Decimal("0.0")
        
        for bet in bets:
            if bet.currency == "TON":
                potential_payouts_ton += self.payout_calculator.calculate_payout(
                    bet.amount_ton or Decimal("0.0"), current_multiplier
                )
            else:
                potential_payouts_stars += self.payout_calculator.calculate_payout(
                    bet.amount_stars or Decimal("0.0"), current_multiplier
                )
        
        return {
            "current_multiplier": float(current_multiplier),
            "potential_payouts_ton": float(potential_payouts_ton),
            "potential_payouts_stars": float(potential_payouts_stars),
            "active_bets_count": len(bets),
        }
