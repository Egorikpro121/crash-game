"""Bonus system module."""
from src.economics.bonuses.first_deposit import FirstDepositBonus
from src.economics.bonuses.daily_bonus import DailyBonus
from src.economics.bonuses.activity_bonus import ActivityBonus
from src.economics.bonuses.streak_bonus import StreakBonus
from src.economics.bonuses.vip_bonus import VIPBonus
from src.economics.bonuses.bonus_manager import BonusManager
from src.economics.bonuses.bonus_validator import BonusValidator
from src.economics.bonuses.bonus_history import BonusHistory

__all__ = [
    "FirstDepositBonus",
    "DailyBonus",
    "ActivityBonus",
    "StreakBonus",
    "VIPBonus",
    "BonusManager",
    "BonusValidator",
    "BonusHistory",
]
