"""
JWT utility functions for token verification and validation.

This module provides reusable functions for JWT operations that can be used
across different parts of the application.
"""

import os
from typing import Optional
from fastapi import HTTPException, status
from jose import JWTError, jwt
from datetime import datetime
import logging

# Get the shared secret from environment variables
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")
if not BETTER_AUTH_SECRET:
    raise ValueError("BETTER_AUTH_SECRET environment variable is not set")

ALGORITHM = "HS256"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def verify_jwt_token(token: str) -> Optional[dict]:
    """
    Verify a JWT token and return the payload if valid.

    Args:
        token: JWT token string

    Returns:
        Decoded token payload if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        logger.warning(f"JWT verification failed: {str(e)}")
        return None


def extract_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user ID from JWT token.

    Args:
        token: JWT token string

    Returns:
        User ID if found and valid, None otherwise
    """
    payload = verify_jwt_token(token)
    if payload:
        # Better Auth typically stores user ID in 'sub' (subject) field
        user_id = payload.get("sub")
        if user_id:
            return str(user_id)
    return None


def validate_user_access(token_user_id: str, url_user_id: str) -> bool:
    """
    Validate that the user ID from the token matches the user ID in the URL.

    Args:
        token_user_id: User ID extracted from JWT token
        url_user_id: User ID from the request URL

    Returns:
        True if user IDs match, False otherwise
    """
    is_valid = token_user_id == url_user_id
    if not is_valid:
        logger.warning(f"User access validation failed: token_user_id={token_user_id}, url_user_id={url_user_id}")
    return is_valid


def authenticate_and_authorize(token: str, url_user_id: str) -> bool:
    """
    Authenticate JWT token and authorize access to the specified user ID.

    Args:
        token: JWT token string
        url_user_id: User ID from the request URL

    Returns:
        True if authentication and authorization succeed

    Raises:
        HTTPException: If authentication or authorization fails
    """
    # Verify the JWT token
    payload = verify_jwt_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # Extract user ID from token
    token_user_id = extract_user_id_from_token(token)
    if not token_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: no user ID found"
        )

    # Validate that token user ID matches URL user ID
    if not validate_user_access(token_user_id, url_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    logger.info(f"Successfully authenticated user {token_user_id} for access to {url_user_id}")
    return True


def is_token_expired(token: str) -> bool:
    """
    Check if a JWT token is expired.

    Args:
        token: JWT token string

    Returns:
        True if token is expired, False otherwise
    """
    try:
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])
        exp = payload.get("exp")

        if exp is None:
            return True

        return datetime.fromtimestamp(exp) < datetime.utcnow()
    except JWTError:
        # If we can't decode the token, treat it as expired
        return True