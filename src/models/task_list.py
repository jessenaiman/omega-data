from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class TaskList(Base):
    __tablename__ = "task_lists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feature_id = Column(UUID(as_uuid=True), nullable=False)  # Reference to feature
    task_id = Column(String, nullable=False)  # Unique identifier for the task
    description = Column(Text, nullable=False)  # Description of the task
    phase = Column(String)  # Which phase the task belongs to
    dependencies = Column(JSONB, default=[])  # List of dependent tasks
    parallelizable = Column(Boolean, default=False)  # Whether task can be run in parallel
    created_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Not Started")  # Not Started, In Progress, Complete
    
    def __repr__(self):
        return f"<TaskList(task_id={self.task_id}, feature_id={self.feature_id}, status={self.status})>"