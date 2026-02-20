"""Unit tests for bonus system."""
import pytest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from src.database.connection import Base
from src.database.repositories.user_repo import UserRepository
from src.database.repositories.payment_repo import PaymentRepository, PaymentType, PaymentMethod
from src.economics.bonuses import (
    FirstDepositBonus,
    DailyBonus,
    ActivityBonus,
    StreakBonus,
    VIPBonus,
    BonusManager,
)


@pytest.fixture
def db_session():
    """Create test database session."""
    engine = create_engine('sqlite:///./test_bonuses.db')
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    import os
    if os.path.exists('./test_bonuses.db'):
        os.remove('./test_bonuses.db')


@pytest.fixture
def test_user(db_session):
    """Create test user."""
    user_repo = UserRepository(db_session)
    return user_repo.create(
        telegram_user_id=111111111,
        username='testuser',
    )


def test_first_deposit_bonus_eligibility(db_session, test_user):
    """Test first deposit bonus eligibility."""
    bonus = FirstDepositBonus(db_session)
    
    # User should be eligible for first deposit
    assert bonus.is_eligible(test_user.id, "TON")
    
    # Calculate bonus
    bonus_amount = bonus.calculate_bonus(Decimal("10.0"), "TON")
    assert bonus_amount == Decimal("1.0")


def test_daily_bonus(db_session, test_user):
    """Test daily bonus."""
    bonus = DailyBonus(db_session)
    
    # Check if claimed today
    claimed = bonus.has_claimed_today(test_user.id)
    assert isinstance(claimed, bool)
    
    # Get available bonus
    amount = bonus.get_available_bonus("TON")
    assert amount > 0


def test_activity_bonus(db_session, test_user):
    """Test activity bonus."""
    bonus = ActivityBonus(db_session)
    
    # Calculate activity bonus
    bonus_amount = bonus.calculate_activity_bonus(test_user.id, "TON", period_days=1)
    assert bonus_amount >= Decimal("0.0")


def test_streak_bonus(db_session, test_user):
    """Test streak bonus."""
    bonus = StreakBonus(db_session)
    
    # Calculate streak days
    streak = bonus.calculate_streak_days(test_user.id)
    assert streak >= 0
    
    # Calculate streak bonus
    bonus_amount = bonus.calculate_streak_bonus(test_user.id, "TON")
    assert bonus_amount >= Decimal("0.0")


def test_vip_bonus(db_session, test_user):
    """Test VIP bonus."""
    bonus = VIPBonus(db_session)
    
    # Calculate VIP level
    vip_level = bonus.calculate_vip_level(test_user.id)
    assert vip_level >= 0
    assert vip_level <= 5
    
    # Calculate VIP bonus
    bonus_amount = bonus.calculate_vip_bonus(test_user.id, "TON")
    assert bonus_amount >= Decimal("0.0")


def test_bonus_manager(db_session, test_user):
    """Test bonus manager."""
    manager = BonusManager(db_session)
    
    # Get available bonuses
    bonuses = manager.get_available_bonuses(test_user.id, "TON")
    assert isinstance(bonuses, dict)
    assert "daily" in bonuses
    assert "activity" in bonuses
    assert "streak" in bonuses
    assert "vip" in bonuses
