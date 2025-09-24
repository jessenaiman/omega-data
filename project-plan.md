# **Project Plan: Persistent Scene Flow API with SQLAlchemy and Alembic**

## **1. Objective**

Build a minimal, robust backend service that:
- Exposes two HTTP endpoints: **save scene state** and **load scene state**
- Persists structured game progress using a relational database
- Supports schema evolution via automated migrations
- Integrates cleanly with a separate frontend that renders scenes 1–11 as defined in `scene-flow.md`

The system must be **self-contained**, **resumable**, and **demo-ready**.

---

## **2. Core Requirements**

### **2.1 Data to Persist per Session**
- `session_id` (string, e.g., `"shard-472-demo"`)
- `scene_index` (integer: 1–11)
- `party_name` (string)
- `heroes` (list of objects with `name`, `class`, `hp`)
- `symbol_choice` (string or null)
- `choices` (dictionary mapping scene keys to player decisions, e.g., `{"scene8": "fight"}`)

### **2.2 API Endpoints**
- `POST /api/v1/save`  
  Accepts full session state; creates or updates record.
- `GET /api/v1/load/{session_id}`  
  Returns full session state or 404 if not found.

### **2.3 Storage Guarantees**
- ACID-compliant writes
- Full state recovery on restart
- Schema must support future additions (e.g., generated asset references)

---

## **3. Technology Stack**

> **All dependencies must use the system-installed or latest stable version available at build time. No pinned versions.**

### **3.1 Language & Framework**
- **Python** (latest stable)
- **FastAPI** — for automatic OpenAPI docs, async-ready, minimal boilerplate

### **3.2 ORM & Database**
- **SQLAlchemy** — for declarative model definition and database abstraction
- **Alembic** — for versioned, automated schema migrations
- **PostgreSQL** — primary production database (with JSON and UUID support)  
  *(Fallback: SQLite for local demo mode if PostgreSQL unavailable)*

### **3.3 Database Drivers**
- **psycopg2** (for PostgreSQL)
- *(SQLite requires no external driver)*

### **3.4 Process & Deployment**
- **uvicorn** — ASGI server to run the API
- **Environment variables** — for configuration (`DATABASE_URL`, `ENV`)

---

## **4. Data Model**

A single table `parties` stores all resumable session data:

| Column | Type | Description |
|-------|------|-------------|
| `id` | UUID (primary key) | Internal record ID |
| `session_id` | TEXT (unique) | Public session identifier (e.g., `"shard-472-demo"`) |
| `name` | TEXT | Party name |
| `heroes` | JSON | List of hero objects (`name`, `class`, `hp`) |
| `symbol_choice` | TEXT | Player’s chosen symbol (nullable) |
| `scene_index` | INTEGER | Current scene (1–11) |
| `choices` | JSON | Map of scene decisions |
| `created_at` | TIMESTAMPTZ | Record creation time |
| `updated_at` | TIMESTAMPTZ | Last save time |

> **Note**: Use PostgreSQL `JSONB` in production; SQLite `JSON` in demo.

---

## **5. Migration Strategy**

- Initialize project with **Alembic**
- All schema changes must be made by:
  1. Updating the SQLAlchemy model
  2. Running `alembic revision --autogenerate -m "describe change"`
  3. Reviewing and (if needed) editing the generated script
  4. Applying via `alembic upgrade head`
- The first migration creates the `parties` table.

---

## **6. API Specification**

### **6.1 Save Endpoint**
- **Method**: `POST`
- **Path**: `/api/v1/save`
- **Request Body**:
  ```json
  {
    "session_id": "string",
    "state": {
      "scene_index": "integer",
      "party_name": "string",
      "heroes": "array",
      "symbol_choice": "string|null",
      "choices": "object"
    }
  }
  ```
- **Response (200)**:
  ```json
  { "status": "saved", "scene_index": 6 }
  ```

### **6.2 Load Endpoint**
- **Method**: `GET`
- **Path**: `/api/v1/load/{session_id}`
- **Response (200)**:
  ```json
  {
    "session_id": "string",
    "state": { /* same structure as save */ }
  }
  ```
- **Response (404)**: If no session found

---

## **7. Project Structure**

```
project/
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

---

## **8. Setup & Execution**

### **8.1 Installation**
```bash
pip install -r requirements.txt
```

### **8.2 Database Initialization**
```bash
# Generate initial migration
alembic revision --autogenerate -m "initial"

# Apply to database
alembic upgrade head
```

### **8.3 Run Server**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

> The API will be available at `http://localhost:8000`

---

## **9. Configuration**

- **Database URL**: Set via `DATABASE_URL` environment variable  
  - Example (PostgreSQL): `postgresql://user:pass@localhost/omega`  
  - Example (SQLite): `sqlite:///./omega.db`
- **Default**: `sqlite:///./omega.db` if `DATABASE_URL` not set

---

## **10. Deliverables**

- A running HTTP API with `/api/v1/save` and `/api/v1/load/{id}`
- A migration-ready SQLAlchemy model
- Alembic configured for future schema changes
- Zero hardcoded credentials or paths
- Fully scriptable setup (no manual SQL)

---

## **11. Notes for Implementation Agent**

- Do **not** implement authentication, rate limiting, or logging beyond basics.
- Do **not** interpret game narrative—only store and retrieve the provided state structure.
- Assume the frontend handles all scene rendering and logic.
- Prioritize correctness and simplicity over performance (this is a pitch/demo backend).
- Use environment-based configuration only.

--- 

**End of Plan**