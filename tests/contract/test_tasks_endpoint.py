import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_tasks_endpoint_contract():
    """
    Contract test for POST /tasks endpoint
    Validates request/response schemas according to contract
    """
    # This test should initially fail since the endpoint is not implemented yet
    response = client.post("/tasks")
    
    # Validate response structure based on contract
    assert response.status_code == 201  # Or 200 depending on implementation
    
    response_data = response.json()
    assert "tasks_file_path" in response_data
    assert "status" in response_data
    assert "task_count" in response_data
    assert response_data["status"] == "tasks generated"
    
    # Validate data types
    assert isinstance(response_data["tasks_file_path"], str)
    assert isinstance(response_data["task_count"], int)