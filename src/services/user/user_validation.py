"""User validation service."""
from typing import Tuple, Optional
from sqlalchemy.orm import Session

from src.database.repositories.user_repo import UserRepository


class UserValidationService:
    """User validation service."""
    
    def __init__(self, db: Session):
        """
        Initialize user validation service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
    
    def validate_user_exists(self, user_id: int) -> Tuple[bool, Optional[str]]:
        """
        Validate that user exists.
        
        Args:
            user_id: User ID
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False, "User not found"
        
        return True, None
    
    def validate_user_active(self, user_id: int) -> Tuple[bool, Optional[str]]:
        """
        Validate that user is active.
        
        Args:
            user_id: User ID
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False, "User not found"
        
        if not user.is_active:
            return False, "User is not active"
        
        if user.is_banned:
            return False, f"User is banned: {user.ban_reason}"
        
        return True, None
    
    def validate_telegram_user(self, telegram_user_id: int) -> Tuple[bool, Optional[str]]:
        """
        Validate Telegram user ID.
        
        Args:
            telegram_user_id: Telegram user ID
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if telegram_user_id <= 0:
            return False, "Invalid Telegram user ID"
        
        return True, None
