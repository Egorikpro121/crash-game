"""Input validation service."""
from typing import Any, Tuple, Optional
from decimal import Decimal


class InputValidator:
    """Input validation service."""
    
    @staticmethod
    def validate_amount(amount: Any, min_amount: Decimal = Decimal("0.01")) -> Tuple[bool, Optional[str]]:
        """Validate amount."""
        try:
            amount_decimal = Decimal(str(amount))
            if amount_decimal < min_amount:
                return False, f"Amount must be at least {min_amount}"
            return True, None
        except (ValueError, TypeError):
            return False, "Invalid amount format"
    
    @staticmethod
    def validate_currency(currency: str) -> Tuple[bool, Optional[str]]:
        """Validate currency."""
        if currency not in ["TON", "STARS"]:
            return False, "Invalid currency. Must be TON or STARS"
        return True, None
