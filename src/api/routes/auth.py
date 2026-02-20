"""Authentication routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.database.repositories.user_repo import UserRepository
from src.api.middleware.auth import create_access_token, get_current_user
from src.api.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post("/login", response_model=dict)
async def login(
    telegram_user_id: int,
    username: str = None,
    first_name: str = None,
    last_name: str = None,
    db: Session = Depends(get_db)
):
    """
    Login or register user via Telegram.
    
    Args:
        telegram_user_id: Telegram user ID
        username: Telegram username
        first_name: First name
        last_name: Last name
        db: Database session
    
    Returns:
        Access token and user data
    """
    user_repo = UserRepository(db)
    
    # Get or create user
    user = user_repo.get_by_telegram_id(telegram_user_id)
    if not user:
        user = user_repo.create(telegram_user_id, username, first_name, last_name)
    
    # Update user info
    if username:
        user.username = username
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    db.commit()
    
    # Create access token
    token = create_access_token(telegram_user_id)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user).dict()
    }


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get current user info.
    
    Args:
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        User data
    """
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(current_user["id"])
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return UserResponse.from_orm(user)
