import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from src.models.implementation_plan import ImplementationPlan
from src.services.planning_service import PlanningService
import uuid


class TestPlanningService:
    
    def setup_method(self):
        # Create a mock database session
        self.mock_db = Mock(spec=Session)
        self.planning_service = PlanningService(self.mock_db)
    
    def test_create_implementation_plan(self):
        # Mock the database operations
        expected_plan = ImplementationPlan(
            id=uuid.uuid4(),
            feature_id=uuid.uuid4(),
            technical_context={"language": "Python"},
            project_structure="single",
            phases=["setup", "development"]
        )
        self.mock_db.add.return_value = None
        self.mock_db.commit.return_value = None
        self.mock_db.refresh.return_value = None
        
        # Call the method
        feature_id = uuid.uuid4()
        result = self.planning_service.create_implementation_plan(
            feature_id=feature_id,
            technical_context={"language": "Python"},
            project_structure="single", 
            phases=["setup", "development"]
        )
        
        # Verify the database was called correctly
        assert self.mock_db.add.called
        assert self.mock_db.commit.called
        assert self.mock_db.refresh.called
    
    def test_get_implementation_plan(self):
        # Create a mock plan to return
        mock_plan = ImplementationPlan(
            id=uuid.uuid4(),
            feature_id=uuid.uuid4(),
            technical_context={"language": "Python"},
            project_structure="single",
            phases=["setup", "development"]
        )
        
        # Configure the mock to return the plan
        self.mock_db.query().filter().first.return_value = mock_plan
        
        # Call the method
        plan_id = uuid.uuid4()
        result = self.planning_service.get_implementation_plan(plan_id)
        
        # Verify the result
        assert result is not None
        assert result.feature_id == mock_plan.feature_id
        
        # Verify the query was called with correct parameters
        self.mock_db.query().filter.assert_called()
    
    def test_get_implementation_plan_by_feature(self):
        # Create a mock plan to return
        mock_plan = ImplementationPlan(
            id=uuid.uuid4(),
            feature_id=uuid.uuid4(),
            technical_context={"language": "Python"},
            project_structure="single",
            phases=["setup", "development"]
        )
        
        # Configure the mock to return the plan
        self.mock_db.query().filter().first.return_value = mock_plan
        
        # Call the method
        feature_id = uuid.uuid4()
        result = self.planning_service.get_implementation_plan_by_feature(feature_id)
        
        # Verify the result
        assert result is not None
        assert result.feature_id == feature_id
        
        # Verify the query was called with correct parameters
        self.mock_db.query().filter.assert_called()
    
    def test_update_implementation_plan(self):
        # Create a mock plan to update
        mock_plan = ImplementationPlan(
            id=uuid.uuid4(),
            feature_id=uuid.uuid4(),
            technical_context={"language": "Python"},
            project_structure="single",
            phases=["setup", "development"]
        )
        
        # Configure the mock to return the plan
        self.mock_db.query().filter().first.return_value = mock_plan
        
        # Call the method
        plan_id = uuid.uuid4()
        new_context = {"language": "Python", "framework": "FastAPI"}
        result = self.planning_service.update_implementation_plan(
            plan_id,
            technical_context=new_context,
            project_structure="web application"
        )
        
        # Verify the result and that the database was updated
        assert result is not None
        assert result.technical_context == new_context
        assert result.project_structure == "web application"
        assert self.mock_db.commit.called
    
    def test_delete_implementation_plan(self):
        # Create a mock plan to delete
        mock_plan = ImplementationPlan(
            id=uuid.uuid4(),
            feature_id=uuid.uuid4(),
            technical_context={"language": "Python"},
            project_structure="single",
            phases=["setup", "development"]
        )
        
        # Configure the mock to return the plan
        self.mock_db.query().filter().first.return_value = mock_plan
        
        # Call the method
        plan_id = uuid.uuid4()
        result = self.planning_service.delete_implementation_plan(plan_id)
        
        # Verify the result and that the database was called to delete
        assert result is True
        self.mock_db.delete.assert_called()
        self.mock_db.commit.assert_called()