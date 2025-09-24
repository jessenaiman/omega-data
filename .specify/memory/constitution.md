# Spiral Archives Constitution

## Core Principles

### I. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced

### II. API-First Design
All services start with clearly defined API contracts; Contract tests validate request/response schemas; APIs versioned from inception

### III. Database-Backed Persistence
All user state must be stored in a relational database; ACID compliance required for all transactions; Schema migrations versioned with Alembic

### IV. Environment-Based Configuration
All configuration via environment variables; No hardcoded credentials or paths; Support for dev, staging, and production environments

### V. Observability & Simplicity
Structured logging required; Start simple, YAGNI principles; Clear metrics for performance and usage

## Additional Constraints
- Technology stack: Python (FastAPI, SQLAlchemy, Alembic, PostgreSQL)
- Dependencies: Use latest stable versions unless specific constraints apply
- Performance: <500ms response time for all API endpoints
- Security: Input validation for all endpoints, SQL injection protection

## Development Workflow
- Feature development via spec-driven approach (spec → plan → tasks → implementation)
- All code requires contract and integration tests before merging
- Schema changes require Alembic migrations
- Code review required for all changes

## Governance
- Constitution supersedes all other practices
- All PRs/reviews must verify compliance
- Complexity must be justified with clear business value
- Amendments require documentation and approval by senior team members

**Version**: 1.0.0 | **Ratified**: 2025-09-24 | **Last Amended**: 2025-09-24