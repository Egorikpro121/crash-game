"""Deposit limits system."""
from decimal import Decimal
from typing import Tuple, Optional


class DepositLimits:
    """Manage deposit limits."""
    
    # Minimum deposit amounts
    MIN_DEPOSIT_TON = Decimal("0.1")
    MIN_DEPOSIT_STARS = Decimal("10.0")
    
    # Maximum deposit amounts (per transaction)
    MAX_DEPOSIT_TON = Decimal("10000.0")
    MAX_DEPOSIT_STARS = Decimal("1000000.0")
    
    # Daily deposit limits
    MAX_DAILY_DEPOSIT_TON = Decimal("50000.0")
    MAX_DAILY_DEPOSIT_STARS = Decimal("5000000.0")
    
    def validate_deposit_amount(
        self,
        amount: Decimal,
        currency: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate deposit amount against limits.
        
        Args:
            amount: Deposit amount
            currency: Currency
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if amount <= 0:
            return False, "Deposit amount must be positive"
        
        min_deposit = (
            self.MIN_DEPOSIT_TON if currency == "TON"
            else self.MIN_DEPOSIT_STARS
        )
        max_deposit = (
            self.MAX_DEPOSIT_TON if currency == "TON"
            else self.MAX_DEPOSIT_STARS
        )
        
        if amount < min_deposit:
            return False, f"Minimum deposit is {min_deposit} {currency}"
        
        if amount > max_deposit:
            return False, f"Maximum deposit per transaction is {max_deposit} {currency}"
        
        return True, None
    
    def validate_daily_limit(
        self,
        daily_total: Decimal,
        amount: Decimal,
        currency: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate against daily deposit limit.
        
        Args:
            daily_total: Total deposited today
            amount: New deposit amount
            currency: Currency
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        max_daily = (
            self.MAX_DAILY_DEPOSIT_TON if currency == "TON"
            else self.MAX_DAILY_DEPOSIT_STARS
        )
        
        if daily_total + amount > max_daily:
            return False, f"Daily deposit limit exceeded. Maximum is {max_daily} {currency}"
        
        return True, None
    
    def get_min_deposit(self, currency: str) -> Decimal:
        """
        Get minimum deposit for currency.
        
        Args:
            currency: Currency
        
        Returns:
            Minimum deposit amount
        """
        return (
            self.MIN_DEPOSIT_TON if currency == "TON"
            else self.MIN_DEPOSIT_STARS
        )
    
    def get_max_deposit(self, currency: str) -> Decimal:
        """
        Get maximum deposit per transaction for currency.
        
        Args:
            currency: Currency
        
        Returns:
            Maximum deposit amount
        """
        return (
            self.MAX_DEPOSIT_TON if currency == "TON"
            else self.MAX_DEPOSIT_STARS
        )
    
    def get_max_daily_deposit(self, currency: str) -> Decimal:
        """
        Get maximum daily deposit for currency.
        
        Args:
            currency: Currency
        
        Returns:
            Maximum daily deposit amount
        """
        return (
            self.MAX_DAILY_DEPOSIT_TON if currency == "TON"
            else self.MAX_DAILY_DEPOSIT_STARS
        )
