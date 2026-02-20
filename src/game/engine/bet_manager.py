"""Bet manager for crash game."""
from decimal import Decimal
from typing import List, Dict, Optional
from datetime import datetime

from src.database.models.game import BetStatus


class BetManager:
    """Manage bets for crash game."""
    
    def __init__(self, min_bet_ton: Decimal = Decimal("0.01"),
                 max_bet_ton: Decimal = Decimal("100.0"),
                 min_bet_stars: Decimal = Decimal("1.0"),
                 max_bet_stars: Decimal = Decimal("10000.0")):
        """
        Initialize bet manager.
        
        Args:
            min_bet_ton: Minimum bet in TON
            max_bet_ton: Maximum bet in TON
            min_bet_stars: Minimum bet in Stars
            max_bet_stars: Maximum bet in Stars
        """
        self.min_bet_ton = min_bet_ton
        self.max_bet_ton = max_bet_ton
        self.min_bet_stars = min_bet_stars
        self.max_bet_stars = max_bet_stars
        
        # Active bets: {user_id: [bet_dict, ...]}
        self.active_bets: Dict[int, List[Dict]] = {}
    
    def validate_bet(self, user_id: int, amount: Decimal, currency: str,
                    user_balance: Decimal) -> tuple[bool, Optional[str]]:
        """
        Validate a bet.
        
        Args:
            user_id: User ID
            amount: Bet amount
            currency: Currency ("TON" or "STARS")
            user_balance: User's current balance
        
        Returns:
            (is_valid, error_message)
        """
        # Check minimum bet
        if currency == "TON":
            if amount < self.min_bet_ton:
                return False, f"Minimum bet is {self.min_bet_ton} TON"
            if amount > self.max_bet_ton:
                return False, f"Maximum bet is {self.max_bet_ton} TON"
        elif currency == "STARS":
            if amount < self.min_bet_stars:
                return False, f"Minimum bet is {self.min_bet_stars} Stars"
            if amount > self.max_bet_stars:
                return False, f"Maximum bet is {self.max_bet_stars} Stars"
        else:
            return False, f"Invalid currency: {currency}"
        
        # Check balance
        if amount > user_balance:
            return False, "Insufficient balance"
        
        # Check if user already has active bet in this round
        if user_id in self.active_bets and len(self.active_bets[user_id]) > 0:
            return False, "You already have an active bet in this round"
        
        return True, None
    
    def place_bet(self, user_id: int, round_id: int, amount: Decimal,
                 currency: str, auto_cashout: Optional[Decimal] = None) -> Dict:
        """
        Place a bet.
        
        Args:
            user_id: User ID
            round_id: Round ID
            amount: Bet amount
            currency: Currency
            auto_cashout: Auto cashout multiplier (optional)
        
        Returns:
            Bet data dictionary
        """
        bet_data = {
            "user_id": user_id,
            "round_id": round_id,
            "amount": amount,
            "currency": currency,
            "auto_cashout_multiplier": auto_cashout,
            "status": BetStatus.PENDING,
            "placed_at": datetime.utcnow(),
            "cashed_out": False,
            "cashed_out_multiplier": None,
            "payout": None,
        }
        
        if user_id not in self.active_bets:
            self.active_bets[user_id] = []
        
        self.active_bets[user_id].append(bet_data)
        
        return bet_data
    
    def activate_bets(self, round_id: int):
        """Activate all pending bets for a round."""
        for user_id, bets in self.active_bets.items():
            for bet in bets:
                if bet["round_id"] == round_id and bet["status"] == BetStatus.PENDING:
                    bet["status"] = BetStatus.ACTIVE
    
    def check_auto_cashouts(self, current_multiplier: Decimal) -> List[Dict]:
        """
        Check and process auto cashouts.
        
        Args:
            current_multiplier: Current multiplier
        
        Returns:
            List of cashed out bets
        """
        cashed_out = []
        
        for user_id, bets in list(self.active_bets.items()):
            for bet in bets[:]:  # Copy list to modify during iteration
                if bet["status"] != BetStatus.ACTIVE:
                    continue
                
                auto_cashout = bet.get("auto_cashout_multiplier")
                if auto_cashout and current_multiplier >= auto_cashout:
                    bet["cashed_out"] = True
                    bet["cashed_out_multiplier"] = current_multiplier
                    bet["payout"] = bet["amount"] * current_multiplier
                    bet["status"] = BetStatus.CASHED_OUT
                    cashed_out.append(bet)
                    self.active_bets[user_id].remove(bet)
        
        return cashed_out
    
    def cashout_bet(self, user_id: int, current_multiplier: Decimal) -> Optional[Dict]:
        """
        Cash out a user's bet.
        
        Args:
            user_id: User ID
            current_multiplier: Current multiplier
        
        Returns:
            Cashed out bet or None if no active bet
        """
        if user_id not in self.active_bets:
            return None
        
        bets = self.active_bets[user_id]
        if not bets:
            return None
        
        # Find active bet
        active_bet = None
        for bet in bets:
            if bet["status"] == BetStatus.ACTIVE:
                active_bet = bet
                break
        
        if not active_bet:
            return None
        
        # Cash out
        active_bet["cashed_out"] = True
        active_bet["cashed_out_multiplier"] = current_multiplier
        active_bet["payout"] = active_bet["amount"] * current_multiplier
        active_bet["status"] = BetStatus.CASHED_OUT
        
        # Remove from active bets
        self.active_bets[user_id].remove(active_bet)
        
        return active_bet
    
    def crash_all_bets(self, round_id: int):
        """Mark all active bets as crashed."""
        for user_id, bets in self.active_bets.items():
            for bet in bets[:]:
                if bet["round_id"] == round_id and bet["status"] == BetStatus.ACTIVE:
                    bet["status"] = BetStatus.CRASHED
                    self.active_bets[user_id].remove(bet)
    
    def get_active_bets(self, round_id: Optional[int] = None) -> List[Dict]:
        """
        Get all active bets.
        
        Args:
            round_id: Optional round ID filter
        
        Returns:
            List of active bets
        """
        all_bets = []
        for bets in self.active_bets.values():
            for bet in bets:
                if bet["status"] == BetStatus.ACTIVE:
                    if round_id is None or bet["round_id"] == round_id:
                        all_bets.append(bet)
        return all_bets
    
    def get_user_bet(self, user_id: int, round_id: int) -> Optional[Dict]:
        """Get user's bet for a round."""
        if user_id not in self.active_bets:
            return None
        
        for bet in self.active_bets[user_id]:
            if bet["round_id"] == round_id:
                return bet
        
        return None
    
    def clear_round_bets(self, round_id: int):
        """Clear all bets for a round."""
        for user_id in list(self.active_bets.keys()):
            self.active_bets[user_id] = [
                bet for bet in self.active_bets[user_id]
                if bet["round_id"] != round_id
            ]
            if not self.active_bets[user_id]:
                del self.active_bets[user_id]
