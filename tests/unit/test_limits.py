"""Unit tests for limits system."""
import pytest
from decimal import Decimal

from src.economics.limits.bet_limits import BetLimits
from src.economics.limits.withdrawal_limits import WithdrawalLimits
from src.economics.limits.deposit_limits import DepositLimits


class TestBetLimits:
    """Test bet limits."""
    
    def test_validate_min_bet_ton(self):
        """Test minimum bet validation for TON."""
        limits = BetLimits()
        is_valid, error = limits.validate_bet_amount(Decimal("0.01"), "TON")
        assert is_valid
        assert error is None
    
    def test_validate_min_bet_stars(self):
        """Test minimum bet validation for Stars."""
        limits = BetLimits()
        is_valid, error = limits.validate_bet_amount(Decimal("1.0"), "STARS")
        assert is_valid
    
    def test_validate_too_small_bet(self):
        """Test too small bet."""
        limits = BetLimits()
        is_valid, error = limits.validate_bet_amount(Decimal("0.001"), "TON")
        assert not is_valid
        assert error is not None
    
    def test_validate_max_bet(self):
        """Test maximum bet validation."""
        limits = BetLimits()
        is_valid, error = limits.validate_bet_amount(Decimal("100.0"), "TON")
        assert is_valid
    
    def test_validate_too_large_bet(self):
        """Test too large bet."""
        limits = BetLimits()
        is_valid, error = limits.validate_bet_amount(Decimal("1000.0"), "TON")
        assert not is_valid
    
    def test_get_min_bet(self):
        """Test get minimum bet."""
        limits = BetLimits()
        assert limits.get_min_bet("TON") == Decimal("0.01")
        assert limits.get_min_bet("STARS") == Decimal("1.0")
    
    def test_get_max_bet(self):
        """Test get maximum bet."""
        limits = BetLimits()
        assert limits.get_max_bet("TON") == Decimal("100.0")
        assert limits.get_max_bet("STARS") == Decimal("10000.0")


class TestWithdrawalLimits:
    """Test withdrawal limits."""
    
    def test_validate_min_withdrawal(self):
        """Test minimum withdrawal."""
        limits = WithdrawalLimits()
        is_valid, error = limits.validate_withdrawal_amount(Decimal("0.1"), "TON")
        assert is_valid
    
    def test_validate_max_withdrawal(self):
        """Test maximum withdrawal."""
        limits = WithdrawalLimits()
        is_valid, error = limits.validate_withdrawal_amount(Decimal("1000.0"), "TON")
        assert is_valid
    
    def test_validate_daily_limit(self):
        """Test daily limit validation."""
        limits = WithdrawalLimits()
        is_valid, error = limits.validate_daily_limit(Decimal("4000.0"), Decimal("1000.0"), "TON")
        assert is_valid
    
    def test_validate_daily_limit_exceeded(self):
        """Test daily limit exceeded."""
        limits = WithdrawalLimits()
        is_valid, error = limits.validate_daily_limit(Decimal("5000.0"), Decimal("100.0"), "TON")
        assert not is_valid


class TestDepositLimits:
    """Test deposit limits."""
    
    def test_validate_min_deposit(self):
        """Test minimum deposit."""
        limits = DepositLimits()
        is_valid, error = limits.validate_deposit_amount(Decimal("0.1"), "TON")
        assert is_valid
    
    def test_validate_max_deposit(self):
        """Test maximum deposit."""
        limits = DepositLimits()
        is_valid, error = limits.validate_deposit_amount(Decimal("10000.0"), "TON")
        assert is_valid
