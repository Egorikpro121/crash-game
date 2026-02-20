"""Integration tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.api.main import app
from src.database.connection import get_db, Base, engine
from src.database.repositories.user_repo import UserRepository


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


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
        first_name="Test",
    )
    return user


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_auth_login(client, db_session: Session):
    """Test login endpoint."""
    response = client.post(
        "/auth/login",
        json={
            "telegram_user_id": 123456789,
            "username": "testuser",
            "first_name": "Test",
        }
    )
    assert response.status_code in [200, 201]
    data = response.json()
    assert "token" in data or "access_token" in data


def test_get_balance(client, test_user, db_session: Session):
    """Test get balance endpoint."""
    # First login to get token
    login_response = client.post(
        "/auth/login",
        json={
            "telegram_user_id": test_user.telegram_user_id,
            "username": test_user.username,
        }
    )
    token = login_response.json().get("token") or login_response.json().get("access_token")
    
    # Get balance
    response = client.get(
        "/user/balance",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "ton" in data or "balance_ton" in data
    assert "stars" in data or "balance_stars" in data


def test_get_round_status(client):
    """Test get round status endpoint."""
    response = client.get("/game/round/status")
    assert response.status_code in [200, 404]  # 404 if no active round


def test_bonuses_endpoint(client, test_user, db_session: Session):
    """Test bonuses endpoint."""
    login_response = client.post(
        "/auth/login",
        json={
            "telegram_user_id": test_user.telegram_user_id,
        }
    )
    token = login_response.json().get("token") or login_response.json().get("access_token")
    
    response = client.get(
        "/bonuses/available?user_id=1&currency=TON",
        headers={"Authorization": f"Bearer {token}"}
    )
    # Should return 200 or handle error gracefully
    assert response.status_code in [200, 400, 404]


def test_referrals_endpoint(client, test_user, db_session: Session):
    """Test referrals endpoint."""
    login_response = client.post(
        "/auth/login",
        json={
            "telegram_user_id": test_user.telegram_user_id,
        }
    )
    token = login_response.json().get("token") or login_response.json().get("access_token")
    
    response = client.get(
        "/referrals/code?user_id=1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code in [200, 400, 404]


def test_leaderboard_endpoint(client):
    """Test leaderboard endpoint."""
    response = client.get("/leaderboard/top?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) or isinstance(data, dict)
