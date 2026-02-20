"""Bonus API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.connection import get_db
from src.economics.bonuses import BonusManager

router = APIRouter(prefix="/bonuses", tags=["bonuses"])


@router.get("/available")
def get_available_bonuses(
    user_id: int,
    currency: str,
    db: Session = Depends(get_db)
):
    """Get available bonuses."""
    manager = BonusManager(db)
    return manager.get_available_bonuses(user_id, currency)
