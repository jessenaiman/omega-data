import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import Party

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_save_and_load_game():
    """Test saving and loading game state"""
    # Define test game state
    test_session_id = "test-session-123"
    test_state = {
        "scene_index": 5,
        "party_name": "Test Party",
        "heroes": [
            {"name": "Hero1", "class": "fighter", "hp": 100},
            {"name": "Hero2", "class": "mage", "hp": 80}
        ],
        "symbol_choice": "fire",
        "choices": {"scene3": "fight", "scene4": "run"}
    }
    
    # Save game state
    save_payload = {
        "session_id": test_session_id,
        "state": test_state
    }
    
    response = client.post("/api/v1/save", json=save_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "saved"
    assert response.json()["scene_index"] == 5
    
    # Load game state
    response = client.get(f"/api/v1/load/{test_session_id}")
    assert response.status_code == 200
    
    loaded_data = response.json()
    assert loaded_data["session_id"] == test_session_id
    assert loaded_data["state"]["scene_index"] == 5
    assert loaded_data["state"]["party_name"] == "Test Party"
    assert len(loaded_data["state"]["heroes"]) == 2
    assert loaded_data["state"]["symbol_choice"] == "fire"
    assert loaded_data["state"]["choices"]["scene3"] == "fight"

def test_load_nonexistent_game():
    """Test loading a non-existent game session"""
    response = client.get("/api/v1/load/nonexistent-session")
    assert response.status_code == 404
    assert response.json() == {"detail": "No saved game"}

def test_save_with_minimal_state():
    """Test saving a minimal game state"""
    test_session_id = "minimal-test-456"
    test_state = {
        "scene_index": 1,
        "party_name": "Minimal Party",
        "heroes": [],
        "symbol_choice": None,
        "choices": {}
    }
    
    save_payload = {
        "session_id": test_session_id,
        "state": test_state
    }
    
    response = client.post("/api/v1/save", json=save_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "saved"
    assert response.json()["scene_index"] == 1
    
    # Load and verify
    response = client.get(f"/api/v1/load/{test_session_id}")
    assert response.status_code == 200
    
    loaded_data = response.json()
    assert loaded_data["state"]["scene_index"] == 1
    assert loaded_data["state"]["party_name"] == "Minimal Party"
    assert loaded_data["state"]["symbol_choice"] is None
    assert loaded_data["state"]["choices"] == {}