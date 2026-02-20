"""Referral API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.connection import get_db
from src.economics.referrals import ReferralManager

router = APIRouter(prefix="/referrals", tags=["referrals"])


@router.get("/code")
def get_referral_code(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user referral code."""
    manager = ReferralManager(db)
    return {"code": manager.get_referral_code(user_id)}
