"""Telegram Stars payment validation."""
from typing import Dict, Optional
from decimal import Decimal
import hmac
import hashlib


class StarsPaymentValidator:
    """Validate Telegram Stars payments."""
    
    @staticmethod
    def validate_payment_data(data: Dict) -> tuple[bool, Optional[str]]:
        """
        Validate payment data structure.
        
        Args:
            data: Payment data
        
        Returns:
            (is_valid, error_message)
        """
        if not isinstance(data, dict):
            return False, "Invalid data type"
        
        # Check required fields for pre-checkout
        if "pre_checkout_query" in data:
            query = data["pre_checkout_query"]
            if "id" not in query:
                return False, "Missing payment ID"
            if "from" not in query:
                return False, "Missing user data"
            if "total_amount" not in query:
                return False, "Missing amount"
            if "currency" not in query:
                return False, "Missing currency"
            
            # Check currency is Stars
            if query.get("currency") != "XTR":
                return False, "Invalid currency (must be XTR)"
        
        # Check required fields for successful payment
        if "message" in data and "successful_payment" in data["message"]:
            payment = data["message"]["successful_payment"]
            if "telegram_payment_charge_id" not in payment:
                return False, "Missing payment charge ID"
            if "total_amount" not in payment:
                return False, "Missing amount"
            if "currency" not in payment:
                return False, "Missing currency"
            
            if payment.get("currency") != "XTR":
                return False, "Invalid currency (must be XTR)"
        
        return True, None
    
    @staticmethod
    def extract_amount(data: Dict) -> Optional[Decimal]:
        """
        Extract amount from payment data.
        
        Args:
            data: Payment data
        
        Returns:
            Amount in Stars or None
        """
        if "pre_checkout_query" in data:
            amount_cents = data["pre_checkout_query"].get("total_amount", 0)
            return Decimal(amount_cents) / Decimal("100")
        
        if "message" in data and "successful_payment" in data["message"]:
            amount_cents = data["message"]["successful_payment"].get("total_amount", 0)
            return Decimal(amount_cents) / Decimal("100")
        
        return None
    
    @staticmethod
    def extract_user_id(data: Dict) -> Optional[int]:
        """
        Extract user ID from payment data.
        
        Args:
            data: Payment data
        
        Returns:
            User ID or None
        """
        if "pre_checkout_query" in data:
            return data["pre_checkout_query"].get("from", {}).get("id")
        
        if "message" in data:
            return data["message"].get("from", {}).get("id")
        
        return None
    
    @staticmethod
    def extract_invoice_payload(data: Dict) -> Optional[str]:
        """
        Extract invoice payload from payment data.
        
        Args:
            data: Payment data
        
        Returns:
            Invoice payload or None
        """
        if "pre_checkout_query" in data:
            return data["pre_checkout_query"].get("invoice_payload")
        
        if "message" in data and "successful_payment" in data["message"]:
            return data["message"]["successful_payment"].get("invoice_payload")
        
        return None
    
    @staticmethod
    def validate_amount_range(amount: Decimal, min_amount: Decimal = Decimal("1.0"),
                            max_amount: Decimal = Decimal("10000.0")) -> tuple[bool, Optional[str]]:
        """
        Validate amount is in acceptable range.
        
        Args:
            amount: Amount to validate
            min_amount: Minimum amount
            max_amount: Maximum amount
        
        Returns:
            (is_valid, error_message)
        """
        if amount < min_amount:
            return False, f"Amount too small (minimum {min_amount} Stars)"
        
        if amount > max_amount:
            return False, f"Amount too large (maximum {max_amount} Stars)"
        
        return True, None
