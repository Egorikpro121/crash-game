"""Commission calculation for payments."""
from decimal import Decimal
from typing import Optional


class CommissionCalculator:
    """Calculate commissions for deposits and withdrawals."""
    
    def __init__(
        self,
        withdrawal_commission_percent: Decimal = Decimal("0.01"),  # 1%
        withdrawal_min_commission_ton: Decimal = Decimal("0.1"),
        withdrawal_min_commission_stars: Decimal = Decimal("10"),
        deposit_commission_percent: Decimal = Decimal("0.0"),  # 0% for deposits
    ):
        """
        Initialize commission calculator.
        
        Args:
            withdrawal_commission_percent: Commission percentage for withdrawals
            withdrawal_min_commission_ton: Minimum commission for TON withdrawals
            withdrawal_min_commission_stars: Minimum commission for Stars withdrawals
            deposit_commission_percent: Commission percentage for deposits (usually 0)
        """
        self.withdrawal_commission_percent = withdrawal_commission_percent
        self.withdrawal_min_commission_ton = withdrawal_min_commission_ton
        self.withdrawal_min_commission_stars = withdrawal_min_commission_stars
        self.deposit_commission_percent = deposit_commission_percent
    
    def calculate_withdrawal_commission(
        self,
        amount: Decimal,
        currency: str
    ) -> Decimal:
        """
        Calculate withdrawal commission.
        
        Args:
            amount: Withdrawal amount
            currency: Currency ("TON" or "STARS")
        
        Returns:
            Commission amount
        """
        commission = amount * self.withdrawal_commission_percent
        
        # Apply minimum commission
        min_commission = (
            self.withdrawal_min_commission_ton if currency == "TON"
            else self.withdrawal_min_commission_stars
        )
        
        return max(commission, min_commission)
    
    def calculate_deposit_commission(
        self,
        amount: Decimal,
        currency: str
    ) -> Decimal:
        """
        Calculate deposit commission (usually 0).
        
        Args:
            amount: Deposit amount
            currency: Currency
        
        Returns:
            Commission amount (usually 0)
        """
        return amount * self.deposit_commission_percent
    
    def calculate_net_withdrawal_amount(
        self,
        amount: Decimal,
        currency: str
    ) -> Decimal:
        """
        Calculate net withdrawal amount after commission.
        
        Args:
            amount: Gross withdrawal amount
            currency: Currency
        
        Returns:
            Net amount (amount - commission)
        """
        commission = self.calculate_withdrawal_commission(amount, currency)
        return amount - commission
    
    def calculate_gross_withdrawal_amount(
        self,
        net_amount: Decimal,
        currency: str
    ) -> Decimal:
        """
        Calculate gross withdrawal amount from net amount.
        
        Args:
            net_amount: Net withdrawal amount
            currency: Currency
        
        Returns:
            Gross amount (net_amount + commission)
        """
        # Reverse calculation
        min_commission = (
            self.withdrawal_min_commission_ton if currency == "TON"
            else self.withdrawal_min_commission_stars
        )
        
        # Calculate required gross amount
        if self.withdrawal_commission_percent > 0:
            # net = gross * (1 - commission_percent)
            # gross = net / (1 - commission_percent)
            gross = net_amount / (Decimal("1.0") - self.withdrawal_commission_percent)
            
            # Check if minimum commission applies
            commission = gross * self.withdrawal_commission_percent
            if commission < min_commission:
                gross = net_amount + min_commission
            
            return gross
        
        return net_amount + min_commission
