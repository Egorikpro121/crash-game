"""Authentication middleware."""
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import jwt
from datetime import datetime, timedelta

from src.config import get_secret_key
from src.database.connection import get_db
from src.database.repositories.user_repo import UserRepository


security = HTTPBearer()


def create_access_token(telegram_user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token.
    
    Args:
        telegram_user_id: Telegram user ID
        expires_delta: Token expiration time
    
    Returns:
        JWT token
    """
    if expires_delta is None:
        expires_delta = timedelta(days=30)  # Long-lived for Telegram Mini App
    
    expire = datetime.utcnow() + expires_delta
    
    payload = {
        "telegram_user_id": telegram_user_id,
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    
    token = jwt.encode(payload, get_secret_key(), algorithm="HS256")
    return token


def verify_token(token: str) -> Optional[int]:
    """
    Verify JWT token and return user ID.
    
    Args:
        token: JWT token
    
    Returns:
        Telegram user ID or None
    """
    try:
        payload = jwt.decode(token, get_secret_key(), algorithms=["HS256"])
        return payload.get("telegram_user_id")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


async def get_current_user(request: Request) -> dict:
    """
    Get current authenticated user.
    
    Args:
        request: FastAPI request
    
    Returns:
        User data
    
    Raises:
        HTTPException: If authentication fails
    """
    # Try to get token from Authorization header
    authorization = request.headers.get("Authorization")
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        telegram_user_id = verify_token(token)
        if telegram_user_id:
            db = next(get_db())
            user_repo = UserRepository(db)
            user = user_repo.get_by_telegram_id(telegram_user_id)
            if user:
                return {"id": user.id, "telegram_user_id": user.telegram_user_id}
    
    # Try to get from Telegram Mini App init data
    init_data = request.headers.get("X-Telegram-Init-Data")
    if init_data:
        # Parse Telegram init data
        # In production, would verify signature
        # Placeholder implementation
        user_data = parse_telegram_init_data(init_data)
        if user_data:
            db = next(get_db())
            user_repo = UserRepository(db)
            user = user_repo.get_by_telegram_id(user_data["id"])
            if user:
                return {"id": user.id, "telegram_user_id": user.telegram_user_id}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated"
    )


def parse_telegram_init_data(init_data: str) -> Optional[dict]:
    """
    Parse Telegram Mini App init data.
    
    Args:
        init_data: Telegram init data string
    
    Returns:
        User data or None
    """
    # In production, would verify signature using bot token
    # Placeholder implementation
    try:
        # Parse query string format: key=value&key2=value2
        data = {}
        for pair in init_data.split("&"):
            if "=" in pair:
                key, value = pair.split("=", 1)
                data[key] = value
        
        # Extract user data from JSON
        if "user" in data:
            import json
            user_data = json.loads(data["user"])
            return user_data
    except Exception:
        pass
    
    return None
