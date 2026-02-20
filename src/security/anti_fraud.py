"""Anti-fraud system."""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
from collections import defaultdict

from src.database.repositories.user_repo import UserRepository
from src.database.repositories.bet_repo import BetRepository


class AntiFraudSystem:
    """Anti-fraud detection system."""
    
    def __init__(self):
        """Initialize anti-fraud system."""
        self.bet_history: Dict[int, List[datetime]] = defaultdict(list)
        self.suspicious_patterns: Dict[int, int] = defaultdict(int)
    
    def check_bet_frequency(self, user_id: int, max_bets_per_minute: int = 10) -> tuple[bool, Optional[str]]:
        """
        Check if user is betting too frequently.
        
        Args:
            user_id: User ID
            max_bets_per_minute: Maximum bets per minute
        
        Returns:
            (is_valid, error_message)
        """
        now = datetime.utcnow()
        minute_ago = now - timedelta(minutes=1)
        
        # Clean old bets
        self.bet_history[user_id] = [
            bet_time for bet_time in self.bet_history[user_id]
            if bet_time > minute_ago
        ]
        
        # Check limit
        if len(self.bet_history[user_id]) >= max_bets_per_minute:
            self.suspicious_patterns[user_id] += 1
            return False, "Too many bets in short time"
        
        # Record bet
        self.bet_history[user_id].append(now)
        
        return True, None
    
    def check_bet_amounts(self, user_id: int, bet_amounts: List[Decimal],
                        threshold: Decimal = Decimal("0.01")) -> tuple[bool, Optional[str]]:
        """
        Check for suspicious bet amount patterns.
        
        Args:
            user_id: User ID
            bet_amounts: List of recent bet amounts
            threshold: Threshold for pattern detection
        
        Returns:
            (is_valid, error_message)
        """
        if len(bet_amounts) < 5:
            return True, None
        
        # Check if all amounts are identical (bot pattern)
        if len(set(bet_amounts)) == 1:
            self.suspicious_patterns[user_id] += 1
            return False, "Suspicious bet pattern detected"
        
        return True, None
    
    def check_win_rate(self, user_id: int, wins: int, total: int,
                      max_win_rate: float = 0.95) -> tuple[bool, Optional[str]]:
        """
        Check for suspiciously high win rate.
        
        Args:
            user_id: User ID
            wins: Number of wins
            total: Total bets
            max_win_rate: Maximum acceptable win rate
        
        Returns:
            (is_valid, error_message)
        """
        if total == 0:
            return True, None
        
        win_rate = wins / total
        if win_rate > max_win_rate:
            self.suspicious_patterns[user_id] += 1
            return False, f"Suspiciously high win rate: {win_rate:.2%}"
        
        return True, None
    
    def get_suspicion_score(self, user_id: int) -> int:
        """
        Get suspicion score for user.
        
        Args:
            user_id: User ID
        
        Returns:
            Suspicion score (0-100)
        """
        return min(self.suspicious_patterns.get(user_id, 0) * 10, 100)
    
    def should_ban_user(self, user_id: int, threshold: int = 50) -> bool:
        """
        Check if user should be banned.
        
        Args:
            user_id: User ID
            threshold: Suspicion score threshold
        
        Returns:
            True if should ban
        """
        return self.get_suspicion_score(user_id) >= threshold
    
    def reset_user_history(self, user_id: int):
        """
        Reset user history (for testing).
        
        Args:
            user_id: User ID
        """
        if user_id in self.bet_history:
            del self.bet_history[user_id]
        if user_id in self.suspicious_patterns:
            del self.suspicious_patterns[user_id]


# Global anti-fraud instance
anti_fraud = AntiFraudSystem()
