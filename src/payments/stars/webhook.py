"""Telegram Stars webhook handler."""
from typing import Dict, Optional, Callable
from decimal import Decimal
from datetime import datetime

from src.payments.stars.integration import StarsIntegration


class StarsWebhookHandler:
    """Handle Telegram Stars webhooks."""
    
    def __init__(self, secret_token: str):
        """
        Initialize webhook handler.
        
        Args:
            secret_token: Webhook secret token
        """
        self.stars_integration = StarsIntegration()
        self.secret_token = secret_token
        self.payment_callbacks: Dict[str, Callable] = {}
    
    def register_payment_callback(self, invoice_id: str, callback: Callable):
        """
        Register callback for payment.
        
        Args:
            invoice_id: Invoice ID
            callback: Callback function(user_id, amount)
        """
        self.payment_callbacks[invoice_id] = callback
    
    async def handle_webhook(self, data: Dict) -> Dict:
        """
        Handle webhook request.
        
        Args:
            data: Webhook data
        
        Returns:
            Response data
        """
        # Validate webhook
        if not self.stars_integration.validate_webhook(data, self.secret_token):
            return {"error": "Invalid webhook signature"}
        
        # Handle pre-checkout query
        if "pre_checkout_query" in data:
            return await self._handle_pre_checkout(data["pre_checkout_query"])
        
        # Handle successful payment
        if "message" in data and data["message"].get("successful_payment"):
            return await self._handle_successful_payment(data["message"]["successful_payment"])
        
        return {"status": "ok"}
    
    async def _handle_pre_checkout(self, query: Dict) -> Dict:
        """
        Handle pre-checkout query.
        
        Args:
            query: Pre-checkout query data
        
        Returns:
            Response
        """
        payment_id = query.get("id")
        invoice_payload = query.get("invoice_payload", "")
        
        # Extract user_id from payload
        # Format: deposit_{user_id}_{timestamp}
        parts = invoice_payload.split("_")
        if len(parts) >= 2 and parts[0] == "deposit":
            user_id = int(parts[1])
            
            # Approve payment
            await self.stars_integration.approve_payment(payment_id)
            
            return {"status": "approved"}
        
        return {"status": "rejected", "error": "Invalid payload"}
    
    async def _handle_successful_payment(self, payment: Dict) -> Dict:
        """
        Handle successful payment.
        
        Args:
            payment: Payment data
        
        Returns:
            Response
        """
        payment_id = payment.get("telegram_payment_charge_id")
        invoice_payload = payment.get("invoice_payload", "")
        amount = Decimal(payment.get("total_amount", 0)) / Decimal("100")
        
        # Extract user_id from payload
        parts = invoice_payload.split("_")
        if len(parts) >= 2 and parts[0] == "deposit":
            user_id = int(parts[1])
            
            # Call registered callback
            if invoice_payload in self.payment_callbacks:
                await self.payment_callbacks[invoice_payload](user_id, amount)
            
            return {"status": "processed", "user_id": user_id, "amount": float(amount)}
        
        return {"status": "error", "message": "Invalid payload"}
