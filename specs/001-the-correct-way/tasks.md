# Tasks: The Correct Way Implementation

**Input**: Design documents from `/specs/001-the-correct-way/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
   → quickstart.md: Extract scenarios → integration tests
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, API endpoints
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 3.1: Setup
- [x] T001 Create project structure per implementation plan: src/models/, src/services/, src/api/, tests/contract/, tests/integration/, tests/unit/
- [x] T002 Initialize Python project with FastAPI, SQLAlchemy, Alembic, pytest dependencies
- [x] T003 [P] Configure linting and formatting tools (black, flake8, mypy)

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [x] T004 [P] Contract test POST /specify in tests/contract/test_specify_endpoint.py
- [x] T005 [P] Contract test POST /plan in tests/contract/test_plan_endpoint.py
- [x] T006 [P] Contract test POST /tasks in tests/contract/test_tasks_endpoint.py
- [x] T007 [P] Integration test feature specification workflow in tests/integration/test_feature_spec_workflow.py
- [x] T008 [P] Integration test implementation planning workflow in tests/integration/test_planning_workflow.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [x] T009 [P] Feature Specification model in src/models/feature_specification.py
- [x] T010 [P] Implementation Plan model in src/models/implementation_plan.py
- [x] T011 [P] Task List model in src/models/task_list.py
- [x] T012 [P] Feature Service in src/services/feature_service.py
- [x] T013 [P] Planning Service in src/services/planning_service.py
- [x] T014 [P] Task Generation Service in src/services/task_service.py
- [x] T015 POST /specify endpoint in src/api/main.py
- [x] T016 POST /plan endpoint in src/api/main.py
- [x] T017 POST /tasks endpoint in src/api/main.py
- [x] T018 Input validation for all endpoints in src/api/validation.py
- [x] T019 Error handling and logging in src/api/middleware.py

## Phase 3.4: Integration
- [x] T020 Connect Feature Service to database with SQLAlchemy
- [x] T021 Connect Planning Service to database with SQLAlchemy
- [x] T022 Connect Task Generation Service to database with SQLAlchemy
- [x] T023 Auth middleware for securing endpoints
- [x] T024 Request/response logging middleware
- [x] T025 CORS and security headers configuration

## Phase 3.5: Polish
- [x] T026 [P] Unit tests for Feature Service in tests/unit/test_feature_service.py
- [x] T027 [P] Unit tests for Planning Service in tests/unit/test_planning_service.py
- [x] T028 [P] Unit tests for Task Service in tests/unit/test_task_service.py
- [ ] T029 Performance tests (<500ms response time)
- [x] T030 [P] Update docs/api.md with API documentation
- [ ] T031 Remove duplication in codebase
- [ ] T032 Run manual-testing.md to verify workflow

## Dependencies
- Tests (T004-T008) before implementation (T009-T019)
- T009, T010, T011 blocks T012, T013, T014
- T012, T013, T014 blocks T015, T016, T017
- T015, T016, T017 blocks T023
- Implementation before polish (T026-T032)

## Parallel Example
```
# Launch T004-T006 together:
Task: "Contract test POST /specify in tests/contract/test_specify_endpoint.py"
Task: "Contract test POST /plan in tests/contract/test_plan_endpoint.py"
Task: "Contract test POST /tasks in tests/contract/test_tasks_endpoint.py"

# Launch T009-T011 together:
Task: "Feature Specification model in src/models/feature_specification.py"
Task: "Implementation Plan model in src/models/implementation_plan.py"
Task: "Task List model in src/models/task_list.py"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - Each contract file → contract test task [P]
   - Each endpoint → implementation task
   
2. **From Data Model**:
   - Each entity → model creation task [P]
   - Relationships → service layer tasks
   
3. **From User Stories**:
   - Each story → integration test [P]
   - Quickstart scenarios → validation tasks

4. **Ordering**:
   - Setup → Tests → Models → Services → Endpoints → Polish
   - Dependencies block parallel execution

## Validation Checklist
*GATE: Checked by main() before returning*

- [ ] All contracts have corresponding tests
- [ ] All entities have model tasks
- [ ] All tests come before implementation
- [ ] Parallel tasks truly independent
- [ ] Each task specifies exact file path
- [ ] No task modifies same file as another [P] task