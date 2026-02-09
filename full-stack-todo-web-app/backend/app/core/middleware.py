"""
Authentication middleware for FastAPI application.

This module implements middleware to validate JWT tokens on incoming requests
and ensure that the user ID in the token matches the user ID in the URL path.
"""

from fastapi import HTTPException, status, Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from jose import JWTError, jwt
import os
from urllib.parse import urlparse
import logging

# Get the shared secret from environment variables
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")
if not BETTER_AUTH_SECRET:
    raise ValueError("BETTER_AUTH_SECRET environment variable is not set")

ALGORITHM = "HS256"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Authentication middleware that validates JWT tokens and enforces user isolation.

    This middleware checks that:
    1. A valid JWT token is present in the Authorization header
    2. The user ID in the token matches the user ID in the URL path
    3. Returns appropriate 401/403 responses for unauthorized access
    """

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Define public endpoints that don't require authentication
        public_endpoints = ["/docs", "/redoc", "/openapi.json", "/health", "/"]

        # Extract path to check if it's a public endpoint
        path = request.url.path

        # Skip authentication for public endpoints
        if path in public_endpoints:
            return await call_next(request)

        # Skip authentication for auth endpoints (login, register, etc.)
        if path.startswith("/api/auth/"):
            return await call_next(request)

        # Check if this is an API endpoint that requires authentication
        if not path.startswith("/api/"):
            return await call_next(request)

        # Extract user_id from the URL path
        # Supports format /api/{user_id}/... and /api/v1/chat/{user_id}/...
        path_segments = path.strip('/').split('/')
        url_user_id = None

        if len(path_segments) >= 2 and path_segments[0] == 'api':
            # Case 1: /api/{user_id}/...
            if path_segments[1].isdigit():
                url_user_id = path_segments[1]
            # Case 2: /api/v1/chat/{user_id}/...
            elif len(path_segments) >= 4 and path_segments[1] == 'v1' and path_segments[2] == 'chat':
                if path_segments[3].isdigit():
                    url_user_id = path_segments[3]

        if url_user_id:
            # Get the authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                logger.warning(f"Missing or invalid Authorization header for path: {path}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authorization header missing or invalid"
                )

            # Extract the token
            token = auth_header.split(' ')[1]

            # Verify the JWT token and validate user access
            try:
                # Decode the token to get the payload
                payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])

                # Extract user ID from token
                token_user_id = str(payload.get("sub"))
                if not token_user_id:
                    logger.warning(f"No user ID found in token for path: {path}")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid token: no user ID found"
                    )

                # Validate that the user ID in the token matches the one in the URL
                if token_user_id != url_user_id:
                    logger.warning(f"User ID mismatch - token: {token_user_id}, url: {url_user_id} for path: {path}")
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Access denied: User ID mismatch"
                    )

            except HTTPException:
                # Re-raise HTTP exceptions as they are
                raise
            except JWTError as e:
                logger.error(f"JWT validation error for path: {path}, error: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token"
                )
            except Exception as e:
                logger.error(f"Unexpected error in auth middleware for path: {path}, error: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Internal server error during authentication: {str(e)}"
                )

        # Continue with the request if authentication passes
        response = await call_next(request)
        return response


async def graceful_failure_handler(request: Request, call_next: RequestResponseEndpoint) -> Response:
    """
    Wrapper function to handle authentication service availability with graceful fallbacks.
    """
    try:
        return await call_next(request)
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        # Log the error and return a generic error response
        logger.error(f"Unexpected error in middleware: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service temporarily unavailable"
        )