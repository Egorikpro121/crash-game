"""Bet limits system."""
from decimal import Decimal
from typing import Tuple, Optional


class BetLimits:
    """Manage bet limits."""
    
    # Minimum bet amounts
    MIN_BET_TON = Decimal("0.01")
    MIN_BET_STARS = Decimal("1.0")
    
    # Maximum bet amounts
    MAX_BET_TON = Decimal("100.0")
    MAX_BET_STARS = Decimal("10000.0")
    
    def validate_bet_amount(
        self,
        amount: Decimal,
        currency: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate bet amount against limits.
        
        Args:
            amount: Bet amount
            currency: Currency
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if amount <= 0:
            return False, "Bet amount must be positive"
        
        min_bet = self.MIN_BET_TON if currency == "TON" else self.MIN_BET_STARS
        max_bet = self.MAX_BET_TON if currency == "TON" else self.MAX_BET_STARS
        
        if amount < min_bet:
            return False, f"Minimum bet is {min_bet} {currency}"
        
        if amount > max_bet:
            return False, f"Maximum bet is {max_bet} {currency}"
        
        return True, None
    
    def get_min_bet(self, currency: str) -> Decimal:
        """
        Get minimum bet for currency.
        
        Args:
            currency: Currency
        
        Returns:
            Minimum bet amount
        """
        return self.MIN_BET_TON if currency == "TON" else self.MIN_BET_STARS
    
    def get_max_bet(self, currency: str) -> Decimal:
        """
        Get maximum bet for currency.
        
        Args:
            currency: Currency
        
        Returns:
            Maximum bet amount
        """
        return self.MAX_BET_TON if currency == "TON" else self.MAX_BET_STARS
    
    def adjust_bet_amount(
        self,
        amount: Decimal,
        currency: str
    ) -> Decimal:
        """
        Adjust bet amount to fit within limits.
        
        Args:
            amount: Bet amount
            currency: Currency
        
        Returns:
            Adjusted amount
        """
        min_bet = self.get_min_bet(currency)
        max_bet = self.get_max_bet(currency)
        
        if amount < min_bet:
            return min_bet
        if amount > max_bet:
            return max_bet
        
        return amount
