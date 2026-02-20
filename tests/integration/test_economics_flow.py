"""Integration tests for economics flow."""
import pytest
from decimal import Decimal
from sqlalchemy.orm import Session

from src.database.connection import get_db, Base, engine
from src.database.repositories.user_repo import UserRepository
from src.database.repositories.payment_repo import PaymentRepository, PaymentType, PaymentMethod
from src.economics.bonuses import BonusManager
from src.economics.referrals import ReferralManager
from src.economics.commissions import CommissionCalculator
from src.economics.limits import LimitsValidator


@pytest.fixture
def db_session():
    """Create test database session."""
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    yield db
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(db_session: Session):
    """Create test user."""
    user_repo = UserRepository(db_session)
    user = user_repo.create(
        telegram_user_id=123456789,
        username="testuser",
    )
    return user


def test_first_deposit_bonus_flow(db_session: Session, test_user):
    """Test first deposit bonus flow."""
    bonus_manager = BonusManager(db_session)
    payment_repo = PaymentRepository(db_session)
    
    # Create deposit
    deposit = payment_repo.create_deposit(
        user_id=test_user.id,
        amount=Decimal("10.0"),
        currency="TON",
        payment_method=PaymentMethod.TON,
    )
    
    # Apply first deposit bonus
    bonus_amount = bonus_manager.apply_first_deposit_bonus(
        user_id=test_user.id,
        deposit_amount=Decimal("10.0"),
        currency="TON",
        payment_id=deposit.id,
    )
    
    assert bonus_amount > 0
    assert bonus_amount == Decimal("1.0")  # 10% of 10 TON


def test_referral_flow(db_session: Session):
    """Test referral flow."""
    user_repo = UserRepository(db_session)
    referral_manager = ReferralManager(db_session)
    
    # Create referrer
    referrer = user_repo.create(telegram_user_id=111111111, username="referrer")
    
    # Create referred user
    referred = user_repo.create(telegram_user_id=222222222, username="referred")
    
    # Register referral
    code = referral_manager.create_referral_code(referrer.id)
    success = referral_manager.register_referral(referrer.id, referred.id)
    
    assert success
    assert code is not None


def test_commission_calculation(db_session: Session):
    """Test commission calculation."""
    calculator = CommissionCalculator(db_session)
    
    # Test withdrawal commission
    commission = calculator.calculate_withdrawal_commission(
        amount=Decimal("100.0"),
        currency="TON"
    )
    
    assert commission > 0
    assert commission == Decimal("1.0")  # 1% of 100 TON


def test_limits_validation(db_session: Session, test_user):
    """Test limits validation."""
    validator = LimitsValidator(db_session)
    
    # Test bet validation
    is_valid, error = validator.validate_bet(
        amount=Decimal("0.01"),
        currency="TON",
        user_id=test_user.id
    )
    
    assert is_valid
    assert error is None
    
    # Test invalid bet (too small)
    is_valid, error = validator.validate_bet(
        amount=Decimal("0.001"),
        currency="TON",
        user_id=test_user.id
    )
    
    assert not is_valid
    assert error is not None
