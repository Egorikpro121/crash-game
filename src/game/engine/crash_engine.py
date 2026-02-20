"""Main crash game engine."""
from decimal import Decimal
from datetime import datetime
from typing import Optional, List, Dict, Callable
from enum import Enum

from src.game.engine.provably_fair import ProvablyFair
from src.game.engine.multiplier_calculator import MultiplierCalculator
from src.database.models.game import GameRoundStatus, BetStatus


class RoundState(Enum):
    """State of a game round."""
    PENDING = "pending"
    COUNTDOWN = "countdown"
    ACTIVE = "active"
    CRASHED = "crashed"


class CrashEngine:
    """Main crash game engine."""
    
    def __init__(self, house_edge: Decimal = Decimal("0.01"), 
                 countdown_seconds: int = 5,
                 base_speed_ms: int = 100):
        """
        Initialize crash engine.
        
        Args:
            house_edge: House edge (default 1%)
            countdown_seconds: Countdown before round starts
            base_speed_ms: Base speed of multiplier increase
        """
        self.house_edge = house_edge
        self.countdown_seconds = countdown_seconds
        self.multiplier_calculator = MultiplierCalculator(base_speed_ms)
        
        # Current round state
        self.current_round: Optional[Dict] = None
        self.round_state: RoundState = RoundState.PENDING
        
        # Callbacks
        self.on_round_start: Optional[Callable] = None
        self.on_multiplier_update: Optional[Callable] = None
        self.on_round_crash: Optional[Callable] = None
    
    def start_new_round(self, round_id: int, server_seed_hash: str,
                       client_seed: Optional[str] = None) -> Dict:
        """
        Start a new game round.
        
        Args:
            round_id: Round ID
            server_seed_hash: Hash of server seed
            client_seed: Optional client seed
        
        Returns:
            Round data dictionary
        """
        # Generate server seed (in production, this should be stored securely)
        server_seed = ProvablyFair.generate_server_seed()
        
        # Verify hash matches
        if ProvablyFair.hash_seed(server_seed) != server_seed_hash:
            raise ValueError("Server seed hash mismatch")
        
        # Combine seeds
        combined_seed = ProvablyFair.combine_seeds(server_seed, client_seed, round_id)
        
        # Calculate crash point
        crash_point = ProvablyFair.calculate_crash_point(combined_seed, self.house_edge)
        
        # Create round data
        self.current_round = {
            "round_id": round_id,
            "server_seed_hash": server_seed_hash,
            "server_seed": server_seed,  # Will be revealed after crash
            "client_seed": client_seed,
            "combined_seed": combined_seed,
            "crash_point": crash_point,
            "start_time": None,
            "crash_time": None,
            "status": RoundState.COUNTDOWN,
        }
        
        self.round_state = RoundState.COUNTDOWN
        
        return self.current_round
    
    def begin_round(self) -> Dict:
        """
        Begin the actual round (after countdown).
        
        Returns:
            Updated round data
        """
        if not self.current_round:
            raise ValueError("No round started")
        
        if self.round_state != RoundState.COUNTDOWN:
            raise ValueError(f"Round not in countdown state: {self.round_state}")
        
        self.current_round["start_time"] = datetime.utcnow()
        self.current_round["status"] = RoundState.ACTIVE
        self.round_state = RoundState.ACTIVE
        
        if self.on_round_start:
            self.on_round_start(self.current_round)
        
        return self.current_round
    
    def get_current_multiplier(self) -> Optional[Decimal]:
        """
        Get current multiplier.
        
        Returns:
            Current multiplier or None if no active round
        """
        if not self.current_round or self.round_state != RoundState.ACTIVE:
            return None
        
        start_time = self.current_round["start_time"]
        crash_point = self.current_round["crash_point"]
        
        current_multiplier = self.multiplier_calculator.calculate_current_multiplier(
            crash_point, start_time
        )
        
        # Check if crashed
        if current_multiplier >= crash_point:
            self._crash_round()
            return crash_point
        
        return current_multiplier
    
    def _crash_round(self):
        """Crash the current round."""
        if not self.current_round:
            return
        
        self.current_round["crash_time"] = datetime.utcnow()
        self.current_round["status"] = RoundState.CRASHED
        self.round_state = RoundState.CRASHED
        
        if self.on_round_crash:
            self.on_round_crash(self.current_round)
    
    def crash_round_manually(self):
        """Manually crash the round (for testing)."""
        if not self.current_round:
            raise ValueError("No active round")
        
        self._crash_round()
    
    def get_round_data(self) -> Optional[Dict]:
        """Get current round data."""
        return self.current_round.copy() if self.current_round else None
    
    def is_round_active(self) -> bool:
        """Check if round is currently active."""
        return self.round_state == RoundState.ACTIVE
    
    def can_place_bet(self) -> bool:
        """Check if bets can be placed."""
        return self.round_state in [RoundState.COUNTDOWN, RoundState.ACTIVE]
    
    def get_time_until_crash(self) -> Optional[int]:
        """
        Get milliseconds until crash (approximate).
        
        Returns:
            Milliseconds until crash or None
        """
        if not self.current_round or self.round_state != RoundState.ACTIVE:
            return None
        
        start_time = self.current_round["start_time"]
        crash_point = self.current_round["crash_point"]
        
        # Calculate time needed for crash point
        multiplier_diff = crash_point - Decimal("1.0")
        ms_needed = int(multiplier_diff * Decimal("100") * Decimal("100"))  # base_speed_ms = 100
        
        elapsed_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        
        return max(0, ms_needed - elapsed_ms)
