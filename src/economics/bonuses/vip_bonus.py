"""VIP bonus system."""
from decimal import Decimal
from sqlalchemy.orm import Session

from src.database.repositories.user_repo import UserRepository
from src.database.repositories.transaction_repo import TransactionRepository, TransactionType
from src.economics.core.bonus_calculator import BonusCalculator


class VIPBonus:
    """Handle VIP bonuses."""
    
    def __init__(self, db: Session):
        """
        Initialize VIP bonus handler.
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.transaction_repo = TransactionRepository(db)
        self.bonus_calculator = BonusCalculator()
    
    def calculate_vip_level(self, user_id: int) -> int:
        """
        Calculate user VIP level based on total deposits.
        
        Args:
            user_id: User ID
        
        Returns:
            VIP level (1-5)
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return 0
        
        # Calculate total deposits in TON equivalent
        total_deposits = user.total_deposited_ton + (user.total_deposited_stars / Decimal("1000"))
        
        # VIP levels based on total deposits
        if total_deposits >= Decimal("1000"):
            return 5
        elif total_deposits >= Decimal("500"):
            return 4
        elif total_deposits >= Decimal("100"):
            return 3
        elif total_deposits >= Decimal("50"):
            return 2
        elif total_deposits >= Decimal("10"):
            return 1
        
        return 0
    
    def calculate_vip_bonus(
        self,
        user_id: int,
        currency: str
    ) -> Decimal:
        """
        Calculate VIP bonus for user.
        
        Args:
            user_id: User ID
            currency: Currency
        
        Returns:
            VIP bonus amount
        """
        vip_level = self.calculate_vip_level(user_id)
        
        if vip_level == 0:
            return Decimal("0.0")
        
        return self.bonus_calculator.calculate_vip_bonus(vip_level, currency)
    
    def apply_vip_bonus(self, user_id: int, currency: str) -> Decimal:
        """
        Apply VIP bonus to user.
        
        Args:
            user_id: User ID
            currency: Currency
        
        Returns:
            Bonus amount applied
        """
        bonus_amount = self.calculate_vip_bonus(user_id, currency)
        
        if bonus_amount > 0:
            user = self.user_repo.get_by_id(user_id)
            vip_level = self.calculate_vip_level(user_id)
            
            if currency == "TON":
                self.user_repo.update_balance(user_id, amount_ton=bonus_amount)
                balance_before = user.balance_ton
                balance_after = balance_before + bonus_amount
            else:
                self.user_repo.update_balance(user_id, amount_stars=bonus_amount)
                balance_before = user.balance_stars
                balance_after = balance_before + bonus_amount
            
            # Create transaction record
            self.transaction_repo.create(
                user_id=user_id,
                transaction_type=TransactionType.BONUS,
                currency=currency,
                amount=bonus_amount,
                balance_before=balance_before,
                balance_after=balance_after,
                description=f"VIP {vip_level} bonus: {bonus_amount} {currency}",
            )
        
        return bonus_amount
