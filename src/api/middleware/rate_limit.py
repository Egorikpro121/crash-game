"""Rate limiting middleware."""
from fastapi import Request, HTTPException, status
from typing import Dict
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio


class RateLimiter:
    """Simple rate limiter."""
    
    def __init__(self):
        """Initialize rate limiter."""
        self.requests: Dict[str, list] = defaultdict(list)
        self.lock = asyncio.Lock()
    
    async def check_rate_limit(self, key: str, max_requests: int, window_seconds: int) -> bool:
        """
        Check if request is within rate limit.
        
        Args:
            key: Rate limit key (e.g., user_id or IP)
            max_requests: Maximum requests allowed
            window_seconds: Time window in seconds
        
        Returns:
            True if within limit, False otherwise
        """
        async with self.lock:
            now = datetime.utcnow()
            window_start = now - timedelta(seconds=window_seconds)
            
            # Clean old requests
            self.requests[key] = [
                req_time for req_time in self.requests[key]
                if req_time > window_start
            ]
            
            # Check limit
            if len(self.requests[key]) >= max_requests:
                return False
            
            # Add current request
            self.requests[key].append(now)
            return True


# Global rate limiter instance
rate_limiter = RateLimiter()


async def rate_limit_middleware(request: Request, call_next):
    """
    Rate limiting middleware.
    
    Args:
        request: FastAPI request
        call_next: Next middleware/handler
    
    Returns:
        Response
    """
    # Get rate limit key (user ID or IP)
    user_id = request.state.get("user_id")
    key = f"user_{user_id}" if user_id else f"ip_{request.client.host}"
    
    # Check rate limit (e.g., 100 requests per minute)
    is_allowed = await rate_limiter.check_rate_limit(key, max_requests=100, window_seconds=60)
    
    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )
    
    response = await call_next(request)
    return response
