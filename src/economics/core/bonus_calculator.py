"""Bonus calculation system."""
from decimal import Decimal
from typing import Optional, Dict
from datetime import datetime, timedelta


class BonusCalculator:
    """Calculate bonuses for users."""
    
    def __init__(
        self,
        first_deposit_bonus_percent: Decimal = Decimal("0.10"),  # 10%
        daily_bonus_amount_ton: Decimal = Decimal("0.01"),
        daily_bonus_amount_stars: Decimal = Decimal("1.0"),
    ):
        """
        Initialize bonus calculator.
        
        Args:
            first_deposit_bonus_percent: Bonus percentage for first deposit
            daily_bonus_amount_ton: Daily bonus amount in TON
            daily_bonus_amount_stars: Daily bonus amount in Stars
        """
        self.first_deposit_bonus_percent = first_deposit_bonus_percent
        self.daily_bonus_amount_ton = daily_bonus_amount_ton
        self.daily_bonus_amount_stars = daily_bonus_amount_stars
    
    def calculate_first_deposit_bonus(
        self,
        deposit_amount: Decimal,
        currency: str
    ) -> Decimal:
        """
        Calculate first deposit bonus.
        
        Args:
            deposit_amount: Deposit amount
            currency: Currency
        
        Returns:
            Bonus amount
        """
        return deposit_amount * self.first_deposit_bonus_percent
    
    def get_daily_bonus_amount(self, currency: str) -> Decimal:
        """
        Get daily bonus amount.
        
        Args:
            currency: Currency
        
        Returns:
            Daily bonus amount
        """
        return (
            self.daily_bonus_amount_ton if currency == "TON"
            else self.daily_bonus_amount_stars
        )
    
    def calculate_activity_bonus(
        self,
        bets_count: int,
        currency: str
    ) -> Decimal:
        """
        Calculate activity bonus based on number of bets.
        
        Args:
            bets_count: Number of bets made
            currency: Currency
        
        Returns:
            Activity bonus amount
        """
        # Example: 0.001 TON per bet, max 0.1 TON
        base_bonus = (
            Decimal("0.001") if currency == "TON"
            else Decimal("0.1")
        )
        max_bonus = (
            Decimal("0.1") if currency == "TON"
            else Decimal("10")
        )
        
        bonus = base_bonus * Decimal(bets_count)
        return min(bonus, max_bonus)
    
    def calculate_streak_bonus(
        self,
        streak_days: int,
        currency: str
    ) -> Decimal:
        """
        Calculate streak bonus for consecutive days.
        
        Args:
            streak_days: Number of consecutive days
            currency: Currency
        
        Returns:
            Streak bonus amount
        """
        # Example: 0.01 TON per day of streak, max 0.5 TON
        base_bonus = (
            Decimal("0.01") if currency == "TON"
            else Decimal("1")
        )
        max_bonus = (
            Decimal("0.5") if currency == "TON"
            else Decimal("50")
        )
        
        bonus = base_bonus * Decimal(streak_days)
        return min(bonus, max_bonus)
    
    def calculate_vip_bonus(
        self,
        vip_level: int,
        currency: str
    ) -> Decimal:
        """
        Calculate VIP bonus based on VIP level.
        
        Args:
            vip_level: VIP level (1-5)
            currency: Currency
        
        Returns:
            VIP bonus amount
        """
        vip_multipliers = {
            1: Decimal("1.0"),
            2: Decimal("1.5"),
            3: Decimal("2.0"),
            4: Decimal("3.0"),
            5: Decimal("5.0"),
        }
        
        base_bonus = (
            Decimal("0.1") if currency == "TON"
            else Decimal("10")
        )
        
        multiplier = vip_multipliers.get(vip_level, Decimal("1.0"))
        return base_bonus * multiplier
