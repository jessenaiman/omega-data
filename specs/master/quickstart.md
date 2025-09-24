# Quickstart: Persistent Scene Flow API

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set database URL: `export DATABASE_URL=sqlite:///./omega.db`
3. Initialize database: 
   ```bash
   alembic init alembic
   alembic revision --autogenerate -m "initial"
   alembic upgrade head
   ```
4. Start server: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## Test the API
1. Save a game state:
```bash
curl -X POST "http://localhost:8000/api/v1/save" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session",
    "state": {
      "scene_index": 3,
      "party_name": "Test Party",
      "heroes": [
        {"name": "Hero1", "class": "fighter", "hp": 100}
      ],
      "symbol_choice": "fire",
      "choices": {"scene2": "fight"}
    }
  }'
```

2. Load a game state:
```bash
curl -X GET "http://localhost:8000/api/v1/load/test-session"
```

## Verify Setup
- Check health: `curl http://localhost:8000/health`
- Run tests: `pytest tests/`