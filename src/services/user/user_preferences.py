"""User preferences service."""
from decimal import Decimal
from typing import Optional, Dict
from sqlalchemy.orm import Session

from src.database.repositories.user_repo import UserRepository
from src.database.models.user import User


class UserPreferencesService:
    """User preferences service."""
    
    def __init__(self, db: Session):
        """
        Initialize user preferences service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
    
    def get_preferences(self, user_id: int) -> Optional[Dict]:
        """
        Get user preferences.
        
        Args:
            user_id: User ID
        
        Returns:
            Preferences dictionary
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None
        
        return {
            "auto_cashout_enabled": user.auto_cashout_enabled,
            "default_auto_cashout_multiplier": (
                float(user.default_auto_cashout_multiplier)
                if user.default_auto_cashout_multiplier
                else None
            ),
            "sound_enabled": user.sound_enabled,
            "notifications_enabled": user.notifications_enabled,
        }
    
    def update_preferences(
        self,
        user_id: int,
        auto_cashout_enabled: Optional[bool] = None,
        default_auto_cashout_multiplier: Optional[Decimal] = None,
        sound_enabled: Optional[bool] = None,
        notifications_enabled: Optional[bool] = None,
    ) -> User:
        """
        Update user preferences.
        
        Args:
            user_id: User ID
            auto_cashout_enabled: Enable auto cashout
            default_auto_cashout_multiplier: Default auto cashout multiplier
            sound_enabled: Enable sound
            notifications_enabled: Enable notifications
        
        Returns:
            Updated user
        """
        updates = {}
        
        if auto_cashout_enabled is not None:
            updates["auto_cashout_enabled"] = auto_cashout_enabled
        if default_auto_cashout_multiplier is not None:
            updates["default_auto_cashout_multiplier"] = default_auto_cashout_multiplier
        if sound_enabled is not None:
            updates["sound_enabled"] = sound_enabled
        if notifications_enabled is not None:
            updates["notifications_enabled"] = notifications_enabled
        
        return self.user_repo.update_statistics(user_id, **updates)
