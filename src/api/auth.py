from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import os

# For a simple implementation, we'll use a shared secret/token
SECURE_ENDPOINTS_ENABLED = os.getenv("SECURE_ENDPOINTS", "false").lower() == "true"
SHARED_SECRET = os.getenv("SHARED_SECRET", "default_secret_for_demo")

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = None):
    if not SECURE_ENDPOINTS_ENABLED:
        # If security is disabled, allow all requests
        return True
    
    if not credentials or credentials.credentials != SHARED_SECRET:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )
    
    return True