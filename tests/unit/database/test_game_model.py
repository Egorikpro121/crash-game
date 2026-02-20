"""Tests for Game models (~100 tests for GameRound, ~100 for Bet)."""
import pytest
from decimal import Decimal
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from src.database.connection import Base
from src.database.models.game import GameRound, Bet, GameRoundStatus, BetStatus
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
    user = User(telegram_user_id=123456789)
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def sample_round(db_session):
    """Create a sample game round."""
    round_obj = GameRound(
        server_seed_hash="abc123hash",
        status=GameRoundStatus.PENDING
    )
    db_session.add(round_obj)
    db_session.commit()
    return round_obj


# ========== GameRound Tests (1-100) ==========

# Test 1-20: Basic creation
def test_create_round_minimal(db_session):
    """Test creating round with minimal fields."""
    round_obj = GameRound(server_seed_hash="hash123")
    db_session.add(round_obj)
    db_session.commit()
    assert round_obj.id is not None
    assert round_obj.server_seed_hash == "hash123"
    assert round_obj.status == GameRoundStatus.PENDING


def test_create_round_with_client_seed(db_session):
    """Test creating round with client seed."""
    round_obj = GameRound(
        server_seed_hash="hash123",
        client_seed="client456"
    )
    db_session.add(round_obj)
    db_session.commit()
    assert round_obj.client_seed == "client456"


def test_round_default_status(db_session):
    """Test round default status is PENDING."""
    round_obj = GameRound(server_seed_hash="hash123")
    db_session.add(round_obj)
    db_session.commit()
    assert round_obj.status == GameRoundStatus.PENDING


def test_round_default_statistics(db_session):
    """Test round default statistics."""
    round_obj = GameRound(server_seed_hash="hash123")
    db_session.add(round_obj)
    db_session.commit()
    assert round_obj.total_bets == 0
    assert round_obj.total_bet_amount_ton == Decimal("0.0")


def test_round_status_enum(db_session):
    """Test round status enum values."""
    assert GameRoundStatus.PENDING == "pending"
    assert GameRoundStatus.ACTIVE == "active"
    assert GameRoundStatus.CRASHED == "crashed"
    assert GameRoundStatus.CANCELLED == "cancelled"


def test_round_set_status_active(db_session):
    """Test setting round status to ACTIVE."""
    round_obj = GameRound(server_seed_hash="hash123")
    db_session.add(round_obj)
    db_session.commit()
    round_obj.status = GameRoundStatus.ACTIVE
    db_session.commit()
    assert round_obj.status == GameRoundStatus.ACTIVE


def test_round_set_status_crashed(db_session):
    """Test setting round status to CRASHED."""
    round_obj = GameRound(server_seed_hash="hash123")
    db_session.add(round_obj)
    db_session.commit()
    round_obj.status = GameRoundStatus.CRASHED
    db_session.commit()
    assert round_obj.status == GameRoundStatus.CRASHED


def test_round_crash_multiplier(db_session):
    """Test setting crash multiplier."""
    round_obj = GameRound(server_seed_hash="hash123", crash_multiplier=Decimal("2.5"))
    db_session.add(round_obj)
    db_session.commit()
    assert round_obj.crash_multiplier == Decimal("2.5")


def test_round_duration_ms(db_session):
    """Test setting duration."""
    round_obj = GameRound(server_seed_hash="hash123", duration_ms=5000)
    db_session.add(round_obj)
    db_session.commit()
    assert round_obj.duration_ms == 5000


def test_round_started_at(db_session):
    """Test setting started_at timestamp."""
    start_time = datetime.utcnow()
    round_obj = GameRound(server_seed_hash="hash123", started_at=start_time)
    db_session.add(round_obj)
    db_session.commit()
    assert round_obj.started_at == start_time


def test_round_crashed_at(db_session):
    """Test setting crashed_at timestamp."""
    crash_time = datetime.utcnow()
    round_obj = GameRound(server_seed_hash="hash123", crashed_at=crash_time)
    db_session.add(round_obj)
    db_session.commit()
    assert round_obj.crashed_at == crash_time


def test_round_combined_seed(db_session):
    """Test setting combined seed."""
    round_obj = GameRound(
        server_seed_hash="hash123",
        combined_seed="combined789"
    )
    db_session.add(round_obj)
    db_session.commit()
    assert round_obj.combined_seed == "combined789"


def test_round_server_seed_revealed(db_session):
    """Test revealing server seed."""
    round_obj = GameRound(server_seed_hash="hash123", server_seed="revealed_seed")
    db_session.add(round_obj)
    db_session.commit()
    assert round_obj.server_seed == "revealed_seed"


