"""User routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.api.middleware.auth import get_current_user
from src.api.schemas.user import UserResponse, UserBalance, UserStatistics
from src.database.repositories.user_repo import UserRepository

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/balance", response_model=UserBalance)
async def get_balance(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user balance.
    
    Args:
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        User balance
    """
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(current_user["id"])
    
    return UserBalance(
        balance_ton=user.balance_ton,
        balance_stars=user.balance_stars
    )


@router.get("/statistics", response_model=UserStatistics)
async def get_statistics(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user statistics.
    
    Args:
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        User statistics
    """
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(current_user["id"])
    
    # Calculate win rate
    total_games = user.total_bets
    wins = user.total_cashouts
    win_rate = Decimal("0.0")
    if total_games > 0:
        win_rate = Decimal(wins) / Decimal(total_games) * Decimal("100")
    
    return UserStatistics(
        total_bets=user.total_bets,
        total_cashouts=user.total_cashouts,
        total_won_ton=user.total_won_ton,
        total_won_stars=user.total_won_stars,
        total_lost_ton=user.total_lost_ton,
        total_lost_stars=user.total_lost_stars,
        biggest_win_ton=user.biggest_win_ton,
        biggest_win_stars=user.biggest_win_stars,
        biggest_multiplier=user.biggest_multiplier,
        win_rate=win_rate
    )
