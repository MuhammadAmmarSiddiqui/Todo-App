# Authentication Flow Documentation

## Overview
This document describes the JWT-based authentication flow implemented between Better Auth (frontend) and FastAPI backend for the Todo Web Application.

## Architecture

### Components
- **Frontend**: Next.js 16+ application with Better Auth
- **Backend**: FastAPI server with JWT validation middleware
- **Shared Secret**: BETTER_AUTH_SECRET environment variable

### Flow Diagram
```
User Action → Better Auth → JWT Token → API Request → FastAPI Middleware → Database Query
```

## Detailed Flow

### 1. User Authentication
1. User registers/logs in via Better Auth on the frontend
2. Better Auth generates a JWT token with user information
3. Token is stored in frontend (localStorage/sessionStorage)
4. Token includes user ID in the `sub` (subject) field

### 2. API Request Flow
1. Frontend API client retrieves JWT token from storage
2. Token is attached to request header: `Authorization: Bearer <token>`
3. Request sent to backend API endpoint (e.g., `/api/{user_id}/tasks`)
4. FastAPI authentication middleware intercepts request

### 3. Token Validation
1. Middleware extracts JWT token from Authorization header
2. Token signature is verified using shared secret (BETTER_AUTH_SECRET)
3. Token payload is decoded to extract user ID
4. User ID from token is compared with user ID in URL path
5. If IDs match, request proceeds; otherwise, 403 Forbidden is returned

## Security Measures

### User Isolation
- Each user can only access their own data
- URL pattern: `/api/{user_id}/...` enforces user-specific access
- Middleware validates token user ID matches URL user ID

### Error Handling
- **401 Unauthorized**: Invalid/expired token, missing token
- **403 Forbidden**: Valid token but user ID mismatch
- **404 Not Found**: Resource doesn't exist for the user

### Token Management
- JWT tokens expire after 7 days (configurable)
- Tokens contain user ID, email, and expiration time
- Frontend handles token refresh when needed

## Implementation Details

### Backend Middleware
Located in: `backend/app/core/middleware.py`
- Implements `BaseHTTPMiddleware`
- Validates JWT tokens for all `/api/` routes
- Enforces user ID matching between token and URL

### Frontend API Client
Located in: `frontend/lib/api-client.ts`
- Automatically attaches JWT tokens to requests
- Handles authentication errors
- Provides convenient methods for API calls

### JWT Utilities
Located in: `backend/app/core/jwt_utils.py`
- Token verification functions
- User ID extraction
- Expiration checking
- Access validation

## Environment Variables
- `BETTER_AUTH_SECRET`: Shared secret for JWT signing/verification
- `BETTER_AUTH_URL`: Better Auth service URL
- `NEXT_PUBLIC_API_BASE_URL`: Backend API base URL

## Testing Considerations
- Test token validation with valid/invalid tokens
- Test user ID mismatch scenarios
- Test expired token handling
- Test cross-service authentication flow
- Verify user isolation between different users