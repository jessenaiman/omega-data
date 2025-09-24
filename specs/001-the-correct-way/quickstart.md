# Quickstart: The Correct Way Implementation

## Setup
1. Ensure Python 3.11+ is installed
2. Navigate to project root: `cd /path/to/project`
3. Install dependencies: `pip install -r requirements.txt`
4. Create a new feature: `/specify "your feature description"`
5. Generate implementation plan: `/plan`
6. Create tasks: `/tasks`
7. Execute tasks following constitutional principles

## Creating a New Feature
1. Run `/specify "feature description"` to create feature spec
2. System generates branch name and spec file
3. Feature specification follows template with user scenarios and requirements
4. Specification must pass review checklist before proceeding

## Running the Implementation Workflow
1. After creating your feature specification, run `/plan` to generate implementation plan
2. The plan includes:
   - Technical context (language, dependencies, storage, etc.)
   - Constitution check to ensure compliance
   - Project structure recommendation
   - Phase-by-phase implementation approach
3. Generate tasks with `/tasks` command
4. Execute tasks with appropriate tests before implementation (TDD approach)

## Running Tests
1. Unit tests: `pytest tests/unit/`
2. Contract tests: `pytest tests/contract/`
3. Integration tests: `pytest tests/integration/`
4. All tests should pass before merging

## Environment Configuration
- Set `DATABASE_URL` for database connection (defaults to SQLite)
- Set `ENV` to dev/staging/prod for different environments
- All configuration via environment variables as per constitution

## Verification
- Check your implementation follows the constitution principles
- Ensure all required artifacts are generated (research.md, data-model.md, quickstart.md, contracts/)
- Run all tests to verify functionality
- Confirm implementation follows the spec-driven approach