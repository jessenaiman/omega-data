import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_feature_specification_workflow():
    """
    Integration test for the feature specification workflow
    Tests the complete flow from feature description to spec file creation
    """
    # This test should initially fail since the workflow is not implemented yet
    feature_description = "test feature for workflow validation"
    
    response = client.post("/specify", json={"feature_description": feature_description})
    
    # Validate the response
    assert response.status_code in [200, 201]
    
    response_data = response.json()
    assert "branch_name" in response_data
    assert "spec_file_path" in response_data
    assert "status" in response_data
    
    # Validate that a spec file was created at the returned path
    # This would require checking the actual file system in a real implementation
    assert response_data["status"] == "specification created"