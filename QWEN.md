# spiral-archives Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-09-24

## Active Technologies
- Python 3.13.7 + FastAPI, SQLAlchemy, Alembic, pytest, uvicorn (001-the-correct-way)

## Project Structure
```
src/
tests/
```

## Commands
cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style
Python 3.11: Follow standard conventions

## Recent Changes
- 001-the-correct-way: Added Python 3.13.7 (this is the latest stable version) + FastAPI, SQLAlchemy, Alembic, pytest, uvicorn

<!-- MANUAL ADDITIONS START -->
# Validation Loop Process

## Step 1: Ruff Linter Check

- Run `python -m ruff check .` to find code quality issues
- Fix all warnings and errors.

## Step 2: MyPy Type Checking

- Run `python -m mypy src/` to check type annotations
- Fix missing return types, untyped decorators, etc.

## Step 3: Black Formatting

- Run `python -m black --check .` to verify formatting
- Auto-fix with `python -m black .` if issues found
- Fix manually because when you introduce errors you need to fix them yourself, not autofix

## Step 4: Pre-commit Validation

- Run `pre-commit run --all-files` to test all hooks
- Fix any remaining issues

## Step 5: Repeat Until Clean

- Loop through steps 1-4 until no errors remain

## Rules

Do not execute terminal commands without providing at least 1 sentence explanation about what you're doing, this includes writing "validation step #1: "

- All python code must include inline Python "docstring" documentation.
- pass lint checks without workarounds
<!-- MANUAL ADDITIONS END -->