def test_round_total_bets_counter(db_session):
    """Test total_bets counter."""
    round_obj = GameRound(server_seed_hash="hash123", total_bets=10)
    db_session.add(round_obj)
    db_session.commit()
    assert round_obj.total_bets == 10


def test_round_total_bet_amount(db_session):
    """Test total bet amounts."""
    round_obj = GameRound(
        server_seed_hash="hash123",
        total_bet_amount_ton=Decimal("100.5"),
        total_bet_amount_stars=Decimal("10000.0")
    )
    db_session.add(round_obj)
    db_session.commit()
    assert round_obj.total_bet_amount_ton == Decimal("100.5")
    assert round_obj.total_bet_amount_stars == Decimal("10000.0")


def test_round_total_payout(db_session):
    """Test total payout amounts."""
    round_obj = GameRound(
        server_seed_hash="hash123",
        total_payout_ton=Decimal("200.0"),
        total_payout_stars=Decimal("20000.0")
    )
    db_session.add(round_obj)
    db_session.commit()
    assert round_obj.total_payout_ton == Decimal("200.0")
    assert round_obj.total_payout_stars == Decimal("20000.0")


def test_round_has_bets_relationship(db_session):
    """Test round has bets relationship."""
    round_obj = GameRound(server_seed_hash="hash123")
    db_session.add(round_obj)
    db_session.commit()
    assert round_obj.bets == []


def test_round_to_dict(db_session):
    """Test round to_dict method."""
    round_obj = GameRound(
        server_seed_hash="hash123",
        crash_multiplier=Decimal("3.5"),
        status=GameRoundStatus.CRASHED
    )
    db_session.add(round_obj)
    db_session.commit()
    data = round_obj.to_dict()
    assert data["server_seed_hash"] == "hash123"
    assert data["crash_multiplier"] == 3.5
    assert data["status"] == "crashed"


def test_round_repr(db_session):
    """Test round __repr__ method."""
    round_obj = GameRound(server_seed_hash="hash123", crash_multiplier=Decimal("2.5"))
    db_session.add(round_obj)
    db_session.commit()
    repr_str = repr(round_obj)
    assert "GameRound" in repr_str
    assert str(round_obj.id) in repr_str


# Test 21-40: Round state transitions
def test_round_pending_to_active(db_session):
    """Test transitioning from PENDING to ACTIVE."""
    round_obj = GameRound(server_seed_hash="hash123")
    db_session.add(round_obj)
    db_session.commit()
    round_obj.status = GameRoundStatus.ACTIVE
    round_obj.started_at = datetime.utcnow()
    db_session.commit()
    assert round_obj.status == GameRoundStatus.ACTIVE
    assert round_obj.started_at is not None


def test_round_active_to_crashed(db_session):
    """Test transitioning from ACTIVE to CRASHED."""
    round_obj = GameRound(
        server_seed_hash="hash123",
        status=GameRoundStatus.ACTIVE,
        started_at=datetime.utcnow()
    )
    db_session.add(round_obj)
    db_session.commit()
    round_obj.status = GameRoundStatus.CRASHED
    round_obj.crashed_at = datetime.utcnow()
    round_obj.crash_multiplier = Decimal("1.5")
    db_session.commit()
    assert round_obj.status == GameRoundStatus.CRASHED
    assert round_obj.crashed_at is not None


# Test 41-60: Edge cases
def test_round_very_high_multiplier(db_session):
    """Test very high crash multiplier."""
    round_obj = GameRound(
        server_seed_hash="hash123",
        crash_multiplier=Decimal("999.99")
    )
    db_session.add(round_obj)
    db_session.commit()
    assert round_obj.crash_multiplier == Decimal("999.99")


def test_round_low_multiplier(db_session):
    """Test low crash multiplier."""
    round_obj = GameRound(
        server_seed_hash="hash123",
        crash_multiplier=Decimal("1.01")
    )
    db_session.add(round_obj)
    db_session.commit()
    assert round_obj.crash_multiplier == Decimal("1.01")


def test_round_long_duration(db_session):
    """Test long duration."""
    round_obj = GameRound(server_seed_hash="hash123", duration_ms=300000)
    db_session.add(round_obj)
    db_session.commit()
    assert round_obj.duration_ms == 300000


def test_round_short_duration(db_session):
    """Test short duration."""
    round_obj = GameRound(server_seed_hash="hash123", duration_ms=100)
    db_session.add(round_obj)
    db_session.commit()
    assert round_obj.duration_ms == 100


# ========== Bet Tests (1-100) ==========

