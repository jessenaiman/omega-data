from sqlalchemy.orm import Session
from src.models.task_list import TaskList
import uuid
from typing import Optional, List, Dict, Any


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, feature_id: uuid.UUID, task_id: str, description: str, 
                    phase: str = None, dependencies: List[str] = None, 
                    parallelizable: bool = False) -> TaskList:
        """
        Create a new task
        """
        if dependencies is None:
            dependencies = []
        
        task = TaskList(
            feature_id=feature_id,
            task_id=task_id,
            description=description,
            phase=phase,
            dependencies=dependencies,
            parallelizable=parallelizable,
            status="Not Started"
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task(self, task_id: str) -> Optional[TaskList]:
        """
        Retrieve a task by ID
        """
        return self.db.query(TaskList).filter(
            TaskList.task_id == task_id
        ).first()

    def get_tasks_by_feature(self, feature_id: uuid.UUID) -> List[TaskList]:
        """
        Retrieve all tasks for a feature
        """
        return self.db.query(TaskList).filter(
            TaskList.feature_id == feature_id
        ).all()

    def update_task(self, task_id: str, **kwargs) -> Optional[TaskList]:
        """
        Update a task
        """
        task = self.get_task(task_id)
        if task:
            for key, value in kwargs.items():
                setattr(task, key, value)
            self.db.commit()
            self.db.refresh(task)
        return task

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task
        """
        task = self.get_task(task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
            return True
        return False

    def mark_task_complete(self, task_id: str) -> Optional[TaskList]:
        """
        Mark a task as complete
        """
        return self.update_task(task_id, status="Complete")