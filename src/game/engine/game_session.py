"""Game session manager."""
from decimal import Decimal
from datetime import datetime
from typing import Optional, Dict, List
from sqlalchemy.orm import Session

from src.game.engine.crash_engine import CrashEngine, RoundState
from src.game.engine.bet_manager import BetManager
from src.game.engine.balance_manager import BalanceManager
from src.database.models.game import GameRoundStatus, BetStatus
from src.database.repositories.game_repo import GameRoundRepository, BetRepository


class GameSession:
    """Manage a game session."""
    
    def __init__(self, db: Session):
        """
        Initialize game session.
        
        Args:
            db: Database session
        """
        self.db = db
        self.crash_engine = CrashEngine()
        self.bet_manager = BetManager()
        self.balance_manager = BalanceManager(db)
        self.round_repo = GameRoundRepository(db)
        self.bet_repo = BetRepository(db)
        
        # Current round ID
        self.current_round_id: Optional[int] = None
    
    def start_new_round(self, server_seed_hash: str,
                       client_seed: Optional[str] = None) -> Dict:
        """
        Start a new round.
        
        Args:
            server_seed_hash: Server seed hash
            client_seed: Optional client seed
        
        Returns:
            Round data
        """
        # Create round in database
        round_obj = self.round_repo.create(server_seed_hash, client_seed)
        self.current_round_id = round_obj.id
        
        # Start round in engine
        round_data = self.crash_engine.start_new_round(
            round_obj.id, server_seed_hash, client_seed
        )
        
        return round_data
    
    def begin_round(self):
        """Begin the round (after countdown)."""
        if not self.current_round_id:
            raise ValueError("No round started")
        
        # Begin in engine
        self.crash_engine.begin_round()
        
        # Update database
        round_obj = self.round_repo.get_by_id(self.current_round_id)
        if round_obj:
            combined_seed = self.crash_engine.current_round["combined_seed"]
            self.round_repo.start_round(self.current_round_id, combined_seed)
        
        # Activate bets
        self.bet_manager.activate_bets(self.current_round_id)
    
    def place_bet(self, user_id: int, amount: Decimal, currency: str,
                 auto_cashout: Optional[Decimal] = None) -> Dict:
        """
        Place a bet.
        
        Args:
            user_id: User ID
            amount: Bet amount
            currency: Currency
            auto_cashout: Auto cashout multiplier
        
        Returns:
            Bet data
        """
        # Check if bets can be placed
        if not self.crash_engine.can_place_bet():
            raise ValueError("Cannot place bet: round not active")
        
        # Validate bet
        balance = self.balance_manager.get_balance(user_id, currency)
        is_valid, error = self.bet_manager.validate_bet(user_id, amount, currency, balance)
        if not is_valid:
            raise ValueError(error)
        
        # Deduct balance
        self.balance_manager.deduct_balance(
            user_id, amount, currency,
            description=f"Bet: {amount} {currency}",
            round_id=self.current_round_id
        )
        
        # Place bet
        bet_data = self.bet_manager.place_bet(
            user_id, self.current_round_id, amount, currency, auto_cashout
        )
        
        # Save to database
        bet = self.bet_repo.create(
            user_id=user_id,
            round_id=self.current_round_id,
            amount_ton=amount if currency == "TON" else None,
            amount_stars=amount if currency == "STARS" else None,
            currency=currency,
            auto_cashout_multiplier=auto_cashout
        )
        
        bet_data["bet_id"] = bet.id
        
        return bet_data
    
    def cashout(self, user_id: int) -> Optional[Dict]:
        """
        Cash out user's bet.
        
        Args:
            user_id: User ID
        
        Returns:
            Cashout data or None
        """
        if not self.crash_engine.is_round_active():
            raise ValueError("Round not active")
        
        current_multiplier = self.crash_engine.get_current_multiplier()
        if current_multiplier is None:
            raise ValueError("Cannot get current multiplier")
        
        # Cash out in bet manager
        bet_data = self.bet_manager.cashout_bet(user_id, current_multiplier)
        if not bet_data:
            return None
        
        # Add balance
        payout = bet_data["payout"]
        currency = bet_data["currency"]
        self.balance_manager.add_balance(
            user_id, payout, currency,
            description=f"Cashout: {payout} {currency} at {current_multiplier}x",
            bet_id=bet_data.get("bet_id"),
            round_id=self.current_round_id
        )
        
        # Update database
        if bet_data.get("bet_id"):
            self.bet_repo.cashout_bet(
                bet_data["bet_id"],
                current_multiplier,
                payout if currency == "TON" else None,
                payout if currency == "STARS" else None
            )
        
        return bet_data
    
    def update_round(self) -> Dict:
        """
        Update round (check for crashes, auto cashouts).
        
        Returns:
            Round update data
        """
        if not self.crash_engine.is_round_active():
            return {"status": "not_active"}
        
        current_multiplier = self.crash_engine.get_current_multiplier()
        
        # Check auto cashouts
        auto_cashouts = self.bet_manager.check_auto_cashouts(current_multiplier)
        
        # Process auto cashouts
        for bet_data in auto_cashouts:
            user_id = bet_data["user_id"]
            payout = bet_data["payout"]
            currency = bet_data["currency"]
            
            self.balance_manager.add_balance(
                user_id, payout, currency,
                description=f"Auto cashout: {payout} {currency} at {bet_data['cashed_out_multiplier']}x",
                bet_id=bet_data.get("bet_id"),
                round_id=self.current_round_id
            )
            
            if bet_data.get("bet_id"):
                self.bet_repo.cashout_bet(
                    bet_data["bet_id"],
                    bet_data["cashed_out_multiplier"],
                    payout if currency == "TON" else None,
                    payout if currency == "STARS" else None
                )
        
        # Check if crashed
        if self.crash_engine.round_state == RoundState.CRASHED:
            self._process_crash()
        
        return {
            "multiplier": float(current_multiplier) if current_multiplier else None,
            "auto_cashouts": len(auto_cashouts),
            "status": self.crash_engine.round_state.value
        }
    
    def _process_crash(self):
        """Process round crash."""
        if not self.current_round_id:
            return
        
        round_data = self.crash_engine.get_round_data()
        crash_multiplier = round_data["crash_point"]
        server_seed = round_data["server_seed"]
        duration_ms = int((round_data["crash_time"] - round_data["start_time"]).total_seconds() * 1000)
        
        # Update database
        self.round_repo.crash_round(
            self.current_round_id,
            crash_multiplier,
            server_seed,
            duration_ms
        )
        
        # Crash all remaining bets
        self.bet_manager.crash_all_bets(self.current_round_id)
        
        # Update bet statuses in database
        active_bets = self.bet_repo.get_active_bets_by_round(self.current_round_id)
        for bet in active_bets:
            self.bet_repo.crash_bet(bet.id)
    
    def get_round_status(self) -> Dict:
        """Get current round status."""
        if not self.current_round_id:
            return {"status": "no_round"}
        
        round_data = self.crash_engine.get_round_data()
        if not round_data:
            return {"status": "no_round"}
        
        current_multiplier = None
        if self.crash_engine.is_round_active():
            current_multiplier = self.crash_engine.get_current_multiplier()
        
        return {
            "round_id": self.current_round_id,
            "status": round_data["status"].value,
            "multiplier": float(current_multiplier) if current_multiplier else None,
            "crash_point": float(round_data["crash_point"]) if round_data.get("crash_point") else None,
            "start_time": round_data["start_time"].isoformat() if round_data.get("start_time") else None,
        }
