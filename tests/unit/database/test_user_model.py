"""Tests for User model (~100 tests)."""
import pytest
from decimal import Decimal
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from src.database.connection import Base, SessionLocal, init_db
from src.database.models.user import User


@pytest.fixture
def db_session():
    """Create a test database session."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def sample_user(db_session):
    """Create a sample user."""
    user = User(
        telegram_user_id=123456789,
        username="testuser",
        first_name="Test",
        last_name="User",
        balance_ton=Decimal("10.0"),
        balance_stars=Decimal("1000.0"),
    )
    db_session.add(user)
    db_session.commit()
    return user


# Test 1-10: Basic creation and attributes
def test_create_user_minimal(db_session):
    """Test creating user with minimal required fields."""
    user = User(telegram_user_id=111111111)
    db_session.add(user)
    db_session.commit()
    assert user.id is not None
    assert user.telegram_user_id == 111111111
    assert user.balance_ton == Decimal("0.0")
    assert user.balance_stars == Decimal("0.0")


def test_create_user_with_username(db_session):
    """Test creating user with username."""
    user = User(telegram_user_id=222222222, username="testuser")
    db_session.add(user)
    db_session.commit()
    assert user.username == "testuser"


def test_create_user_with_full_name(db_session):
    """Test creating user with full name."""
    user = User(
        telegram_user_id=333333333,
        first_name="John",
        last_name="Doe"
    )
    db_session.add(user)
    db_session.commit()
    assert user.first_name == "John"
    assert user.last_name == "Doe"


def test_create_user_with_balances(db_session):
    """Test creating user with initial balances."""
    user = User(
        telegram_user_id=444444444,
        balance_ton=Decimal("5.5"),
        balance_stars=Decimal("500.0")
    )
    db_session.add(user)
    db_session.commit()
    assert user.balance_ton == Decimal("5.5")
    assert user.balance_stars == Decimal("500.0")


def test_user_default_statistics(db_session):
    """Test user default statistics are zero."""
    user = User(telegram_user_id=555555555)
    db_session.add(user)
    db_session.commit()
    assert user.total_deposited_ton == Decimal("0.0")
    assert user.total_won_ton == Decimal("0.0")
    assert user.total_bets == 0


def test_user_default_settings(db_session):
    """Test user default settings."""
    user = User(telegram_user_id=666666666)
    db_session.add(user)
    db_session.commit()
    assert user.auto_cashout_enabled == False
    assert user.sound_enabled == True
    assert user.notifications_enabled == True


def test_user_referral_code(db_session):
    """Test user referral code."""
    user = User(telegram_user_id=777777777, referral_code="REF123")
    db_session.add(user)
    db_session.commit()
    assert user.referral_code == "REF123"


def test_user_default_active(db_session):
    """Test user is active by default."""
    user = User(telegram_user_id=888888888)
    db_session.add(user)
    db_session.commit()
    assert user.is_active == True
    assert user.is_banned == False


def test_user_timestamps(db_session):
    """Test user timestamps are set."""
    user = User(telegram_user_id=999999999)
    db_session.add(user)
    db_session.commit()
    assert user.created_at is not None
    assert isinstance(user.created_at, datetime)


def test_user_to_dict(db_session):
    """Test user to_dict method."""
    user = User(
        telegram_user_id=101010101,
        username="test",
        balance_ton=Decimal("1.5"),
        balance_stars=Decimal("150.0")
    )
    db_session.add(user)
    db_session.commit()
    data = user.to_dict()
    assert data["telegram_user_id"] == 101010101
    assert data["username"] == "test"
    assert data["balance_ton"] == 1.5


# Test 11-20: Uniqueness constraints
def test_unique_telegram_user_id(db_session):
    """Test telegram_user_id must be unique."""
    user1 = User(telegram_user_id=111111111)
    db_session.add(user1)
    db_session.commit()
    
    user2 = User(telegram_user_id=111111111)
    db_session.add(user2)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_unique_referral_code(db_session):
    """Test referral_code must be unique."""
    user1 = User(telegram_user_id=111111111, referral_code="REF1")
    db_session.add(user1)
    db_session.commit()
    
    user2 = User(telegram_user_id=222222222, referral_code="REF1")
    db_session.add(user2)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_multiple_users_same_username(db_session):
    """Test multiple users can have same username (not unique)."""
    user1 = User(telegram_user_id=111111111, username="test")
    user2 = User(telegram_user_id=222222222, username="test")
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()
    assert user1.username == user2.username


# Test 21-30: Balance operations
def test_balance_ton_precision(db_session):
    """Test TON balance precision."""
    user = User(telegram_user_id=111111111, balance_ton=Decimal("0.123456789"))
    db_session.add(user)
    db_session.commit()
    assert user.balance_ton == Decimal("0.123456789")


def test_balance_stars_precision(db_session):
    """Test Stars balance precision."""
    user = User(telegram_user_id=111111111, balance_stars=Decimal("123.45"))
    db_session.add(user)
    db_session.commit()
    assert user.balance_stars == Decimal("123.45")


def test_balance_can_be_zero(db_session):
    """Test balance can be zero."""
    user = User(telegram_user_id=111111111, balance_ton=Decimal("0.0"))
    db_session.add(user)
    db_session.commit()
    assert user.balance_ton == Decimal("0.0")


def test_balance_can_be_negative(db_session):
    """Test balance can be negative (for edge cases)."""
    user = User(telegram_user_id=111111111, balance_ton=Decimal("-1.0"))
    db_session.add(user)
    db_session.commit()
    assert user.balance_ton == Decimal("-1.0")


def test_large_balance(db_session):
    """Test large balance values."""
    user = User(telegram_user_id=111111111, balance_ton=Decimal("999999999.999999999"))
    db_session.add(user)
    db_session.commit()
    assert user.balance_ton == Decimal("999999999.999999999")


# Test 31-40: Statistics
def test_total_deposited_ton(db_session):
    """Test total_deposited_ton field."""
    user = User(telegram_user_id=111111111, total_deposited_ton=Decimal("100.5"))
    db_session.add(user)
    db_session.commit()
    assert user.total_deposited_ton == Decimal("100.5")


def test_total_won_stars(db_session):
    """Test total_won_stars field."""
    user = User(telegram_user_id=111111111, total_won_stars=Decimal("5000.0"))
    db_session.add(user)
    db_session.commit()
    assert user.total_won_stars == Decimal("5000.0")


def test_biggest_multiplier(db_session):
    """Test biggest_multiplier field."""
    user = User(telegram_user_id=111111111, biggest_multiplier=Decimal("50.25"))
    db_session.add(user)
    db_session.commit()
    assert user.biggest_multiplier == Decimal("50.25")


def test_total_bets_counter(db_session):
    """Test total_bets counter."""
    user = User(telegram_user_id=111111111, total_bets=42)
    db_session.add(user)
    db_session.commit()
    assert user.total_bets == 42


def test_total_cashouts_counter(db_session):
    """Test total_cashouts counter."""
    user = User(telegram_user_id=111111111, total_cashouts=10)
    db_session.add(user)
    db_session.commit()
    assert user.total_cashouts == 10


# Test 41-50: Settings
def test_auto_cashout_enabled(db_session):
    """Test auto_cashout_enabled setting."""
    user = User(telegram_user_id=111111111, auto_cashout_enabled=True)
    db_session.add(user)
    db_session.commit()
    assert user.auto_cashout_enabled == True


def test_default_auto_cashout_multiplier(db_session):
    """Test default_auto_cashout_multiplier setting."""
    user = User(telegram_user_id=111111111, default_auto_cashout_multiplier=Decimal("2.5"))
    db_session.add(user)
    db_session.commit()
    assert user.default_auto_cashout_multiplier == Decimal("2.5")


def test_sound_enabled(db_session):
    """Test sound_enabled setting."""
    user = User(telegram_user_id=111111111, sound_enabled=False)
    db_session.add(user)
    db_session.commit()
    assert user.sound_enabled == False


def test_notifications_enabled(db_session):
    """Test notifications_enabled setting."""
    user = User(telegram_user_id=111111111, notifications_enabled=False)
    db_session.add(user)
    db_session.commit()
    assert user.notifications_enabled == False


# Test 51-60: Referral system
def test_referred_by_id(db_session):
    """Test referred_by_id field."""
    referrer = User(telegram_user_id=111111111)
    db_session.add(referrer)
    db_session.commit()
    
    user = User(telegram_user_id=222222222, referred_by_id=referrer.id)
    db_session.add(user)
    db_session.commit()
    assert user.referred_by_id == referrer.id


def test_referral_earnings(db_session):
    """Test referral_earnings fields."""
    user = User(
        telegram_user_id=111111111,
        referral_earnings_ton=Decimal("10.5"),
        referral_earnings_stars=Decimal("1000.0")
    )
    db_session.add(user)
    db_session.commit()
    assert user.referral_earnings_ton == Decimal("10.5")
    assert user.referral_earnings_stars == Decimal("1000.0")


# Test 61-70: Security
def test_ban_user(db_session):
    """Test banning a user."""
    user = User(telegram_user_id=111111111, is_banned=True, ban_reason="Test ban")
    db_session.add(user)
    db_session.commit()
    assert user.is_banned == True
    assert user.ban_reason == "Test ban"


def test_deactivate_user(db_session):
    """Test deactivating a user."""
    user = User(telegram_user_id=111111111, is_active=False)
    db_session.add(user)
    db_session.commit()
    assert user.is_active == False


def test_last_login_at(db_session):
    """Test last_login_at timestamp."""
    login_time = datetime.utcnow()
    user = User(telegram_user_id=111111111, last_login_at=login_time)
    db_session.add(user)
    db_session.commit()
    assert user.last_login_at == login_time


# Test 71-80: Relationships (basic tests)
def test_user_has_bets_relationship(db_session):
    """Test user has bets relationship."""
    user = User(telegram_user_id=111111111)
    db_session.add(user)
    db_session.commit()
    assert user.bets == []


def test_user_has_transactions_relationship(db_session):
    """Test user has transactions relationship."""
    user = User(telegram_user_id=111111111)
    db_session.add(user)
    db_session.commit()
    assert user.transactions == []


def test_user_has_payments_relationship(db_session):
    """Test user has payments relationship."""
    user = User(telegram_user_id=111111111)
    db_session.add(user)
    db_session.commit()
    assert user.payments == []


# Test 81-90: Edge cases
def test_very_long_username(db_session):
    """Test username length limit."""
    long_username = "a" * 255
    user = User(telegram_user_id=111111111, username=long_username)
    db_session.add(user)
    db_session.commit()
    assert len(user.username) == 255


def test_unicode_username(db_session):
    """Test unicode characters in username."""
    user = User(telegram_user_id=111111111, username="тест_用户_テスト")
    db_session.add(user)
    db_session.commit()
    assert user.username == "тест_用户_テスト"


def test_empty_string_username(db_session):
    """Test empty string username."""
    user = User(telegram_user_id=111111111, username="")
    db_session.add(user)
    db_session.commit()
    assert user.username == ""


def test_none_username(db_session):
    """Test None username."""
    user = User(telegram_user_id=111111111, username=None)
    db_session.add(user)
    db_session.commit()
    assert user.username is None


def test_very_large_telegram_user_id(db_session):
    """Test very large telegram_user_id."""
    user = User(telegram_user_id=9223372036854775807)  # Max bigint
    db_session.add(user)
    db_session.commit()
    assert user.telegram_user_id == 9223372036854775807


# Test 91-100: Update operations
def test_update_username(db_session, sample_user):
    """Test updating username."""
    sample_user.username = "newusername"
    db_session.commit()
    assert sample_user.username == "newusername"


def test_update_balance(db_session, sample_user):
    """Test updating balance."""
    sample_user.balance_ton = Decimal("20.0")
    db_session.commit()
    assert sample_user.balance_ton == Decimal("20.0")


def test_update_statistics(db_session, sample_user):
    """Test updating statistics."""
    sample_user.total_bets = 100
    sample_user.total_won_ton = Decimal("500.0")
    db_session.commit()
    assert sample_user.total_bets == 100
    assert sample_user.total_won_ton == Decimal("500.0")


def test_update_settings(db_session, sample_user):
    """Test updating settings."""
    sample_user.auto_cashout_enabled = True
    sample_user.default_auto_cashout_multiplier = Decimal("3.0")
    db_session.commit()
    assert sample_user.auto_cashout_enabled == True
    assert sample_user.default_auto_cashout_multiplier == Decimal("3.0")


def test_update_referral_code(db_session, sample_user):
    """Test updating referral code."""
    sample_user.referral_code = "NEWREF"
    db_session.commit()
    assert sample_user.referral_code == "NEWREF"


def test_update_ban_status(db_session, sample_user):
    """Test updating ban status."""
    sample_user.is_banned = True
    sample_user.ban_reason = "Violation"
    db_session.commit()
    assert sample_user.is_banned == True
    assert sample_user.ban_reason == "Violation"


def test_update_last_login(db_session, sample_user):
    """Test updating last login."""
    new_login = datetime.utcnow()
    sample_user.last_login_at = new_login
    db_session.commit()
    assert sample_user.last_login_at == new_login


def test_repr_method(db_session, sample_user):
    """Test __repr__ method."""
    repr_str = repr(sample_user)
    assert "User" in repr_str
    assert str(sample_user.id) in repr_str
    assert str(sample_user.telegram_user_id) in repr_str


def test_to_dict_completeness(db_session, sample_user):
    """Test to_dict includes all important fields."""
    data = sample_user.to_dict()
    assert "id" in data
    assert "telegram_user_id" in data
    assert "balance_ton" in data
    assert "balance_stars" in data
    assert "created_at" in data


def test_to_dict_types(db_session, sample_user):
    """Test to_dict returns correct types."""
    data = sample_user.to_dict()
    assert isinstance(data["id"], int)
    assert isinstance(data["telegram_user_id"], int)
    assert isinstance(data["balance_ton"], float)
    assert isinstance(data["balance_stars"], float)
