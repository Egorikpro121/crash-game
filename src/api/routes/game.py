"""Game routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal

from src.database.connection import get_db
from src.api.middleware.auth import get_current_user
from src.api.schemas.game import (
    BetRequest, BetResponse, CashoutRequest, CashoutResponse,
    RoundStatus, RoundHistory, ActiveBet
)
from src.game.engine.game_session import GameSession

router = APIRouter(prefix="/game", tags=["game"])


@router.get("/round/status", response_model=RoundStatus)
async def get_round_status(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current round status.
    
    Args:
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Round status
    """
    game_session = GameSession(db)
    status_data = game_session.get_round_status()
    
    return RoundStatus(**status_data)


@router.post("/bet", response_model=BetResponse)
async def place_bet(
    bet_request: BetRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Place a bet.
    
    Args:
        bet_request: Bet request data
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Bet response
    """
    game_session = GameSession(db)
    
    try:
        bet_data = game_session.place_bet(
            current_user["id"],
            bet_request.amount,
            bet_request.currency,
            bet_request.auto_cashout
        )
        
        return BetResponse(
            bet_id=bet_data["bet_id"],
            round_id=bet_data["round_id"],
            amount=bet_data["amount"],
            currency=bet_data["currency"],
            auto_cashout_multiplier=bet_data.get("auto_cashout_multiplier"),
            status=bet_data["status"].value,
            placed_at=bet_data["placed_at"]
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/cashout", response_model=CashoutResponse)
async def cashout(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cash out current bet.
    
    Args:
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Cashout response
    """
    game_session = GameSession(db)
    
    try:
        cashout_data = game_session.cashout(current_user["id"])
        
        if not cashout_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No active bet to cash out"
            )
        
        return CashoutResponse(
            bet_id=cashout_data["bet_id"],
            multiplier=cashout_data["cashed_out_multiplier"],
            payout=cashout_data["payout"],
            currency=cashout_data["currency"],
            cashed_out_at=cashout_data["cashed_out_at"]
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/history", response_model=list[RoundHistory])
async def get_history(
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get game history.
    
    Args:
        limit: Number of rounds to return
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        Round history
    """
    from src.database.repositories.game_repo import GameRoundRepository
    
    round_repo = GameRoundRepository(db)
    rounds = round_repo.get_latest_rounds(limit)
    
    return [
        RoundHistory(
            round_id=r.id,
            crash_multiplier=r.crash_multiplier or Decimal("0"),
            started_at=r.started_at or r.created_at,
            crashed_at=r.crashed_at or r.created_at,
            total_bets=r.total_bets
        )
        for r in rounds
    ]
