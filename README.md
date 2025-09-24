# Spiral Archives API

A persistent scene flow API that saves and loads player progress for interactive narratives.

## Features

- Save and load game state with full scene fidelity
- Persistent storage using SQLAlchemy and PostgreSQL/SQLite
- Alembic for database migrations
- FastAPI for high-performance API endpoints

## Requirements

- Python 3.8+
- PostgreSQL (optional, SQLite used by default)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up database (if using PostgreSQL):
   ```bash
   export DATABASE_URL=postgresql://user:password@localhost/dbname
   ```
   
   Or use default SQLite:
   ```bash
   export DATABASE_URL=sqlite:///./omega.db
   ```

3. Initialize database with Alembic:
   ```bash
   alembic init alembic
   # Create initial migration after updating alembic.ini to point to app.models
   alembic revision --autogenerate -m "initial"
   alembic upgrade head
   ```

4. Start the server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### `POST /api/v1/save`
Save current game state

Request body:
```json
{
  "session_id": "shard-472-demo",
  "state": {
    "scene_index": 6,
    "party_name": "Aether's Chosen",
    "heroes": [
      {"name": "Aether", "class": "scribe", "hp": 70}
    ],
    "symbol_choice": "chaos",
    "choices": {
      "scene8": null
    }
  }
}
```

Response:
```json
{
  "status": "saved",
  "scene_index": 6
}
```

### `GET /api/v1/load/{session_id}`
Load saved state

Response:
```json
{
  "session_id": "shard-472-demo",
  "state": {
    "scene_index": 6,
    "party_name": "Aether's Chosen",
    "heroes": [
      {"name": "Aether", "class": "scribe", "hp": 70}
    ],
    "symbol_choice": "chaos",
    "choices": {
      "scene8": null
    }
  }
}
```

## Project Structure

```
spiral-archives/
├── app/
│   ├── __init__.py
│   ├── models.py          # SQLAlchemy model
│   ├── database.py        # Engine and session setup
│   └── main.py            # FastAPI app + routes
├── alembic/
│   ├── versions/          # Auto-generated migrations
│   └── env.py             # Alembic runtime config
├── alembic.ini            # Alembic settings
├── requirements.txt       # Dependencies (no version pins)
└── README.md
```

## Testing

Run the tests with pytest:
```bash
pytest tests/
```

## Environment Variables

- `DATABASE_URL`: Database connection string (defaults to SQLite)# omega-data
