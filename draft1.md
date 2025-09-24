Excellent. You want to **connect your scene flow directly to a persistent API** that can **save and load player progress**—so that if the player quits after Scene 6, they can resume exactly where they left off.

Here’s a **complete, integrated plan** that:

- Uses your **existing scene flow** (Scenes 1–11)  
- Adds **two lightweight API endpoints**: `POST /save` and `GET /load`  
- Stores **full scene state** (party, HP, choices, current scene)  
- Works with your **SQLAlchemy + Alembic** backend  
- Is **demo-ready today**, scalable tomorrow

---

## 🔗 Core Idea: Scene State = Save Payload

At any point, your UI holds a **state object** like:

```python
current_state = {
    "scene_index": 6,
    "party_name": "Aether’s Chosen",
    "heroes": [
        {"name": "Aether", "class": "scribe", "hp": 70},
        {"name": "Kael", "class": "fighter", "hp": 120},
        ...
    ],
    "symbol_choice": "chaos",
    "choices": {
        "scene8": None  # not reached yet
    }
}
```

Your API will **save this** and **restore it**.

---

## 🌐 API Endpoints (Minimal & Focused)

### `POST /api/v1/save`
> Save current game state

**Request**:
```json
{
  "session_id": "shard-472-demo",
  "state": { ... }  // full state object
}
```

**Response**:
```json
{ "status": "saved", "scene_index": 6 }
```

---

### `GET /api/v1/load/{session_id}`
> Load saved state

**Response**:
```json
{
  "session_id": "shard-472-demo",
  "state": { ... }
}
```

If not found → `404`

---

## 🗃️ Database Integration (SQLAlchemy Models)

You already have `Party` and `NarrativeLog`. Now add **one table** to track **scene progress**:

### Updated `Party` Model (from your Alembic setup)

```python
# app/models.py (enhanced)
class Party(Base):
    __tablename__ = "parties"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String, unique=True, nullable=False)  # "shard-472-demo"
    name = Column(String, nullable=False)
    heroes = Column(JSON, nullable=False)      # full hero list with HP
    symbol_choice = Column(String, nullable=True)
    scene_index = Column(Integer, default=1)   # ← KEY FIELD
    choices = Column(JSON, default=dict)       # {"scene8": "fight"}
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

> ✅ This stores **everything needed to resume**.

---

## 🔄 Save Logic (FastAPI Endpoint)

```python
# api/routes.py
from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models import Party
import uuid

router = APIRouter()

@router.post("/api/v1/save")
def save_game(payload: dict):
    session_id = payload["session_id"]
    state = payload["state"]

    db = SessionLocal()
    party = db.query(Party).filter(Party.session_id == session_id).first()

    if not party:
        # Create new party on first save
        party = Party(
            session_id=session_id,
            name=state["party_name"],
            heroes=state["heroes"],
            symbol_choice=state.get("symbol_choice"),
            scene_index=state["scene_index"],
            choices=state.get("choices", {})
        )
        db.add(party)
    else:
        # Update existing
        party.name = state["party_name"]
        party.heroes = state["heroes"]
        party.symbol_choice = state.get("symbol_choice")
        party.scene_index = state["scene_index"]
        party.choices = state.get("choices", {})
    
    db.commit()
    db.refresh(party)
    return {"status": "saved", "scene_index": party.scene_index}
```

---

## 🔁 Load Logic

```python
@router.get("/api/v1/load/{session_id}")
def load_game(session_id: str):
    db = SessionLocal()
    party = db.query(Party).filter(Party.session_id == session_id).first()
    
    if not party:
        raise HTTPException(status_code=404, detail="No saved game")
    
    return {
        "session_id": session_id,
        "state": {
            "scene_index": party.scene_index,
            "party_name": party.name,
            "heroes": party.heroes,
            "symbol_choice": party.symbol_choice,
            "choices": party.choices
        }
    }
```

---

## 🎮 UI Integration (Pseudocode)

In your Python UI app (Textual, PyGame, etc.):

```python
SESSION_ID = "shard-472-demo"

# On app start
try:
    resp = requests.get(f"http://localhost:8000/api/v1/load/{SESSION_ID}")
    self.state = resp.json()["state"]
    jump_to_scene(self.state["scene_index"])
except:
    self.state = new_game_state()  # start at Scene 1

# After any meaningful choice (e.g., Scene 6 symbol pick)
self.state["scene_index"] = 6
self.state["symbol_choice"] = "chaos"
requests.post("http://localhost:8000/api/v1/save", json={
    "session_id": SESSION_ID,
    "state": self.state
})
```

---

## 🧪 Demo Workflow

1. Player plays through Scene 1 → 6  
2. Chooses Chaos symbol → UI calls `POST /save`  
3. Closes app  
4. Reopens → UI calls `GET /load` → jumps to Scene 6 with HP=70, symbol=Chaos  
5. Continues to Scene 7, 8, etc.

---

## 🛠️ Alembic Migration (Add `session_id` and `choices`)

If you already ran the initial migration, create a new one:

```bash
alembic revision --autogenerate -m "add session_id and choices to parties"
```

Alembic will detect the new columns and generate the upgrade script.

---

## ✅ Why This Works

- **Minimal API**: Only 2 endpoints  
- **Full fidelity**: Save/restore exact state  
- **SQL-backed**: Safe, queryable, scalable  
- **Demo-ready**: Use `session_id = "shard-472-demo"` hardcoded  
- **Future-proof**: Add `user_id` later for accounts

---

Would you like:
- A complete `main.py` FastAPI app with these routes?
- A Textual UI snippet that auto-saves after each scene?
- A script to pre-load your demo party for testing?

This turns your scene flow into a **resumable, persistent experience**—exactly what a pitch demo needs.