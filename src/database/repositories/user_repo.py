"""User repository for database operations."""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from typing import Optional, List
from decimal import Decimal

from src.database.models.user import User


class UserRepository:
    """Repository for user operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_telegram_id(self, telegram_user_id: int) -> Optional[User]:
        """Get user by Telegram ID."""
        return self.db.query(User).filter(User.telegram_user_id == telegram_user_id).first()
    
    def get_by_referral_code(self, referral_code: str) -> Optional[User]:
        """Get user by referral code."""
        return self.db.query(User).filter(User.referral_code == referral_code).first()
    
    def create(self, telegram_user_id: int, username: Optional[str] = None,
               first_name: Optional[str] = None, last_name: Optional[str] = None,
               referral_code: Optional[str] = None) -> User:
        """Create a new user."""
        user = User(
            telegram_user_id=telegram_user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            referral_code=referral_code,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update_balance(self, user_id: int, amount_ton: Decimal = Decimal("0"),
                      amount_stars: Decimal = Decimal("0")) -> User:
        """Update user balance atomically."""
        user = self.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        # Use database-level update for atomicity
        if amount_ton != 0:
            self.db.query(User).filter(User.id == user_id).update({
                User.balance_ton: User.balance_ton + amount_ton
            })
        if amount_stars != 0:
            self.db.query(User).filter(User.id == user_id).update({
                User.balance_stars: User.balance_stars + amount_stars
            })
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update_statistics(self, user_id: int, **kwargs) -> User:
        """Update user statistics."""
        user = self.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def ban_user(self, user_id: int, reason: str) -> User:
        """Ban a user."""
        user = self.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        user.is_banned = True
        user.ban_reason = reason
        user.is_active = False
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def unban_user(self, user_id: int) -> User:
        """Unban a user."""
        user = self.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        user.is_banned = False
        user.ban_reason = None
        user.is_active = True
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_active_users(self, limit: int = 100) -> List[User]:
        """Get active users."""
        return self.db.query(User).filter(
            User.is_active == True,
            User.is_banned == False
        ).order_by(desc(User.last_login_at)).limit(limit).all()
    
    def get_top_earners(self, limit: int = 100, currency: str = "TON") -> List[User]:
        """Get top earners by total won."""
        if currency == "TON":
            return self.db.query(User).filter(
                User.is_banned == False
            ).order_by(desc(User.total_won_ton)).limit(limit).all()
        else:
            return self.db.query(User).filter(
                User.is_banned == False
            ).order_by(desc(User.total_won_stars)).limit(limit).all()
    
    def get_by_referrer_id(self, referrer_id: int) -> List[User]:
        """Get all users referred by a specific user."""
        return self.db.query(User).filter(
            User.referred_by_id == referrer_id
        ).all()
