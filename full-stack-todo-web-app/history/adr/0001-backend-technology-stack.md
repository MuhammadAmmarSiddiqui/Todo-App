# ADR-0001: Backend Technology Stack

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-01-28
- **Feature:** 001-backend-foundation
- **Context:** Need to establish the foundational technology stack for the FastAPI backend including database driver, session management approach, and user isolation strategy to ensure scalability, security, and maintainability.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

- Database Driver: psycopg2-binary for PostgreSQL connectivity
- Session Management: FastAPI Dependency Injection with context managers
- User Isolation: Filtering via 'user_id' path parameter with internal service logic validation

<!-- For technology stacks, list all components:
     - Framework: Next.js 14 (App Router)
     - Styling: Tailwind CSS v3
     - Deployment: Vercel
     - State Management: React Context (start simple)
-->

## Consequences

### Positive

- Simple setup and debugging for psycopg2-binary with good performance characteristics
- Native FastAPI integration with dependency injection for proper request lifecycle management
- Clear API design with security layer preventing cross-user data access
- Team familiarity with psycopg2-binary reduces development friction

<!-- Example: Integrated tooling, excellent DX, fast deploys, strong TypeScript support -->

### Negative

- Potential performance limitations compared to asyncpg for high-load scenarios
- Additional complexity in managing dependency lifecycles
- Dual validation layer may add slight overhead to API calls
- Possible vendor lock-in to specific PostgreSQL driver

<!-- Example: Vendor lock-in to Vercel, framework coupling, learning curve -->

## Alternatives Considered

- Database Driver: asyncpg was considered but rejected for complexity and team familiarity reasons
- Session Management: Pure context managers were considered but rejected for lack of native FastAPI integration
- User Isolation: Internal service logic only was considered but rejected for lack of clear API design

<!-- Group alternatives by cluster:
     Alternative Stack A: Remix + styled-components + Cloudflare
     Alternative Stack B: Vite + vanilla CSS + AWS Amplify
     Why rejected: Less integrated, more setup complexity
-->

## References

- Feature Spec: specs/001-backend-foundation/spec.md
- Implementation Plan: specs/001-backend-foundation/plan.md
- Related ADRs: none
- Evaluator Evidence: Plan document section 2 on key decisions