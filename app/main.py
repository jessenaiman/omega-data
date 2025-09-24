from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Party
from app.database import SessionLocal, engine
from typing import Dict, Any
import os

# Create database tables
from app.models import Base
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Spiral Archives API", version="1.0.0")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/v1/save")
def save_game(payload: Dict[str, Any], db: Session = Depends(get_db)):
    session_id = payload["session_id"]
    state = payload["state"]

    # Try to find existing party
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

@app.get("/api/v1/load/{session_id}")
def load_game(session_id: str, db: Session = Depends(get_db)):
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

@app.get("/health")
def health_check():
    return {"status": "healthy"}