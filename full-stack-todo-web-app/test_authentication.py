"""
Test suite for authentication functionality.

This test suite covers the authentication and authorization features
implemented for the JWT-based security integration between Better Auth and FastAPI.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from jose import jwt
import sys
from pathlib import Path

# Add backend to path to import modules
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from backend.app.main import app
from backend.app.core.auth import authenticate_and_authorize
from backend.app.core.jwt_utils import (
    verify_jwt_token,
    extract_user_id_from_token,
    validate_user_access,
    is_token_expired
)

# Set up test environment
os.environ["BETTER_AUTH_SECRET"] = "test-secret-key-for-testing-purposes-only"

@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

def create_test_token(user_id: str, expires_delta=None):
    """Helper function to create a test JWT token."""
    from datetime import datetime, timedelta
    from backend.app.core.auth import SECRET_KEY, ALGORITHM

    if expires_delta is None:
        expires_delta = timedelta(minutes=15)  # Default to 15 minutes

    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": user_id, "exp": expire.timestamp()}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class TestJWTUtilities:
    """Test JWT utility functions."""

    def test_verify_jwt_token_valid(self):
        """Test that a valid JWT token can be verified."""
        token = create_test_token("123")

        result = verify_jwt_token(token)

        assert result is not None
        assert result["sub"] == "123"

    def test_verify_jwt_token_invalid(self):
        """Test that an invalid JWT token returns None."""
        result = verify_jwt_token("invalid.token.here")

        assert result is None

    def test_extract_user_id_from_token(self):
        """Test extracting user ID from a valid token."""
        token = create_test_token("456")

        user_id = extract_user_id_from_token(token)

        assert user_id == "456"

    def test_validate_user_access_matching(self):
        """Test that user access validation passes when IDs match."""
        result = validate_user_access("123", "123")

        assert result is True

    def test_validate_user_access_mismatch(self):
        """Test that user access validation fails when IDs don't match."""
        result = validate_user_access("123", "456")

        assert result is False

    def test_is_token_expired_unexpired(self):
        """Test that unexpired tokens are not marked as expired."""
        token = create_test_token("123")

        result = is_token_expired(token)

        assert result is False

    def test_is_token_expired_expired(self):
        """Test that expired tokens are marked as expired."""
        from datetime import timedelta
        expired_token = create_test_token("123", expires_delta=timedelta(seconds=-1))

        result = is_token_expired(expired_token)

        assert result is True

class TestAuthenticationAndAuthorization:
    """Test authentication and authorization functions."""

    def test_authenticate_and_authorize_success(self):
        """Test successful authentication and authorization."""
        token = create_test_token("123")

        result = authenticate_and_authorize(token, "123")

        assert result is True

    def test_authenticate_and_authorize_invalid_token(self):
        """Test that invalid tokens raise HTTPException."""
        from fastapi import HTTPException

        with pytest.raises(HTTPException) as exc_info:
            authenticate_and_authorize("invalid.token.here", "123")

        assert exc_info.value.status_code == 401

    def test_authenticate_and_authorize_user_id_mismatch(self):
        """Test that user ID mismatches raise HTTPException."""
        from fastapi import HTTPException
        token = create_test_token("123")

        with pytest.raises(HTTPException) as exc_info:
            authenticate_and_authorize(token, "456")

        assert exc_info.value.status_code == 403

class TestAPISecurity:
    """Test API endpoint security."""

    @pytest.mark.skip(reason="Requires full app setup with database")
    def test_api_requires_authentication(self, client):
        """Test that API endpoints require authentication."""
        # This would test that accessing /api/123/tasks without auth returns 401
        response = client.get("/api/123/tasks")
        assert response.status_code == 401  # Unauthorized

    @pytest.mark.skip(reason="Requires full app setup with database")
    def test_api_rejects_wrong_user_access(self, client):
        """Test that users can't access other users' data."""
        # This would test that a token for user 123 can't access /api/456/tasks
        token = create_test_token("123")
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/api/456/tasks", headers=headers)
        assert response.status_code == 403  # Forbidden

if __name__ == "__main__":
    pytest.main([__file__, "-v"])