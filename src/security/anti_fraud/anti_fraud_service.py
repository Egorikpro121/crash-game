"""Anti-fraud service."""
from src.security.anti_fraud import AntiFraudSystem, anti_fraud


class AntiFraudService:
    """Anti-fraud service wrapper."""
    
    def __init__(self):
        self.system = anti_fraud
    
    def check_bet_frequency(self, user_id: int, max_bets_per_minute: int = 10):
        """Check bet frequency."""
        return self.system.check_bet_frequency(user_id, max_bets_per_minute)
    
    def get_suspicion_score(self, user_id: int) -> int:
        """Get suspicion score."""
        return self.system.get_suspicion_score(user_id)
