"""Unit tests for economics core modules."""
import pytest
from decimal import Decimal

from src.economics.core.house_edge import HouseEdgeCalculator
from src.economics.core.commission_calculator import CommissionCalculator
from src.economics.core.bonus_calculator import BonusCalculator
from src.economics.core.payout_calculator import PayoutCalculator


class TestHouseEdgeCalculator:
    """Test house edge calculator."""
    
    def test_calculate_expected_multiplier(self):
        """Test expected multiplier calculation."""
        calc = HouseEdgeCalculator(Decimal("0.01"))
        result = calc.calculate_expected_multiplier(Decimal("2.0"))
        assert result == Decimal("1.98")
    
    def test_calculate_house_profit(self):
        """Test house profit calculation."""
        calc = HouseEdgeCalculator()
        profit = calc.calculate_house_profit(Decimal("100.0"), Decimal("95.0"))
        assert profit == Decimal("5.0")
    
    def test_calculate_house_profit_percentage(self):
        """Test house profit percentage."""
        calc = HouseEdgeCalculator()
        percentage = calc.calculate_house_profit_percentage(Decimal("100.0"), Decimal("95.0"))
        assert percentage == Decimal("5.0")
    
    def test_set_house_edge(self):
        """Test setting house edge."""
        calc = HouseEdgeCalculator()
        calc.set_house_edge(Decimal("0.02"))
        assert calc.get_house_edge() == Decimal("0.02")
    
    def test_invalid_house_edge(self):
        """Test invalid house edge."""
        calc = HouseEdgeCalculator()
        with pytest.raises(ValueError):
            calc.set_house_edge(Decimal("0.15"))  # Too high


class TestCommissionCalculator:
    """Test commission calculator."""
    
    def test_withdrawal_commission(self):
        """Test withdrawal commission."""
        calc = CommissionCalculator()
        commission = calc.calculate_withdrawal_commission(Decimal("100.0"), "TON")
        assert commission >= Decimal("0.1")
    
    def test_deposit_commission(self):
        """Test deposit commission (should be 0)."""
        calc = CommissionCalculator()
        commission = calc.calculate_deposit_commission(Decimal("100.0"), "TON")
        assert commission == Decimal("0.0")
    
    def test_net_withdrawal_amount(self):
        """Test net withdrawal amount."""
        calc = CommissionCalculator()
        net = calc.calculate_net_withdrawal_amount(Decimal("100.0"), "TON")
        assert net < Decimal("100.0")


class TestBonusCalculator:
    """Test bonus calculator."""
    
    def test_first_deposit_bonus(self):
        """Test first deposit bonus."""
        calc = BonusCalculator()
        bonus = calc.calculate_first_deposit_bonus(Decimal("10.0"), "TON")
        assert bonus == Decimal("1.0")
    
    def test_daily_bonus_amount(self):
        """Test daily bonus amount."""
        calc = BonusCalculator()
        bonus_ton = calc.get_daily_bonus_amount("TON")
        bonus_stars = calc.get_daily_bonus_amount("STARS")
        assert bonus_ton > 0
        assert bonus_stars > 0
    
    def test_activity_bonus(self):
        """Test activity bonus."""
        calc = BonusCalculator()
        bonus = calc.calculate_activity_bonus(10, "TON")
        assert bonus > 0


class TestPayoutCalculator:
    """Test payout calculator."""
    
    def test_calculate_payout(self):
        """Test payout calculation."""
        calc = PayoutCalculator()
        payout = calc.calculate_payout(Decimal("10.0"), Decimal("2.0"))
        assert payout == Decimal("20.0")
    
    def test_calculate_profit(self):
        """Test profit calculation."""
        calc = PayoutCalculator()
        profit = calc.calculate_profit(Decimal("10.0"), Decimal("20.0"))
        assert profit == Decimal("10.0")
    
    def test_calculate_roi(self):
        """Test ROI calculation."""
        calc = PayoutCalculator()
        roi = calc.calculate_roi(Decimal("10.0"), Decimal("20.0"))
        assert roi == Decimal("100.0")
    
    def test_calculate_total_payout(self):
        """Test total payout calculation."""
        calc = PayoutCalculator()
        bets = [(Decimal("10.0"), Decimal("2.0")), (Decimal("5.0"), Decimal("3.0"))]
        total = calc.calculate_total_payout(bets)
        assert total == Decimal("35.0")  # 20 + 15
