# Quickstart Guide: Security Integration (Better Auth + FastAPI JWT Bridge)

## Prerequisites

- Python 3.12+ installed
- Node.js 18+ installed
- Access to the project repository with backend and frontend directories

## Setup Environment

### 1. Set up Backend Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn sqlmodel pydantic pyjwt python-dotenv
```

### 2. Set up Frontend Environment
```bash
cd frontend
npm init -y
npm install better-auth @better-auth/jwt
```

### 3. Configure Shared Secret
Create `.env` files in both directories with the same secret:

**backend/.env:**
```env
BETTER_AUTH_SECRET=your-super-secret-key-here-make-it-long-and-random
DATABASE_URL=postgresql://...
```

**frontend/.env:**
```env
BETTER_AUTH_SECRET=your-super-secret-key-here-make-it-long-and-random
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

## Implementation Steps

### Step 1: Create Authentication Utilities
Create `backend/src/auth_utils.py` with JWT validation logic:

```python
import jwt
import os
from typing import Optional
from fastapi import HTTPException, Request
from dotenv import load_dotenv

load_dotenv()

BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")
if not BETTER_AUTH_SECRET:
    raise ValueError("BETTER_AUTH_SECRET environment variable is required")

def verify_jwt_token(token: str) -> Optional[dict]:
    """
    Verify JWT token and return payload if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def validate_user_access(token_payload: dict, url_user_id: str) -> bool:
    """
    Validate that the user ID in the token matches the user ID in the URL
    """
    token_user_id = token_payload.get("sub") or token_payload.get("userId")
    return str(token_user_id) == str(url_user_id)
```

### Step 2: Create Authentication Middleware
Add middleware to your FastAPI app:

```python
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from src.auth_utils import verify_jwt_token, validate_user_access
import re

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Define protected routes pattern
        protected_routes = [r"/api/([^/]+)/.*"]

        is_protected = False
        url_user_id = None

        for pattern in protected_routes:
            match = re.match(pattern, request.url.path)
            if match:
                is_protected = True
                url_user_id = match.group(1)
                break

        if is_protected:
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Missing or invalid authorization header"}
                )

            token = auth_header.split(" ")[1]

            try:
                # Verify JWT token
                token_payload = verify_jwt_token(token)

                # Validate user access to the specific user_id
                if not validate_user_access(token_payload, url_user_id):
                    return JSONResponse(
                        status_code=403,
                        content={"detail": "Access forbidden: user ID mismatch"}
                    )

                # Add user info to request state for downstream handlers
                request.state.user_id = token_payload.get("sub")
                request.state.is_authenticated = True

            except HTTPException as e:
                return JSONResponse(
                    status_code=e.status_code,
                    content={"detail": e.detail}
                )

        response = await call_next(request)
        return response
```

### Step 3: Integrate Middleware in Main App
In your `main.py`:

```python
from fastapi import FastAPI
from src.auth_utils import AuthMiddleware

app = FastAPI()
app.add_middleware(AuthMiddleware)

# Your existing API routes...
@app.get("/api/{user_id}/tasks")
async def get_tasks(user_id: str, request: Request):
    # Authentication already verified by middleware
    # user_id in token matches user_id in URL
    # Proceed with business logic...
```

### Step 4: Configure Better Auth in Frontend
Create auth config in frontend:

```typescript
// frontend/src/lib/auth.ts
import { betterAuth } from "better-auth";
import { jwt } from "@better-auth/jwt";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "",
  plugins: [
    jwt({
      secret: process.env.BETTER_AUTH_SECRET || "",
      expiresIn: "7d",
    })
  ]
});
```

## Testing the Setup

### 1. Test Valid Request
```bash
# Get a valid JWT token from Better Auth (via login/register)
# Then make API request:
curl -H "Authorization: Bearer <valid-jwt-token>" \
     http://localhost:8000/api/<user-id>/tasks
```

### 2. Test Invalid Token
```bash
curl -H "Authorization: Bearer invalid-token" \
     http://localhost:8000/api/<user-id>/tasks
# Should return 401 Unauthorized
```

### 3. Test User ID Mismatch
```bash
curl -H "Authorization: Bearer <valid-token-for-user-a>" \
     http://localhost:8000/api/<user-b-id>/tasks
# Should return 403 Forbidden
```

### 4. Test Missing Token
```bash
curl http://localhost:8000/api/<user-id>/tasks
# Should return 401 Unauthorized
```

## Troubleshooting

### Common Issues:
1. **401 errors**: Check that BETTER_AUTH_SECRET is the same in both frontend and backend .env files
2. **403 errors**: Verify that the user_id in JWT token matches the user_id in the URL
3. **JWT decoding errors**: Ensure tokens are properly formatted and not expired

### Debugging Steps:
1. Verify environment variables are loaded correctly
2. Check JWT token format and validity
3. Confirm that Better Auth is issuing tokens with expected structure
4. Review middleware route matching patterns