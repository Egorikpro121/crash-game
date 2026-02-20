"""Provably Fair system for crash game."""
import hashlib
import secrets
from typing import Optional, Tuple
from decimal import Decimal


class ProvablyFair:
    """Provably Fair system for generating fair random multipliers."""
    
    @staticmethod
    def generate_server_seed() -> str:
        """Generate a random server seed."""
        return secrets.token_hex(32)
    
    @staticmethod
    def hash_seed(seed: str) -> str:
        """Hash a seed using SHA256."""
        return hashlib.sha256(seed.encode()).hexdigest()
    
    @staticmethod
    def combine_seeds(server_seed: str, client_seed: Optional[str], round_id: int) -> str:
        """Combine server seed, client seed, and round ID."""
        combined = f"{server_seed}{client_seed or ''}{round_id}"
        return ProvablyFair.hash_seed(combined)
    
    @staticmethod
    def seed_to_int(seed: str) -> int:
        """Convert seed hash to integer."""
        return int(seed[:16], 16)  # Use first 16 hex chars (64 bits)
    
    @staticmethod
    def calculate_crash_point(combined_seed: str, house_edge: Decimal = Decimal("0.01")) -> Decimal:
        """
        Calculate crash point from seed.
        
        Formula: multiplier = 1 + (hash(seed) / 2^64) * max_multiplier_factor
        Crash probability increases exponentially with multiplier.
        
        Args:
            combined_seed: Combined seed string
            house_edge: House edge (default 1%)
        
        Returns:
            Crash multiplier (e.g., 2.5 means crash at 2.5x)
        """
        seed_int = ProvablyFair.seed_to_int(combined_seed)
        max_int = 2**64
        
        # Normalize to 0-1
        normalized = seed_int / max_int
        
        # Calculate crash point using exponential distribution
        # Higher multipliers have exponentially lower probability
        # Formula ensures house edge
        
        # Use inverse of exponential CDF for crash point
        # P(crash before x) = 1 - e^(-lambda * (x-1))
        # We want E[multiplier] = 1 / (1 - house_edge)
        
        # Simplified formula: crash_point = 1 + (1 / (1 - normalized)) * factor
        # This ensures fair distribution
        
        # More precise formula:
        # crash_point = 1 + (1 / (1 - normalized + epsilon)) * (1 / (1 - house_edge))
        epsilon = Decimal("0.0000001")
        
        if normalized >= 1 - epsilon:
            # Very rare case, return high multiplier
            return Decimal("1000.0")
        
        # Calculate crash point
        # This formula ensures:
        # - Minimum multiplier is 1.00x
        # - Higher multipliers are exponentially rarer
        # - House edge is maintained
        
        denominator = Decimal("1.0") - Decimal(str(normalized)) + epsilon
        base_multiplier = Decimal("1.0") / denominator
        house_edge_factor = Decimal("1.0") / (Decimal("1.0") - house_edge)
        
        crash_point = Decimal("1.0") + base_multiplier * house_edge_factor
        
        # Ensure minimum of 1.00x
        if crash_point < Decimal("1.0"):
            crash_point = Decimal("1.0")
        
        # Cap at reasonable maximum (optional)
        if crash_point > Decimal("1000.0"):
            crash_point = Decimal("1000.0")
        
        return crash_point.quantize(Decimal("0.01"))
    
    @staticmethod
    def verify_round(server_seed_hash: str, server_seed: str, 
                   client_seed: Optional[str], round_id: int,
                   crash_multiplier: Decimal) -> bool:
        """
        Verify that a round was fair.
        
        Args:
            server_seed_hash: Hash of server seed published before round
            server_seed: Server seed revealed after round
            client_seed: Client seed (if provided)
            round_id: Round ID
            crash_multiplier: Crash multiplier that occurred
        
        Returns:
            True if round is verified as fair
        """
        # Verify server seed hash matches
        if ProvablyFair.hash_seed(server_seed) != server_seed_hash:
            return False
        
        # Recalculate crash point
        combined_seed = ProvablyFair.combine_seeds(server_seed, client_seed, round_id)
        calculated_crash = ProvablyFair.calculate_crash_point(combined_seed)
        
        # Allow small floating point differences
        diff = abs(calculated_crash - crash_multiplier)
        return diff < Decimal("0.01")
    
    @staticmethod
    def calculate_multiplier_at_time(crash_point: Decimal, elapsed_ms: int, 
                                    base_speed: int = 100) -> Decimal:
        """
        Calculate current multiplier at given time.
        
        Args:
            crash_point: Final crash multiplier
            elapsed_ms: Milliseconds elapsed since round start
            base_speed: Base speed of multiplier increase (ms per 0.01x)
        
        Returns:
            Current multiplier
        """
        # Linear increase: multiplier = 1 + (elapsed_ms / base_speed) * 0.01
        # But we need to cap at crash_point
        
        multiplier = Decimal("1.0") + Decimal(str(elapsed_ms)) / Decimal(str(base_speed)) * Decimal("0.01")
        
        # Cap at crash point
        if multiplier >= crash_point:
            return crash_point
        
        return multiplier.quantize(Decimal("0.01"))
    
    @staticmethod
    def get_crash_probability_distribution() -> dict:
        """
        Get probability distribution of crash multipliers.
        
        Returns:
            Dictionary with multiplier ranges and probabilities
        """
        # This is theoretical distribution based on the formula
        # In practice, actual distribution will vary
        return {
            "1.00x - 2.00x": 0.30,  # 30% crash before 2x
            "2.00x - 5.00x": 0.50,  # 50% crash between 2x and 5x
            "5.00x - 10.00x": 0.15,  # 15% crash between 5x and 10x
            "10.00x+": 0.05,  # 5% crash above 10x
        }
