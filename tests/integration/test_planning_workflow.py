import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_implementation_planning_workflow():
    """
    Integration test for the implementation planning workflow
    Tests the complete flow from feature spec to plan generation
    """
    # This test should initially fail since the workflow is not implemented yet
    response = client.post("/plan")
    
    # Validate the response
    assert response.status_code in [200, 201]
    
    response_data = response.json()
    assert "plan_file_path" in response_data
    assert "status" in response_data
    assert "artifacts" in response_data
    
    # Validate that required artifacts were created
    expected_artifacts = ["research.md", "data-model.md", "quickstart.md"]
    for artifact in expected_artifacts:
        assert artifact in response_data["artifacts"]
    
    assert response_data["status"] == "implementation plan created"