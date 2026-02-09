# Data Model: Frontend Development & Full Integration

## Entity: User

**Description**: Represents an authenticated user in the system

**Attributes**:
- id: string (unique identifier from Better Auth)
- email: string (email address, validated format)
- name: string (display name, optional)
- createdAt: Date (account creation timestamp)
- updatedAt: Date (last updated timestamp)

**Validation rules**:
- Email must be in valid email format
- Email must be unique across the system
- Name must be 1-50 characters if provided

**State transitions**:
- Unauthenticated → Authenticated (on successful login)
- Authenticated → Unauthenticated (on logout)

## Entity: Task

**Description**: Represents a todo item owned by a specific user

**Attributes**:
- id: string (unique identifier)
- userId: string (foreign key to User.id)
- title: string (task title, required)
- description: string (task description, optional)
- completed: boolean (completion status, default: false)
- createdAt: Date (creation timestamp)
- updatedAt: Date (last updated timestamp)
- completedAt: Date (completion timestamp, optional)

**Validation rules**:
- Title must be 1-200 characters
- Description must be 0-1000 characters if provided
- UserId must correspond to an existing user
- Completed status can only be changed by the owning user

**State transitions**:
- Active → Completed (when user marks task as complete)
- Completed → Active (when user unmarks task as complete)

## Entity: Session

**Description**: Represents the user's authenticated state with JWT token information

**Attributes**:
- userId: string (associated user ID)
- token: string (JWT token)
- expiresAt: Date (token expiration time)
- refreshToken: string (refresh token, optional)
- createdAt: Date (session creation time)

**Validation rules**:
- Token must be valid JWT format
- ExpiresAt must be in the future
- Session must be associated with a valid user

**State transitions**:
- Active → Expired (when token expires)
- Expired → Active (when token is refreshed)

## Relationships

**User → Task** (One-to-Many)
- One user can own many tasks
- Tasks are deleted when user is deleted (cascading delete)
- All tasks must belong to a valid user

**User → Session** (One-to-One/Many)
- One user can have one or more active sessions
- Sessions are invalidated when user logs out or is deleted

## API Data Transfer Objects (DTOs)

### TaskRequest DTO
- title: string (required)
- description: string (optional)
- completed: boolean (optional, default: false)

### TaskResponse DTO
- id: string
- userId: string
- title: string
- description: string
- completed: boolean
- createdAt: Date
- updatedAt: Date
- completedAt: Date (nullable)

### AuthRequest DTO
- email: string (required)
- password: string (required)

### AuthResponse DTO
- user: User object
- token: string
- refreshToken: string (optional)