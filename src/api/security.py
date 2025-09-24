from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import os

def add_cors_middleware(app: FastAPI):
    # Get allowed origins from environment, default to all for development
    allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "*")
    allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        # Expose headers that might be needed by clients
        expose_headers=["Content-Range", "X-Content-Range"],
    )

def add_security_headers(app: FastAPI):
    """
    Add security headers middleware
    Note: For a production application, you would use a dedicated security middleware
    like secure-headers or create a custom middleware to add security headers
    """
    @app.middleware("http")
    async def security_headers_middleware(request, call_next):
        response = await call_next(request)
        # Add basic security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response