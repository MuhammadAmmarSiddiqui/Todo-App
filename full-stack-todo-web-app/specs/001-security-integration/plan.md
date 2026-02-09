# Implementation Plan: Security Integration (Better Auth + FastAPI JWT Bridge)

**Branch**: `001-security-integration` | **Date**: 2026-02-02 | **Spec**: [link to spec.md]
**Input**: Feature specification from `/specs/001-security-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement JWT-based authentication bridge between Better Auth (frontend) and FastAPI backend. Create authentication middleware that validates JWT tokens from Better Auth using shared secret, enforces user isolation by comparing token claims with URL user_id, and returns appropriate 401/403 responses for unauthorized access attempts. The implementation follows a Trust-But-Verify principle where backend never trusts user_id in URL without verified JWT.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.12+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI (backend), Next.js 16 (frontend), Better Auth, PyJWT, SQLModel
**Storage**: Neon Serverless PostgreSQL (backend)
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Linux server (backend), Web browser (frontend)
**Project Type**: web (determines source structure)
**Performance Goals**: <100ms p95 latency for authenticated requests, sub-100ms overhead for JWT validation
**Constraints**: JWT validation on every request, shared BETTER_AUTH_SECRET between services, user isolation via {user_id} in URL
**Scale/Scope**: Multi-user support with isolated data access, 401/403 error handling for unauthorized access

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Agentic-First Development: All code will be generated via Claude Code agents following Spec-Kit Plus tools
- ✅ Separation of Concerns: Strict isolation between client and server codebases maintained
- ✅ Security-by-Design: Multi-tenant isolation enforced via JWT and ownership checks
- ✅ Source-of-Truth Compliance: Following claude.md and spec.md requirements exactly
- ✅ Technology Stack Adherence: Using Python 3.12+, SQLModel, FastAPI, Next.js 16, Better Auth, JWT strategy
- ✅ REST API Design: Following /api/{user_id}/... structure with proper 401/404 error handling
- ✅ Directory Structure: Maintaining /frontend and /backend separation
- ✅ Environment Constraints: Using local venv and npm within respective directories
- ✅ Authentication Strategy: Implementing shared-secret JWT strategy with BETTER_AUTH_SECRET

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   ├── services/
│   ├── api/
│   └── auth_utils.py
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/
```

**Structure Decision**: Web application structure with separate frontend (Next.js) and backend (FastAPI) directories. Backend will include auth_utils.py for JWT handling and authentication middleware.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
