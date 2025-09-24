from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class ImplementationPlan(Base):
    __tablename__ = "implementation_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feature_id = Column(UUID(as_uuid=True), nullable=False)  # Reference to feature
    plan_date = Column(DateTime, default=datetime.utcnow)
    technical_context = Column(JSONB)  # Contains language, dependencies, storage, etc.
    project_structure = Column(String)  # Single, web application, or mobile
    phases = Column(JSONB, default=[])  # List of implementation phases
    
    def __repr__(self):
        return f"<ImplementationPlan(feature_id={self.feature_id}, plan_date={self.plan_date})>"