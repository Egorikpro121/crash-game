"""TON transaction processing."""
from decimal import Decimal
from typing import Optional, Dict, List
from datetime import datetime
from sqlalchemy.orm import Session

from src.payments.ton.integration import TONIntegration
from src.payments.ton.wallet import TONWallet
from src.database.models.payment import Payment, PaymentStatus, PaymentMethod
from src.database.models.transaction import Transaction, TransactionType
from src.database.repositories.payment_repo import PaymentRepository
from src.database.repositories.transaction_repo import TransactionRepository
from src.database.repositories.user_repo import UserRepository


class TONTransactionProcessor:
    """Process TON transactions."""
    
    def __init__(self, db: Session):
        """
        Initialize transaction processor.
        
        Args:
            db: Database session
        """
        self.db = db
        self.ton_integration = TONIntegration()
        self.wallet = TONWallet()
        self.payment_repo = PaymentRepository(db)
        self.transaction_repo = TransactionRepository(db)
        self.user_repo = UserRepository(db)
    
    async def process_deposit(self, payment_id: int, tx_hash: str) -> bool:
        """
        Process a deposit transaction.
        
        Args:
            payment_id: Payment ID
            tx_hash: Transaction hash
        
        Returns:
            True if successful
        """
        payment = self.payment_repo.get_by_id(payment_id)
        if not payment:
            return False
        
        if payment.status != PaymentStatus.PENDING:
            return False
        
        # Validate transaction
        is_valid = await self.ton_integration.validate_transaction(
            tx_hash, payment.amount, payment.ton_address or ""
        )
        
        if not is_valid:
            self.payment_repo.update_status(
                payment_id, PaymentStatus.FAILED,
                error_message="Transaction validation failed"
            )
            return False
        
        # Update payment status
        self.payment_repo.update_status(
            payment_id, PaymentStatus.PROCESSING,
            external_tx_hash=tx_hash
        )
        
        # Add balance to user
        user = self.user_repo.get_by_id(payment.user_id)
        if user:
            if payment.currency == "TON":
                self.user_repo.update_balance(payment.user_id, amount_ton=payment.net_amount)
            elif payment.currency == "STARS":
                # TON payment but Stars currency - shouldn't happen, but handle
                self.user_repo.update_balance(payment.user_id, amount_stars=payment.net_amount)
            
            # Create transaction record
            balance_before = user.balance_ton if payment.currency == "TON" else user.balance_stars
            balance_after = balance_before + payment.net_amount
            
            self.transaction_repo.create(
                user_id=payment.user_id,
                transaction_type=TransactionType.DEPOSIT,
                currency=payment.currency,
                amount=payment.net_amount,
                balance_before=balance_before,
                balance_after=balance_after,
                description=f"TON deposit: {payment.net_amount} {payment.currency}",
                payment_id=payment_id,
            )
            
            # Update user statistics
            if payment.currency == "TON":
                self.user_repo.update_statistics(
                    payment.user_id,
                    total_deposited_ton=user.total_deposited_ton + payment.amount
                )
            else:
                self.user_repo.update_statistics(
                    payment.user_id,
                    total_deposited_stars=user.total_deposited_stars + payment.amount
                )
        
        # Complete payment
        self.payment_repo.update_status(payment_id, PaymentStatus.COMPLETED)
        
        return True
    
    async def process_withdrawal(self, payment_id: int) -> Optional[str]:
        """
        Process a withdrawal transaction.
        
        Args:
            payment_id: Payment ID
        
        Returns:
            Transaction hash or None if failed
        """
        payment = self.payment_repo.get_by_id(payment_id)
        if not payment:
            return None
        
        if payment.status != PaymentStatus.PENDING:
            return None
        
        if not payment.ton_address:
            self.payment_repo.update_status(
                payment_id, PaymentStatus.FAILED,
                error_message="No withdrawal address provided"
            )
            return None
        
        # Check user balance
        user = self.user_repo.get_by_id(payment.user_id)
        if not user:
            self.payment_repo.update_status(
                payment_id, PaymentStatus.FAILED,
                error_message="User not found"
            )
            return None
        
        balance = user.balance_ton if payment.currency == "TON" else user.balance_stars
        if balance < payment.amount:
            self.payment_repo.update_status(
                payment_id, PaymentStatus.FAILED,
                error_message="Insufficient balance"
            )
            return None
        
        # Update payment status
        self.payment_repo.update_status(payment_id, PaymentStatus.PROCESSING)
        
        # Deduct balance
        if payment.currency == "TON":
            self.user_repo.update_balance(payment.user_id, amount_ton=-payment.amount)
        else:
            self.user_repo.update_balance(payment.user_id, amount_stars=-payment.amount)
        
        # Create transaction record
        balance_before = balance
        balance_after = balance_before - payment.amount
        
        self.transaction_repo.create(
            user_id=payment.user_id,
            transaction_type=TransactionType.WITHDRAWAL,
            currency=payment.currency,
            amount=-payment.amount,
            balance_before=balance_before,
            balance_after=balance_after,
            description=f"TON withdrawal: {payment.net_amount} {payment.currency}",
            payment_id=payment_id,
        )
        
        # Send transaction
        try:
            tx_hash = await self.ton_integration.send_transaction(
                payment.ton_address,
                payment.net_amount,
                comment=f"Withdrawal for user {payment.user_id}"
            )
            
            # Update payment with transaction hash
            self.payment_repo.update_status(
                payment_id, PaymentStatus.COMPLETED,
                external_tx_hash=tx_hash
            )
            
            # Update user statistics
            if payment.currency == "TON":
                self.user_repo.update_statistics(
                    payment.user_id,
                    total_withdrawn_ton=user.total_withdrawn_ton + payment.amount
                )
            else:
                self.user_repo.update_statistics(
                    payment.user_id,
                    total_withdrawn_stars=user.total_withdrawn_stars + payment.amount
                )
            
            return tx_hash
            
        except Exception as e:
            # Refund balance on failure
            if payment.currency == "TON":
                self.user_repo.update_balance(payment.user_id, amount_ton=payment.amount)
            else:
                self.user_repo.update_balance(payment.user_id, amount_stars=payment.amount)
            
            self.payment_repo.update_status(
                payment_id, PaymentStatus.FAILED,
                error_message=str(e)
            )
            return None
    
    async def monitor_deposits(self, user_id: int, address: str):
        """
        Monitor address for deposits.
        
        Args:
            user_id: User ID
            address: Address to monitor
        """
        async def handle_deposit(tx_hash: str, amount: Decimal, from_address: str):
            # Find pending deposit payment for this user
            payments = self.payment_repo.get_user_payments(
                user_id, PaymentType.DEPOSIT
            )
            
            for payment in payments:
                if payment.status == PaymentStatus.PENDING and payment.ton_address == address:
                    # Check if amount matches
                    if abs(payment.amount - amount) < Decimal("0.001"):
                        await self.process_deposit(payment.id, tx_hash)
                        break
        
        await self.ton_integration.monitor_address(address, handle_deposit)
