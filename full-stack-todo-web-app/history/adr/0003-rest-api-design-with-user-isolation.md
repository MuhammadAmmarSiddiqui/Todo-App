# ADR-0003: REST API Design with User Isolation

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-01-28
- **Feature:** 001-backend-foundation
- **Context:** Need to establish a consistent, secure REST API design that properly isolates user data while maintaining good API ergonomics and following RESTful principles for the todo application.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

- API Pattern: RESTful endpoints with user_id in path parameter
- Resource Structure: /api/{user_id}/tasks/{task_id} for all task operations
- HTTP Methods: Standard CRUD mapping (POST/GET/PUT/DELETE/PATCH)
- User Isolation: Dual-layer validation (path parameter + internal service validation)
- Error Handling: Consistent HTTP status codes and error responses

<!-- For technology stacks, list all components:
     - Framework: Next.js 14 (App Router)
     - Styling: Tailwind CSS v3
     - Deployment: Vercel
     - State Management: React Context (start simple)
-->

## Consequences

### Positive

- Clear API design with explicit user identification in URLs
- Consistent endpoint patterns across all operations
- Strong security with dual-layer validation preventing cross-user access
- Follows RESTful conventions familiar to developers
- Easy to understand and document API structure

<!-- Example: Integrated tooling, excellent DX, fast deploys, strong TypeScript support -->

### Negative

- API URLs are longer due to user_id inclusion
- Potential confusion if user tries to access another user's tasks
- Additional complexity in client-side API consumption
- Need for careful validation to prevent user_id manipulation

<!-- Example: Vendor lock-in to Vercel, framework coupling, learning curve -->

## Alternatives Considered

- Global task access without user_id in path: Rejected for security concerns
- Header-based user identification: Rejected for less explicit API design
- Subdomain-based user isolation: Rejected for complexity and DNS requirements
- Single tenant approach: Rejected for not meeting multi-user requirement

<!-- Group alternatives by cluster:
     Alternative Stack A: Remix + styled-components + Cloudflare
     Alternative Stack B: Vite + vanilla CSS + AWS Amplify
     Why rejected: Less integrated, more setup complexity
-->

## References

- Feature Spec: specs/001-backend-foundation/spec.md
- Implementation Plan: specs/001-backend-foundation/plan.md
- Related ADRs: ADR-0001 Backend Technology Stack, ADR-0002 JWT Authentication
- Evaluator Evidence: Plan document section on API contracts and security requirements