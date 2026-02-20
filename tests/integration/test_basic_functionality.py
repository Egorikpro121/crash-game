"""Basic functionality tests."""
import pytest
from decimal import Decimal
from sqlalchemy.orm import Session

from src.database.connection import Base, engine
from src.database.repositories.user_repo import UserRepository
from src.economics.core.house_edge import HouseEdgeCalculator
from src.economics.core.commission_calculator import CommissionCalculator
from src.economics.core.bonus_calculator import BonusCalculator
from src.economics.limits.bet_limits import BetLimits


@pytest.fixture
def db_session():
    """Create test database session."""
    Base.metadata.create_all(bind=engine)
    from src.database.connection import SessionLocal
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_house_edge_calculation():
    """Test house edge calculation."""
    calculator = HouseEdgeCalculator(house_edge_percent=Decimal("0.01"))
    
    expected_multiplier = calculator.calculate_expected_multiplier(Decimal("2.0"))
    assert expected_multiplier < Decimal("2.0")
    assert expected_multiplier == Decimal("1.98")  # 2.0 * (1 - 0.01)


def test_commission_calculation():
    """Test commission calculation."""
    calculator = CommissionCalculator()
    
    commission = calculator.calculate_withdrawal_commission(
        Decimal("100.0"), "TON"
    )
    assert commission >= Decimal("0.1")  # Minimum commission


def test_bonus_calculation():
    """Test bonus calculation."""
    calculator = BonusCalculator()
    
    bonus = calculator.calculate_first_deposit_bonus(
        Decimal("10.0"), "TON"
    )
    assert bonus == Decimal("1.0")  # 10% of 10 TON


def test_bet_limits():
    """Test bet limits validation."""
    limits = BetLimits()
    
    is_valid, error = limits.validate_bet_amount(Decimal("0.01"), "TON")
    assert is_valid
    assert error is None
    
    is_valid, error = limits.validate_bet_amount(Decimal("0.001"), "TON")
    assert not is_valid
    assert error is not None


def test_user_creation(db_session: Session):
    """Test user creation."""
    user_repo = UserRepository(db_session)
    
    user = user_repo.create(
        telegram_user_id=999999999,
        username="testuser",
    )
    
    assert user.id is not None
    assert user.telegram_user_id == 999999999
    assert user.balance_ton == Decimal("0.0")
    assert user.balance_stars == Decimal("0.0")
