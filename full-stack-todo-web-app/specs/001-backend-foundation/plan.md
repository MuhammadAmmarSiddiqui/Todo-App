# Implementation Plan: Backend Foundation

## Executive Summary
This plan outlines the implementation of a robust FastAPI backend with SQLModel and Neon PostgreSQL integration, focusing on the Task model and CRUD API endpoints. The architecture emphasizes decoupling, proper session management, and user isolation for a multi-user todo application. This implementation complies with the project constitution requiring strict separation of concerns with distinct /frontend and /backend directories.

## 1. Scope and Dependencies

### In Scope
- FastAPI backend implementation with proper routing
- SQLModel-based Task model with user isolation
- Complete CRUD API endpoints for task management
- Neon PostgreSQL database integration with connection pooling
- JWT-based authentication using Better Auth
- Request validation and response serialization
- Database session management with proper lifecycle
- Error handling with structured responses

### Out of Scope
- Frontend implementation (Next.js)
- Better Auth configuration (handled separately)
- Deployment configuration
- Monitoring and logging infrastructure

### External Dependencies
- Neon Serverless PostgreSQL (managed service)
- Better Auth (authentication provider)
- Python 3.12+ runtime environment
- FastAPI ecosystem (SQLModel, Pydantic, etc.)

## 2. Key Decisions and Rationale

### Database Driver Selection
**Decision**: Use `psycopg2-binary` over `asyncpg`
**Options Considered**:
- `psycopg2-binary`: Simpler setup, stable, widely supported
- `asyncpg`: Higher performance, but requires more complex async handling

**Rationale**: For initial development and team familiarity, `psycopg2-binary` offers simpler setup and debugging while maintaining good performance. The performance difference is negligible for typical todo application loads.

### Session Management Approach
**Decision**: FastAPI Dependency Injection with context managers
**Options Considered**:
- Pure context managers: Simple, but harder to integrate with FastAPI
- FastAPI Dependency Injection: Native to FastAPI, enables proper request lifecycle management
- Hybrid approach: Combines both methods

**Rationale**: FastAPI's dependency injection system is designed specifically for managing request-scoped resources like database sessions. It provides proper lifecycle management and integrates seamlessly with the framework's error handling.

### User Isolation Strategy
**Decision**: Filtering via 'user_id' path parameter with internal service logic
**Options Considered**:
- Path parameter only: Simple but less secure
- Internal service logic only: More secure but harder to maintain
- Combined approach: Both path parameter and internal validation

**Rationale**: Using the user_id in the path provides clear API design while internal service logic adds a security layer preventing users from accessing other users' data even if they somehow manipulate the API.

## 3. Interfaces and API Contracts

### Public APIs
```
POST   /api/{user_id}/tasks           - Create a task
GET    /api/{user_id}/tasks           - List user's tasks
GET    /api/{user_id}/tasks/{id}      - Get specific task
PUT    /api/{user_id}/tasks/{id}      - Update a task
DELETE /api/{user_id}/tasks/{id}      - Delete a task
PATCH  /api/{user_id}/tasks/{id}/complete - Toggle completion
```

**Constitution Compliance**: All endpoints follow the constitution's required pattern of /api/{user_id}/... for proper user isolation and authentication.

### Expected Inputs/Outputs
- **Request Body**: JSON with task properties (title, description, completed)
- **Response Body**: JSON with task object including id, timestamps, and user_id
- **Headers**: Authorization: Bearer {jwt_token}

### Error Responses
- `400 Bad Request`: Invalid request format or validation errors
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: User attempting to access another user's tasks
- `404 Not Found`: Requested task doesn't exist
- `500 Internal Server Error`: Database or system errors

## 4. Non-Functional Requirements

### Performance
- API response time: <200ms for 95th percentile
- Database connection pooling: 5-10 active connections
- Concurrent request handling: Up to 100 simultaneous requests

### Reliability
- API uptime: 99.9% availability
- Database connection resilience: Automatic retry with exponential backoff
- Graceful degradation: Service continues with reduced functionality during partial outages

### Security
- JWT token validation: Verify signature and expiration
- User data isolation: Enforced at both API and service layers
- Input sanitization: All user inputs validated and sanitized
- SQL injection prevention: ORM-based queries only

### Cost
- Database resource optimization: Connection pooling and efficient queries
- Serverless scaling: Leverage Neon's serverless capabilities

## 5. Data Management and Migration

### Source of Truth
- Database schema defined in SQLModel models
- Alembic for migration management
- Neon PostgreSQL as the primary data store

### Schema Evolution
- Version-controlled migrations using Alembic
- Backward-compatible schema changes
- Automated testing for migration validity

### Data Retention
- Soft deletes for audit trail (deleted_at timestamp)
- Periodic cleanup of soft-deleted records (configurable policy)

## 6. Operational Readiness

### Observability
- Structured logging with correlation IDs
- Performance metrics for API endpoints
- Database query performance monitoring
- Error rate tracking

### Alerting
- API error rates exceeding 1%
- Response time degradation (>500ms 95th percentile)
- Database connection pool exhaustion
- Authentication failure spikes

### Deployment
- Container-based deployment (Docker)
- Environment-specific configurations
- Health check endpoints for orchestration

## 7. Risk Analysis and Mitigation

### Top 3 Risks
1. **Database Connection Issues**: Mitigated by connection pooling and retry mechanisms
2. **Authentication Failures**: Mitigated by proper JWT validation and fallback logging
3. **Data Isolation Breaches**: Mitigated by dual-layer validation (API and service)

### Blast Radius
- Authentication issues: Affect all API endpoints
- Database issues: Affect all data operations
- Individual task failures: Limited to specific requests

### Guardrails
- Rate limiting per user
- Input size validation
- Transaction boundaries for data consistency

## 8. Implementation Phases

### Phase 1: Backend Infrastructure Setup
- Set up project structure with proper separation
- Configure virtual environment and dependencies
- Implement database connection and session management
- Create basic FastAPI application structure

### Phase 2: Data Models and Schema
- Define Task model using SQLModel
- Set up database session management
- Implement database initialization and health checks
- Create migration system with Alembic

### Phase 3: Core API Implementation
- Implement JWT token validation middleware
- Create CRUD service layer with user isolation
- Build API endpoints with proper request/response validation
- Add authentication and authorization checks

### Phase 4: Testing and Verification
- Unit tests for service layer
- Integration tests for API endpoints
- Database connectivity and schema validation
- User isolation and security testing

## 9. Architecture Sketch

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │────│  FastAPI         │────│  Neon PostgreSQL│
│   (Next.js)     │    │  (Authentication)│    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                       ┌──────────────────┐
                       │  Service Layer   │
                       │  (User Isolation)│
                       └──────────────────┘
                              │
                       ┌──────────────────┐
                       │  SQLModel        │
                       │  (ORM)           │
                       └──────────────────┘
                              │
                       ┌──────────────────┐
                       │  Database Session│
                       │  (Connection Pool)│
                       └──────────────────┘
```

## 10. Architecture Decision Records (ADRs)

The following significant decisions should be documented in ADRs:
- Database driver selection (psycopg2-binary vs asyncpg)
- Session management approach (DI vs context managers)
- User isolation strategy (path parameter + service logic)

---

This plan provides a comprehensive roadmap for implementing the backend foundation while addressing all architectural considerations and risk factors. The phased approach ensures steady progress with proper validation at each step.