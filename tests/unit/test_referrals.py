"""Unit tests for referral system."""
import pytest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.connection import Base
from src.database.repositories.user_repo import UserRepository
from src.economics.referrals import (
    ReferralManager,
    ReferralCalculator,
    ReferralTracker,
)


@pytest.fixture
def db_session():
    """Create test database session."""
    engine = create_engine('sqlite:///./test_referrals.db')
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    import os
    if os.path.exists('./test_referrals.db'):
        os.remove('./test_referrals.db')


@pytest.fixture
def referrer_user(db_session):
    """Create referrer user."""
    user_repo = UserRepository(db_session)
    return user_repo.create(
        telegram_user_id=222222222,
        username='referrer',
    )


@pytest.fixture
def referred_user(db_session):
    """Create referred user."""
    user_repo = UserRepository(db_session)
    return user_repo.create(
        telegram_user_id=333333333,
        username='referred',
    )


def test_create_referral_code(db_session, referrer_user):
    """Test creating referral code."""
    manager = ReferralManager(db_session)
    
    code = manager.create_referral_code(referrer_user.id)
    assert code is not None
    assert len(code) == 8
    assert code.isupper()


def test_get_referral_code(db_session, referrer_user):
    """Test getting referral code."""
    manager = ReferralManager(db_session)
    
    code = manager.get_referral_code(referrer_user.id)
    assert code is not None


def test_register_referral(db_session, referrer_user, referred_user):
    """Test registering referral."""
    manager = ReferralManager(db_session)
    
    success = manager.register_referral(referrer_user.id, referred_user.id)
    assert success
    
    # Should not register self
    success = manager.register_referral(referrer_user.id, referrer_user.id)
    assert not success


def test_referral_calculator(db_session):
    """Test referral calculator."""
    calculator = ReferralCalculator(db_session)
    
    payout = calculator.calculate_referral_payout(Decimal("100.0"), "TON")
    assert payout == Decimal("5.0")  # 5% of 100


def test_referral_tracker(db_session, referrer_user, referred_user):
    """Test referral tracker."""
    tracker = ReferralTracker(db_session)
    manager = ReferralManager(db_session)
    
    # Register referral
    manager.register_referral(referrer_user.id, referred_user.id)
    
    # Get referrals
    referrals = tracker.get_referrals(referrer_user.id)
    assert isinstance(referrals, list)
    
    # Get statistics
    stats = tracker.get_referral_statistics(referrer_user.id)
    assert isinstance(stats, dict)
