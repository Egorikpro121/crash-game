"""JWT service."""
from src.api.middleware.auth import create_access_token, verify_token


class JWTService:
    """JWT service wrapper."""
    
    def create_token(self, telegram_user_id: int, expires_delta=None):
        """Create JWT token."""
        return create_access_token(telegram_user_id, expires_delta)
    
    def verify_token(self, token: str):
        """Verify JWT token."""
        return verify_token(token)