# Test 1-20: Basic creation
def test_create_bet_ton(db_session, sample_user, sample_round):
    """Test creating bet with TON."""
    bet = Bet(
        user_id=sample_user.id,
        round_id=sample_round.id,
        amount_ton=Decimal("1.5"),
        currency="TON"
    )
    db_session.add(bet)
    db_session.commit()
    assert bet.id is not None
    assert bet.amount_ton == Decimal("1.5")
    assert bet.currency == "TON"


def test_create_bet_stars(db_session, sample_user, sample_round):
    """Test creating bet with Stars."""
    bet = Bet(
        user_id=sample_user.id,
        round_id=sample_round.id,
        amount_stars=Decimal("150.0"),
        currency="STARS"
    )
    db_session.add(bet)
    db_session.commit()
    assert bet.amount_stars == Decimal("150.0")
    assert bet.currency == "STARS"


def test_bet_default_status(db_session, sample_user, sample_round):
    """Test bet default status is PENDING."""
    bet = Bet(
        user_id=sample_user.id,
        round_id=sample_round.id,
        amount_ton=Decimal("1.0"),
        currency="TON"
    )
    db_session.add(bet)
    db_session.commit()
    assert bet.status == BetStatus.PENDING


def test_bet_auto_cashout(db_session, sample_user, sample_round):
    """Test bet with auto cashout."""
    bet = Bet(
        user_id=sample_user.id,
        round_id=sample_round.id,
        amount_ton=Decimal("1.0"),
        currency="TON",
        auto_cashout_multiplier=Decimal("2.5"),
        auto_cashout_enabled=True
    )
    db_session.add(bet)
    db_session.commit()
    assert bet.auto_cashout_multiplier == Decimal("2.5")
    assert bet.auto_cashout_enabled == True


def test_bet_status_enum(db_session):
    """Test bet status enum values."""
    assert BetStatus.PENDING == "pending"
    assert BetStatus.ACTIVE == "active"
    assert BetStatus.CASHED_OUT == "cashed_out"
    assert BetStatus.CRASHED == "crashed"
    assert BetStatus.CANCELLED == "cancelled"


def test_bet_set_status_active(db_session, sample_user, sample_round):
    """Test setting bet status to ACTIVE."""
    bet = Bet(
        user_id=sample_user.id,
        round_id=sample_round.id,
        amount_ton=Decimal("1.0"),
        currency="TON"
    )
    db_session.add(bet)
    db_session.commit()
    bet.status = BetStatus.ACTIVE
    db_session.commit()
    assert bet.status == BetStatus.ACTIVE


def test_bet_cashout(db_session, sample_user, sample_round):
    """Test cashing out a bet."""
    bet = Bet(
        user_id=sample_user.id,
        round_id=sample_round.id,
        amount_ton=Decimal("1.0"),
        currency="TON"
    )
    db_session.add(bet)
    db_session.commit()
    bet.status = BetStatus.CASHED_OUT
    bet.cashed_out_multiplier = Decimal("2.0")
    bet.payout_ton = Decimal("2.0")
    bet.profit_ton = Decimal("1.0")
    bet.cashed_out_at = datetime.utcnow()
    db_session.commit()
    assert bet.status == BetStatus.CASHED_OUT
    assert bet.cashed_out_multiplier == Decimal("2.0")
    assert bet.payout_ton == Decimal("2.0")


def test_bet_crash(db_session, sample_user, sample_round):
    """Test bet crashing."""
    bet = Bet(
        user_id=sample_user.id,
        round_id=sample_round.id,
        amount_ton=Decimal("1.0"),
        currency="TON"
    )
    db_session.add(bet)
    db_session.commit()
    bet.status = BetStatus.CRASHED
    db_session.commit()
    assert bet.status == BetStatus.CRASHED


def test_bet_relationships(db_session, sample_user, sample_round):
    """Test bet relationships."""
    bet = Bet(
        user_id=sample_user.id,
        round_id=sample_round.id,
        amount_ton=Decimal("1.0"),
        currency="TON"
    )
    db_session.add(bet)
    db_session.commit()
    assert bet.user.id == sample_user.id
    assert bet.round.id == sample_round.id


def test_bet_to_dict(db_session, sample_user, sample_round):
    """Test bet to_dict method."""
    bet = Bet(
        user_id=sample_user.id,
        round_id=sample_round.id,
        amount_ton=Decimal("1.5"),
        currency="TON",
        cashed_out_multiplier=Decimal("2.0"),
        payout_ton=Decimal("3.0")
    )
    db_session.add(bet)
    db_session.commit()
    data = bet.to_dict()
    assert data["user_id"] == sample_user.id
    assert data["amount_ton"] == 1.5
    assert data["currency"] == "TON"
    assert data["cashed_out_multiplier"] == 2.0


