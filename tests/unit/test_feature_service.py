import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session
from src.models.feature_specification import FeatureSpecification
from src.services.feature_service import FeatureService
import uuid


class TestFeatureService:
    
    def setup_method(self):
        # Create a mock database session
        self.mock_db = Mock(spec=Session)
        self.feature_service = FeatureService(self.mock_db)
    
    def test_create_feature_specification(self):
        # Mock the database operations
        expected_feature = FeatureSpecification(
            id=uuid.uuid4(),
            name="Test Feature",
            description="Test Description",
            status="Draft"
        )
        self.mock_db.add.return_value = None
        self.mock_db.commit.return_value = None
        self.mock_db.refresh.return_value = None
        # Configure the mock to return our expected feature with an ID
        self.mock_db.query().filter().first.return_value = None  # For get operation
        
        # Call the method
        result = self.feature_service.create_feature_specification(
            name="Test Feature", 
            description="Test Description"
        )
        
        # Verify the database was called correctly
        assert self.mock_db.add.called
        assert self.mock_db.commit.called
        assert self.mock_db.refresh.called
    
    def test_get_feature_specification(self):
        # Create a mock feature to return
        mock_feature = FeatureSpecification(
            id=uuid.uuid4(),
            name="Test Feature",
            description="Test Description",
            status="Draft"
        )
        
        # Configure the mock to return the feature
        self.mock_db.query().filter().first.return_value = mock_feature
        
        # Call the method
        feature_id = uuid.uuid4()
        result = self.feature_service.get_feature_specification(feature_id)
        
        # Verify the result
        assert result is not None
        assert result.name == "Test Feature"
        
        # Verify the query was called with correct parameters
        self.mock_db.query().filter.assert_called()
    
    def test_update_feature_specification(self):
        # Create a mock feature to update
        mock_feature = FeatureSpecification(
            id=uuid.uuid4(),
            name="Old Name",
            description="Old Description",
            status="Draft"
        )
        
        # Configure the mock to return the feature
        self.mock_db.query().filter().first.return_value = mock_feature
        
        # Call the method
        feature_id = uuid.uuid4()
        result = self.feature_service.update_feature_specification(
            feature_id, 
            name="New Name", 
            description="New Description"
        )
        
        # Verify the result and that the database was updated
        assert result is not None
        assert result.name == "New Name"
        assert result.description == "New Description"
        assert self.mock_db.commit.called
    
    def test_delete_feature_specification(self):
        # Create a mock feature to delete
        mock_feature = FeatureSpecification(
            id=uuid.uuid4(),
            name="Test Feature",
            description="Test Description",
            status="Draft"
        )
        
        # Configure the mock to return the feature
        self.mock_db.query().filter().first.return_value = mock_feature
        
        # Call the method
        feature_id = uuid.uuid4()
        result = self.feature_service.delete_feature_specification(feature_id)
        
        # Verify the result and that the database was called to delete
        assert result is True
        self.mock_db.delete.assert_called()
        self.mock_db.commit.assert_called()