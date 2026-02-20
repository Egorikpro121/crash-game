"""Withdrawal limits system."""
from decimal import Decimal
from typing import Tuple, Optional


class WithdrawalLimits:
    """Manage withdrawal limits."""
    
    # Minimum withdrawal amounts
    MIN_WITHDRAWAL_TON = Decimal("0.1")
    MIN_WITHDRAWAL_STARS = Decimal("10.0")
    
    # Maximum withdrawal amounts (per transaction)
    MAX_WITHDRAWAL_TON = Decimal("1000.0")
    MAX_WITHDRAWAL_STARS = Decimal("100000.0")
    
    # Daily withdrawal limits
    MAX_DAILY_WITHDRAWAL_TON = Decimal("5000.0")
    MAX_DAILY_WITHDRAWAL_STARS = Decimal("500000.0")
    
    def validate_withdrawal_amount(
        self,
        amount: Decimal,
        currency: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate withdrawal amount against limits.
        
        Args:
            amount: Withdrawal amount
            currency: Currency
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if amount <= 0:
            return False, "Withdrawal amount must be positive"
        
        min_withdrawal = (
            self.MIN_WITHDRAWAL_TON if currency == "TON"
            else self.MIN_WITHDRAWAL_STARS
        )
        max_withdrawal = (
            self.MAX_WITHDRAWAL_TON if currency == "TON"
            else self.MAX_WITHDRAWAL_STARS
        )
        
        if amount < min_withdrawal:
            return False, f"Minimum withdrawal is {min_withdrawal} {currency}"
        
        if amount > max_withdrawal:
            return False, f"Maximum withdrawal per transaction is {max_withdrawal} {currency}"
        
        return True, None
    
    def validate_daily_limit(
        self,
        daily_total: Decimal,
        amount: Decimal,
        currency: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate against daily withdrawal limit.
        
        Args:
            daily_total: Total withdrawn today
            amount: New withdrawal amount
            currency: Currency
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        max_daily = (
            self.MAX_DAILY_WITHDRAWAL_TON if currency == "TON"
            else self.MAX_DAILY_WITHDRAWAL_STARS
        )
        
        if daily_total + amount > max_daily:
            return False, f"Daily withdrawal limit exceeded. Maximum is {max_daily} {currency}"
        
        return True, None
    
    def get_min_withdrawal(self, currency: str) -> Decimal:
        """
        Get minimum withdrawal for currency.
        
        Args:
            currency: Currency
        
        Returns:
            Minimum withdrawal amount
        """
        return (
            self.MIN_WITHDRAWAL_TON if currency == "TON"
            else self.MIN_WITHDRAWAL_STARS
        )
    
    def get_max_withdrawal(self, currency: str) -> Decimal:
        """
        Get maximum withdrawal per transaction for currency.
        
        Args:
            currency: Currency
        
        Returns:
            Maximum withdrawal amount
        """
        return (
            self.MAX_WITHDRAWAL_TON if currency == "TON"
            else self.MAX_WITHDRAWAL_STARS
        )
    
    def get_max_daily_withdrawal(self, currency: str) -> Decimal:
        """
        Get maximum daily withdrawal for currency.
        
        Args:
            currency: Currency
        
        Returns:
            Maximum daily withdrawal amount
        """
        return (
            self.MAX_DAILY_WITHDRAWAL_TON if currency == "TON"
            else self.MAX_DAILY_WITHDRAWAL_STARS
        )
