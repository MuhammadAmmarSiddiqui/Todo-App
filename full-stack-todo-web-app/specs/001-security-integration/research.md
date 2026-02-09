# Research Findings: Security Integration (Better Auth + FastAPI JWT Bridge)

## Authentication Architecture Sketch

```
Client Request -> Authorization: Bearer <JWT_TOKEN> -> FastAPI App
                    ↓
            Authentication Middleware
                    ↓
         JWT Decode & Verify (HS256 + SECRET)
                    ↓
         Extract User Claims (user_id, etc.)
                    ↓
         Compare URL user_id vs Token user_id
                    ↓
         Allow Request / Return 401 / Return 403
```

## Better Auth JWT Plugin Configuration

### Current Better Auth JWT Support
- Better Auth supports JWT tokens through its built-in JWT plugin
- Configuration requires enabling `jwt` option in the auth config
- Uses HS256 algorithm by default with the same `secret` as session tokens
- Token contains user information like id, email, name

### Sample Configuration
```typescript
import { betterAuth } from "better-auth";
import { jwt } from "@better-auth/jwt";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET, // Same secret for both session and JWT
  plugins: [
    jwt({
      secret: process.env.BETTER_AUTH_SECRET, // Explicit JWT secret
      expiresIn: "7d", // Token expiry time
    })
  ]
});
```

## Architectural Decision Research

### 1. Token Verification: Verify JWT in every request vs. caching verified sessions

**Decision**: Verify JWT in every request
**Rationale**:
- Maintains security by validating token integrity on each request
- Prevents issues with revoked tokens that would persist in a cache
- Aligns with stateless authentication principle from spec
- Simple implementation without managing cache invalidation

**Alternatives considered**:
- Caching verified sessions: Reduces latency but introduces complexity with cache invalidation and potential security risks
- Hybrid approach: Still requires verification for cache misses, adding complexity

### 2. Middleware Placement: Global middleware vs. APIRouter dependencies

**Decision**: Global middleware (BaseHTTPMiddleware)
**Rationale**:
- Ensures all requests are authenticated uniformly
- Matches requirement to intercept all routes matching '/api/{user_id}/*' pattern
- Centralized location for authentication logic
- Simpler to maintain and reason about

**Alternatives considered**:
- APIRouter dependencies: Would require adding dependency to each router, more verbose
- Decorator pattern: Would need to annotate each endpoint individually, more maintenance

### 3. Error Responses: Detailed auth error messages vs. generic 'Unauthorized'

**Decision**: Generic 'Unauthorized' responses
**Rationale**:
- Prevents information disclosure about user existence
- Follows security best practices to not distinguish between different types of failures
- Makes it harder for attackers to enumerate users or understand system internals
- Aligns with security-first approach from spec

**Alternatives considered**:
- Detailed error messages: Helpful for debugging but potentially leak information to attackers

## JWT Handshake Process

### Frontend (Better Auth) Side
1. User authenticates via login/register
2. Better Auth creates JWT token with user information
3. Token stored in httpOnly cookie or localStorage (depending on config)
4. Token included in Authorization header for API requests

### Backend (FastAPI) Side
1. Request received by authentication middleware
2. Extract JWT from Authorization: Bearer <token> header
3. Verify JWT signature using shared BETTER_AUTH_SECRET
4. Decode JWT payload to extract user information
5. Compare user_id in token with user_id in URL path
6. Allow request or return appropriate error (401/403)

## Middleware Flow-Control Structure

```python
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Extract JWT from Authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid authorization header"}
            )

        token = auth_header.split(" ")[1]

        try:
            # Verify JWT using PyJWT with shared secret
            payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])
            user_id_from_token = payload.get("userId") or payload.get("sub")

            # Extract user_id from URL path
            url_user_id = extract_user_id_from_path(request.url.path)

            # Verify user_id in token matches user_id in URL
            if str(user_id_from_token) != str(url_user_id):
                return JSONResponse(
                    status_code=403,
                    content={"detail": "Access forbidden: user ID mismatch"}
                )

            # Add user info to request state for downstream handlers
            request.state.user_id = user_id_from_token

        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token has expired"}
            )
        except jwt.InvalidTokenError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"}
            )

        # Continue processing the request
        response = await call_next(request)
        return response
```

## Research on JWT Libraries for Python

### PyJWT (Selected)
- Most popular JWT library for Python
- Supports all required algorithms including HS256
- Simple API for encoding/decoding JWT tokens
- Good documentation and community support
- Compatible with Better Auth JWT format

### Other Options Considered
- python-jose: Good alternative but PyJWT is more widely adopted
- authlib: More comprehensive but overkill for simple JWT verification

## Environment Variables Approach

Both frontend and backend must use the same BETTER_AUTH_SECRET:
- Frontend: Set in `/frontend/.env`
- Backend: Set in `/backend/.env`
- This ensures JWT tokens issued by Better Auth can be validated by FastAPI backend