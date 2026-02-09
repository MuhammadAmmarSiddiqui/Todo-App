# Data Model: Security Integration (Better Auth + FastAPI JWT Bridge)

## JWT Token

**Entity**: JWT Token
**Description**: Self-contained credential containing user identity and metadata, signed with shared secret

### Fields
- `sub` (string): Subject identifier (user ID)
- `iat` (number): Issued at timestamp
- `exp` (number): Expiration timestamp
- `jti` (string): JWT ID (optional)
- Additional claims as needed by Better Auth

### Relationships
- Belongs to: User Identity
- Verified by: Authentication Middleware

### Validation Rules
- Must have valid signature using shared BETTER_AUTH_SECRET
- Must not be expired (check exp field)
- Sub field must match user_id in URL path

## User Identity

**Entity**: User Identity
**Description**: Core entity representing authenticated users with unique identifiers used for access control

### Fields
- `id` (string): Unique user identifier
- `email` (string): User email address
- `name` (string): User display name (optional)
- `createdAt` (datetime): Account creation timestamp

### Relationships
- Issues: JWT Token (via Better Auth)
- Verified by: Authentication Middleware
- Associated with: Tasks (via user_id foreign key)

### Validation Rules
- ID must be non-empty string
- Email must be valid email format
- ID must match between JWT token and URL path

## Authentication Middleware

**Entity**: Authentication Middleware
**Description**: Interceptor component that validates requests before reaching business logic

### Properties
- `secret`: Shared BETTER_AUTH_SECRET for JWT verification
- `algorithm`: HS256 algorithm for signature verification
- `errorHandling`: Strategy for different authentication failures

### Relationships
- Validates: JWT Token
- Protects: API endpoints matching '/api/{user_id}/*' pattern
- Enriches: Request with user context

### State Transitions
- Request received → Extract JWT → Verify signature → Validate user_id → Allow/Reject

## API Request Context

**Entity**: API Request Context
**Description**: Runtime context containing authentication state for processing requests

### Fields
- `user_id` (string): Verified user identifier from JWT
- `is_authenticated` (boolean): Whether request passed auth validation
- `auth_error` (string): Error message if authentication failed

### Relationships
- Created by: Authentication Middleware
- Consumed by: Business logic endpoints
- Derived from: JWT Token validation

### Validation Rules
- user_id must be populated for authenticated requests
- is_authenticated must be True for user_id to be trusted