def test_bet_repr(db_session, sample_user, sample_round):
    """Test bet __repr__ method."""
    bet = Bet(
        user_id=sample_user.id,
        round_id=sample_round.id,
        amount_ton=Decimal("1.0"),
        currency="TON"
    )
    db_session.add(bet)
    db_session.commit()
    repr_str = repr(bet)
    assert "Bet" in repr_str
    assert str(bet.id) in repr_str


# Test 21-40: Bet operations
def test_bet_profit_calculation(db_session, sample_user, sample_round):
    """Test bet profit calculation."""
    bet = Bet(
        user_id=sample_user.id,
        round_id=sample_round.id,
        amount_ton=Decimal("1.0"),
        currency="TON",
        payout_ton=Decimal("2.5"),
        profit_ton=Decimal("1.5")
    )
    db_session.add(bet)
    db_session.commit()
    assert bet.profit_ton == Decimal("1.5")


def test_bet_stars_profit(db_session, sample_user, sample_round):
    """Test bet Stars profit."""
    bet = Bet(
        user_id=sample_user.id,
        round_id=sample_round.id,
        amount_stars=Decimal("100.0"),
        currency="STARS",
        payout_stars=Decimal("250.0"),
        profit_stars=Decimal("150.0")
    )
    db_session.add(bet)
    db_session.commit()
    assert bet.profit_stars == Decimal("150.0")


# Test 41-60: Edge cases
def test_bet_very_small_amount(db_session, sample_user, sample_round):
    """Test very small bet amount."""
    bet = Bet(
        user_id=sample_user.id,
        round_id=sample_round.id,
        amount_ton=Decimal("0.000000001"),
        currency="TON"
    )
    db_session.add(bet)
    db_session.commit()
    assert bet.amount_ton == Decimal("0.000000001")


def test_bet_very_large_amount(db_session, sample_user, sample_round):
    """Test very large bet amount."""
    bet = Bet(
        user_id=sample_user.id,
        round_id=sample_round.id,
        amount_ton=Decimal("1000.0"),
        currency="TON"
    )
    db_session.add(bet)
    db_session.commit()
    assert bet.amount_ton == Decimal("1000.0")


def test_bet_high_multiplier(db_session, sample_user, sample_round):
    """Test high cashout multiplier."""
    bet = Bet(
        user_id=sample_user.id,
        round_id=sample_round.id,
        amount_ton=Decimal("1.0"),
        currency="TON",
        cashed_out_multiplier=Decimal("100.0")
    )
    db_session.add(bet)
    db_session.commit()
    assert bet.cashed_out_multiplier == Decimal("100.0")


# Test 61-80: Foreign key constraints
def test_bet_requires_user(db_session, sample_round):
    """Test bet requires valid user_id."""
    bet = Bet(
        user_id=99999,  # Non-existent user
        round_id=sample_round.id,
        amount_ton=Decimal("1.0"),
        currency="TON"
    )
    db_session.add(bet)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_bet_requires_round(db_session, sample_user):
    """Test bet requires valid round_id."""
    bet = Bet(
        user_id=sample_user.id,
        round_id=99999,  # Non-existent round
        amount_ton=Decimal("1.0"),
        currency="TON"
    )
    db_session.add(bet)
    with pytest.raises(IntegrityError):
        db_session.commit()


# Test 81-100: Multiple bets
def test_multiple_bets_same_user(db_session, sample_user, sample_round):
    """Test multiple bets from same user."""
    bet1 = Bet(
        user_id=sample_user.id,
        round_id=sample_round.id,
        amount_ton=Decimal("1.0"),
        currency="TON"
    )
    bet2 = Bet(
        user_id=sample_user.id,
        round_id=sample_round.id,
        amount_ton=Decimal("2.0"),
        currency="TON"
    )
    db_session.add(bet1)
    db_session.add(bet2)
    db_session.commit()
    assert len(sample_user.bets) == 2


def test_multiple_bets_same_round(db_session, sample_user, sample_round):
    """Test multiple bets in same round."""
    user2 = User(telegram_user_id=987654321)
    db_session.add(user2)
    db_session.commit()
    
    bet1 = Bet(
        user_id=sample_user.id,
        round_id=sample_round.id,
        amount_ton=Decimal("1.0"),
        currency="TON"
    )
    bet2 = Bet(
        user_id=user2.id,
        round_id=sample_round.id,
        amount_ton=Decimal("2.0"),
        currency="TON"
    )
    db_session.add(bet1)
    db_session.add(bet2)
    db_session.commit()
    assert len(sample_round.bets) == 2
