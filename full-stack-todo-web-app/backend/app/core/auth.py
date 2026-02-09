from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv

load_dotenv()

# JWT configuration
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create JWT access token

    Args:
        data: Data to encode in the token
        expires_delta: Optional expiration time delta

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, BETTER_AUTH_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify JWT token from request credentials

    Args:
        credentials: HTTP authorization credentials from request

    Returns:
        Decoded token payload if valid

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def verify_user_owns_resource(url_user_id: str, token_payload: dict):
    """
    Verify that the user owns the resource they're trying to access

    Args:
        url_user_id: User ID from the request URL path parameter
        token_payload: Decoded JWT token payload

    Raises:
        HTTPException: If user doesn't have permission to access the resource
    """
    token_user_id = str(token_payload.get("sub"))

    if url_user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )


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
    try:
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # Extract user ID from token
    token_user_id = str(payload.get("sub"))
    if not token_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: no user ID found"
        )

    # Validate that token user ID matches URL user ID
    if token_user_id != url_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    return True