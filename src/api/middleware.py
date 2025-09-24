from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import logging
import time
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log the incoming request
        logger.info(f"Request: {request.method} {request.url}")
        if request.query_params:
            logger.info(f"Query params: {dict(request.query_params)}")
        
        # Only log body for POST/PUT/PATCH requests
        if request.method in ["POST", "PUT", "PATCH"]:
            body = await request.body()
            if body:
                logger.info(f"Request body: {body.decode('utf-8')}")
        
        try:
            response = await call_next(request)
        except Exception as e:
            # Log the exception
            logger.error(f"Exception occurred: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Re-raise the exception so it can be handled by FastAPI's exception handlers
            raise e
        finally:
            # Calculate request duration
            duration = time.time() - start_time
            
            # Log the response
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Duration: {duration:.2f}s")
        
        return response

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
        except HTTPException as e:
            # Log HTTP exceptions
            logger.error(f"HTTP Exception: {e.status_code} - {e.detail}")
            return JSONResponse(
                status_code=e.status_code,
                content={"error": e.detail}
            )
        except Exception as e:
            # Log unexpected exceptions
            logger.error(f"Unexpected exception: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error"}
            )
        
        return response