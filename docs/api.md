# Spiral Archives API Documentation

## Overview
The Spiral Archives API provides endpoints for managing feature specifications, implementation plans, and task generation in a spec-driven development workflow.

## Base URL
`http://localhost:8000` (default)

## Authentication
The API uses a shared secret token for authentication (optional, enabled via environment variable).

## Endpoints

### POST /specify
Creates a new feature specification based on a user-provided description.

#### Request
```json
{
  "feature_description": "string (required)"
}
```

#### Response (200)
```json
{
  "branch_name": "string",
  "spec_file_path": "string",
  "status": "specification created"
}
```

#### Validation
- feature_description must be provided and non-empty
- feature_description must not exceed 500 characters

### POST /plan
Generates an implementation plan based on the feature specification.

#### Request
No request body required.

#### Response (200)
```json
{
  "plan_file_path": "string",
  "status": "implementation plan created",
  "artifacts": ["research.md", "data-model.md", "quickstart.md"]
}
```

### POST /tasks
Generates a task list based on the implementation plan.

#### Request
No request body required.

#### Response (200)
```json
{
  "tasks_file_path": "string",
  "status": "tasks generated",
  "task_count": "integer"
}
```

## Error Handling
All endpoints return appropriate HTTP status codes:
- 200/201: Success
- 400: Bad request (validation error)
- 401: Unauthorized (if authentication enabled)
- 404: Not found
- 500: Internal server error

## Environment Variables
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `SECURE_ENDPOINTS`: Enable authentication ("true" or "false", defaults to "false")
- `SHARED_SECRET`: Authentication token (if authentication enabled)
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins for CORS (defaults to "*")