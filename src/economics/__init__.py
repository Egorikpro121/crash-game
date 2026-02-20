"""Economics module."""
from src.economics.core import (
    HouseEdgeCalculator,
    CommissionCalculator,
    BonusCalculator,
    PayoutCalculator,
    ProfitTracker,
)
from src.economics.bonuses import (
    FirstDepositBonus,
    DailyBonus,
    ActivityBonus,
    StreakBonus,
    VIPBonus,
    BonusManager,
    BonusValidator,
    BonusHistory,
)
from src.economics.referrals import (
    ReferralManager,
    ReferralCalculator,
    ReferralTracker,
    ReferralPayout,
    ReferralStatistics,
    ReferralValidator,
)
from src.economics.commissions import (
    WithdrawalCommission,
    DepositCommission,
    CommissionCalculator,
    CommissionTracker,
)
from src.economics.limits import (
    BetLimits,
    WithdrawalLimits,
    DepositLimits,
    LimitsValidator,
    LimitsManager,
)
from src.economics.game import (
    MultiplierDistribution,
    CrashProbability,
    RoundEconomics,
    PayoutEconomics,
    HouseProfit,
)
from src.economics.analytics import (
    RevenueTracker,
    ProfitAnalyzer,
    UserLifetimeValue,
    GameStatistics,
    FinancialReports,
)

__all__ = [
    # Core
    "HouseEdgeCalculator",
    "CommissionCalculator",
    "BonusCalculator",
    "PayoutCalculator",
    "ProfitTracker",
    # Bonuses
    "FirstDepositBonus",
    "DailyBonus",
    "ActivityBonus",
    "StreakBonus",
    "VIPBonus",
    "BonusManager",
    "BonusValidator",
    "BonusHistory",
    # Referrals
    "ReferralManager",
    "ReferralCalculator",
    "ReferralTracker",
    "ReferralPayout",
    "ReferralStatistics",
    "ReferralValidator",
    # Commissions
    "WithdrawalCommission",
    "DepositCommission",
    "CommissionTracker",
    # Limits
    "BetLimits",
    "WithdrawalLimits",
    "DepositLimits",
    "LimitsValidator",
    "LimitsManager",
    # Game
    "MultiplierDistribution",
    "CrashProbability",
    "RoundEconomics",
    "PayoutEconomics",
    "HouseProfit",
    # Analytics
    "RevenueTracker",
    "ProfitAnalyzer",
    "UserLifetimeValue",
    "GameStatistics",
    "FinancialReports",
]
