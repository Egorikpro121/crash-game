"""Security middleware."""
from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import List


def setup_cors(app):
    """
    Setup CORS middleware.
    
    Args:
        app: FastAPI app
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://web.telegram.org",
            "https://webk.telegram.org",
            "https://webz.telegram.org",
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


async def security_headers_middleware(request: Request, call_next):
    """
    Add security headers.
    
    Args:
        request: FastAPI request
        call_next: Next middleware/handler
    
    Returns:
        Response
    """
    response = await call_next(request)
    
    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return response
