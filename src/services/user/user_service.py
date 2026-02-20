"""User service - main user operations."""
from typing import Optional
from sqlalchemy.orm import Session

from src.database.repositories.user_repo import UserRepository
from src.database.models.user import User


class UserService:
    """Main user service."""
    
    def __init__(self, db: Session):
        """
        Initialize user service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
    
    def get_user(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
        
        Returns:
            User object or None
        """
        return self.user_repo.get_by_id(user_id)
    
    def get_user_by_telegram_id(self, telegram_user_id: int) -> Optional[User]:
        """
        Get user by Telegram ID.
        
        Args:
            telegram_user_id: Telegram user ID
        
        Returns:
            User object or None
        """
        return self.user_repo.get_by_telegram_id(telegram_user_id)
    
    def create_user(
        self,
        telegram_user_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        referral_code: Optional[str] = None
    ) -> User:
        """
        Create a new user.
        
        Args:
            telegram_user_id: Telegram user ID
            username: Username
            first_name: First name
            last_name: Last name
            referral_code: Referral code
        
        Returns:
            Created user
        """
        return self.user_repo.create(
            telegram_user_id=telegram_user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            referral_code=referral_code,
        )
    
    def get_or_create_user(
        self,
        telegram_user_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        referral_code: Optional[str] = None
    ) -> User:
        """
        Get existing user or create new one.
        
        Args:
            telegram_user_id: Telegram user ID
            username: Username
            first_name: First name
            last_name: Last name
            referral_code: Referral code
        
        Returns:
            User object
        """
        user = self.user_repo.get_by_telegram_id(telegram_user_id)
        
        if not user:
            user = self.create_user(
                telegram_user_id=telegram_user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                referral_code=referral_code,
            )
        
        return user
