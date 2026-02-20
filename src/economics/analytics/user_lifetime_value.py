"""User Lifetime Value (LTV) calculations."""
from decimal import Decimal
from typing import Dict, List
from sqlalchemy.orm import Session

from src.database.repositories.user_repo import UserRepository
from src.database.repositories.payment_repo import PaymentRepository, PaymentType
from src.database.repositories.game_repo import BetRepository


class UserLifetimeValue:
    """Calculate user lifetime value."""
    
    def __init__(self, db: Session):
        """
        Initialize LTV calculator.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.payment_repo = PaymentRepository(db)
        self.bet_repo = BetRepository(db)
    
    def calculate_user_ltv(self, user_id: int) -> Dict:
        """
        Calculate lifetime value for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            LTV breakdown
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return {}
        
        # Total deposits
        total_deposits_ton = user.total_deposited_ton or Decimal("0.0")
        total_deposits_stars = user.total_deposited_stars or Decimal("0.0")
        
        # Total withdrawals
        total_withdrawals_ton = user.total_withdrawn_ton or Decimal("0.0")
        total_withdrawals_stars = user.total_withdrawn_stars or Decimal("0.0")
        
        # Net deposits (money put into system)
        net_deposits_ton = total_deposits_ton - total_withdrawals_ton
        net_deposits_stars = total_deposits_stars - total_withdrawals_stars
        
        # Total bets (activity indicator)
        total_bets = user.total_bets or 0
        
        # House profit from this user (estimated)
        # This is simplified - actual calculation would need bet history
        house_profit_ton = Decimal("0.0")
        house_profit_stars = Decimal("0.0")
        
        # LTV = net deposits + house profit
        ltv_ton = net_deposits_ton + house_profit_ton
        ltv_stars = net_deposits_stars + house_profit_stars
        
        return {
            "user_id": user_id,
            "total_deposits_ton": float(total_deposits_ton),
            "total_deposits_stars": float(total_deposits_stars),
            "total_withdrawals_ton": float(total_withdrawals_ton),
            "total_withdrawals_stars": float(total_withdrawals_stars),
            "net_deposits_ton": float(net_deposits_ton),
            "net_deposits_stars": float(net_deposits_stars),
            "total_bets": total_bets,
            "ltv_ton": float(ltv_ton),
            "ltv_stars": float(ltv_stars),
        }
    
    def calculate_average_ltv(self) -> Dict:
        """
        Calculate average LTV across all users.
        
        Returns:
            Average LTV statistics
        """
        users = self.user_repo.get_active_users(limit=10000)
        
        if not users:
            return {
                "average_ltv_ton": Decimal("0.0"),
                "average_ltv_stars": Decimal("0.0"),
                "total_users": 0,
            }
        
        total_ltv_ton = Decimal("0.0")
        total_ltv_stars = Decimal("0.0")
        
        for user in users:
            ltv = self.calculate_user_ltv(user.id)
            total_ltv_ton += Decimal(str(ltv.get("ltv_ton", 0)))
            total_ltv_stars += Decimal(str(ltv.get("ltv_stars", 0)))
        
        avg_ltv_ton = total_ltv_ton / Decimal(str(len(users)))
        avg_ltv_stars = total_ltv_stars / Decimal(str(len(users)))
        
        return {
            "average_ltv_ton": float(avg_ltv_ton),
            "average_ltv_stars": float(avg_ltv_stars),
            "total_users": len(users),
        }
    
    def get_top_ltv_users(self, limit: int = 100) -> List[Dict]:
        """
        Get users with highest LTV.
        
        Args:
            limit: Maximum number of users
        
        Returns:
            List of top LTV users
        """
        users = self.user_repo.get_active_users(limit=10000)
        
        user_ltvs = []
        for user in users:
            ltv = self.calculate_user_ltv(user.id)
            user_ltvs.append({
                "user_id": user.id,
                "telegram_id": user.telegram_user_id,
                "username": user.username,
                **ltv,
            })
        
        # Sort by LTV (TON + Stars)
        user_ltvs.sort(
            key=lambda x: x.get("ltv_ton", 0) + x.get("ltv_stars", 0) / 1000,
            reverse=True
        )
        
        return user_ltvs[:limit]
