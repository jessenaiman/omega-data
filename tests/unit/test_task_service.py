import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from src.models.task_list import TaskList
from src.services.task_service import TaskService
import uuid


class TestTaskService:
    
    def setup_method(self):
        # Create a mock database session
        self.mock_db = Mock(spec=Session)
        self.task_service = TaskService(self.mock_db)
    
    def test_create_task(self):
        # Mock the database operations
        expected_task = TaskList(
            id=uuid.uuid4(),
            feature_id=uuid.uuid4(),
            task_id="T001",
            description="Test task",
            phase="setup",
            dependencies=[],
            parallelizable=False,
            status="Not Started"
        )
        self.mock_db.add.return_value = None
        self.mock_db.commit.return_value = None
        self.mock_db.refresh.return_value = None
        
        # Call the method
        feature_id = uuid.uuid4()
        result = self.task_service.create_task(
            feature_id=feature_id,
            task_id="T001",
            description="Test task",
            phase="setup"
        )
        
        # Verify the database was called correctly
        assert self.mock_db.add.called
        assert self.mock_db.commit.called
        assert self.mock_db.refresh.called
        assert result.task_id == "T001"
    
    def test_get_task(self):
        # Create a mock task to return
        mock_task = TaskList(
            id=uuid.uuid4(),
            feature_id=uuid.uuid4(),
            task_id="T001",
            description="Test task",
            phase="setup",
            dependencies=[],
            parallelizable=False,
            status="Not Started"
        )
        
        # Configure the mock to return the task
        self.mock_db.query().filter().first.return_value = mock_task
        
        # Call the method
        result = self.task_service.get_task("T001")
        
        # Verify the result
        assert result is not None
        assert result.task_id == "T001"
        
        # Verify the query was called with correct parameters
        self.mock_db.query().filter.assert_called()
    
    def test_get_tasks_by_feature(self):
        # Create mock tasks to return
        mock_tasks = [
            TaskList(
                id=uuid.uuid4(),
                feature_id=uuid.uuid4(),
                task_id="T001",
                description="Test task 1",
                phase="setup",
                dependencies=[],
                parallelizable=False,
                status="Not Started"
            ),
            TaskList(
                id=uuid.uuid4(),
                feature_id=uuid.uuid4(),
                task_id="T002",
                description="Test task 2",
                phase="development",
                dependencies=["T001"],
                parallelizable=True,
                status="Not Started"
            )
        ]
        
        # Configure the mock to return the tasks
        self.mock_db.query().filter().all.return_value = mock_tasks
        
        # Call the method
        feature_id = uuid.uuid4()
        result = self.task_service.get_tasks_by_feature(feature_id)
        
        # Verify the result
        assert len(result) == 2
        assert result[0].task_id == "T001"
        assert result[1].task_id == "T002"
        
        # Verify the query was called with correct parameters
        self.mock_db.query().filter.assert_called()
    
    def test_update_task(self):
        # Create a mock task to update
        mock_task = TaskList(
            id=uuid.uuid4(),
            feature_id=uuid.uuid4(),
            task_id="T001",
            description="Old description",
            phase="setup",
            dependencies=[],
            parallelizable=False,
            status="Not Started"
        )
        
        # Configure the mock to return the task
        self.mock_db.query().filter().first.return_value = mock_task
        
        # Call the method
        result = self.task_service.update_task(
            "T001",
            description="New description",
            status="In Progress"
        )
        
        # Verify the result and that the database was updated
        assert result is not None
        assert result.description == "New description"
        assert result.status == "In Progress"
        assert self.mock_db.commit.called
    
    def test_delete_task(self):
        # Create a mock task to delete
        mock_task = TaskList(
            id=uuid.uuid4(),
            feature_id=uuid.uuid4(),
            task_id="T001",
            description="Test task",
            phase="setup",
            dependencies=[],
            parallelizable=False,
            status="Not Started"
        )
        
        # Configure the mock to return the task
        self.mock_db.query().filter().first.return_value = mock_task
        
        # Call the method
        result = self.task_service.delete_task("T001")
        
        # Verify the result and that the database was called to delete
        assert result is True
        self.mock_db.delete.assert_called()
        self.mock_db.commit.assert_called()
    
    def test_mark_task_complete(self):
        # Create a mock task to update
        mock_task = TaskList(
            id=uuid.uuid4(),
            feature_id=uuid.uuid4(),
            task_id="T001",
            description="Test task",
            phase="setup",
            dependencies=[],
            parallelizable=False,
            status="Not Started"
        )
        
        # Configure the mock to return the task
        self.mock_db.query().filter().first.return_value = mock_task
        
        # Call the method
        result = self.task_service.mark_task_complete("T001")
        
        # Verify the result and that the status was updated to Complete
        assert result is not None
        assert result.status == "Complete"
        assert self.mock_db.commit.called