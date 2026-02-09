# ADR-0002: JWT-Based Authentication with Better Auth Integration

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-01-28
- **Feature:** 001-backend-foundation
- **Context:** Need to establish a secure, scalable authentication system that works across both frontend (Next.js) and backend (FastAPI) services while ensuring proper user isolation and stateless authentication.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

- Authentication Provider: Better Auth for frontend authentication management
- Token Strategy: JWT tokens issued by Better Auth for backend verification
- Token Exchange: Bearer token in Authorization header for API requests
- Secret Sharing: Shared BETTER_AUTH_SECRET environment variable between frontend and backend
- User Identification: JWT payload contains user information for backend validation

<!-- For technology stacks, list all components:
     - Framework: Next.js 14 (App Router)
     - Styling: Tailwind CSS v3
     - Deployment: Vercel
     - State Management: React Context (start simple)
-->

## Consequences

### Positive

- Stateless authentication between frontend and backend services
- Automatic token expiry and renewal handling
- Strong security with signed JWT tokens
- Proper user isolation with token-based user identification
- Scalable authentication without shared session state

<!-- Example: Integrated tooling, excellent DX, fast deploys, strong TypeScript support -->

### Negative

- Complexity in token management and validation across services
- Need for secure secret sharing between services
- Potential token size bloat with embedded user information
- Dependency on external authentication provider (Better Auth)

<!-- Example: Vendor lock-in to Vercel, framework coupling, learning curve -->

## Alternatives Considered

- Session-based authentication: Rejected for requiring shared session state between services
- OAuth-only approach: Rejected for lack of flexibility in user management
- Custom token system: Rejected for reinventing established security patterns
- Cookie-based authentication: Rejected for complexity in API consumption from various clients

<!-- Group alternatives by cluster:
     Alternative Stack A: Remix + styled-components + Cloudflare
     Alternative Stack B: Vite + vanilla CSS + AWS Amplify
     Why rejected: Less integrated, more setup complexity
-->

## References

- Feature Spec: specs/001-backend-foundation/spec.md
- Implementation Plan: specs/001-backend-foundation/plan.md
- Related ADRs: ADR-0001 Backend Technology Stack
- Evaluator Evidence: Plan document section on authentication and security requirements