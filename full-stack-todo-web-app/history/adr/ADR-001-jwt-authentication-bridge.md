# ADR-001: JWT Authentication Bridge Between Better Auth and FastAPI

## Status
Proposed

## Date
2026-02-02

## Context
We need to implement a secure authentication mechanism that bridges Better Auth (frontend) and FastAPI backend. The core requirement is to ensure that JWT tokens issued by Better Auth can be validated by the FastAPI backend using a shared secret. This enables user isolation where each user only accesses their own data based on the user_id in the URL path.

The challenge is that Better Auth runs on the frontend while our FastAPI backend is a separate service. We need to establish trust between these services without requiring database lookups for every request.

## Decision
We will implement a JWT-based authentication bridge using these components:

**Token Strategy**: Use HS256 algorithm with a shared BETTER_AUTH_SECRET between frontend and backend
- Better Auth will be configured with JWT plugin to issue tokens
- FastAPI backend will validate tokens using PyJWT library
- Tokens will contain user identity claims (user_id, email, etc.)

**Validation Approach**: Verify JWT in every request (stateless authentication)
- Each API request will be intercepted by authentication middleware
- JWT signature will be verified using shared secret
- User identity will be extracted from token claims
- User ID in token will be compared with user ID in URL path

**Middleware Implementation**: Use FastAPI's BaseHTTPMiddleware as global interceptor
- Middleware will process all requests matching '/api/{user_id}/*' pattern
- Extract JWT from Authorization: Bearer <token> header
- Validate token and enforce user isolation
- Add authenticated user context to request state

**Error Handling**: Return generic unauthorized responses to prevent information disclosure
- 401 Unauthorized for invalid/missing tokens
- 403 Forbidden for user ID mismatches
- Generic error messages without specific details

## Consequences

### Positive
- Stateless authentication without database lookups for each request
- Strong user isolation preventing cross-user data access
- Consistent authentication across all API endpoints
- Security through generic error responses that don't leak information
- Scalable solution without session management overhead

### Negative
- Slight performance overhead for each request due to JWT validation
- Tokens remain valid until expiration even if user is deactivated
- Requires careful secret management across frontend and backend
- Potential complexity in token refresh/rotation strategies

## Alternatives
1. **Session-based authentication**: Store session data in database/cache and validate on each request
   - Pros: Immediate invalidation possible, simpler token management
   - Cons: Requires database/cache lookups for each request, breaks stateless principle

2. **API Key authentication**: Issue unique API keys to each user
   - Pros: Simple to implement, immediate revocation possible
   - Cons: Less standardized than JWT, requires key storage and management

3. **OAuth 2.0 with custom authorization server**: Implement full OAuth flow
   - Pros: Industry standard, rich feature set, excellent security model
   - Cons: Significant implementation complexity, overkill for this use case

## References
- `/specs/001-security-integration/plan.md`
- `/specs/001-security-integration/research.md`
- `/specs/001-security-integration/data-model.md`
- `/specs/001-security-integration/contracts/api-contract.yaml`