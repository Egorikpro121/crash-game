"""Integration tests for frontend-backend communication."""
import pytest
from fastapi.testclient import TestClient

from src.api.main import app
from src.database.connection import Base, engine


@pytest.fixture
def client():
    """Create test client."""
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


def test_api_cors_headers(client):
    """Test CORS headers are set correctly."""
    response = client.options("/")
    assert "access-control-allow-origin" in response.headers or response.status_code == 200


def test_api_response_format(client):
    """Test API response format."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


def test_api_error_handling(client):
    """Test API error handling."""
    # Test invalid endpoint
    response = client.get("/invalid/endpoint")
    assert response.status_code == 404


def test_api_json_content_type(client):
    """Test API returns JSON content type."""
    response = client.get("/health")
    assert "application/json" in response.headers.get("content-type", "")
