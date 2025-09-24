from sqlalchemy import Column, Integer, String, DateTime, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class FeatureSpecification(Base):
    __tablename__ = "feature_specifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Draft")  # Draft, Planned, In Progress, Complete
    requirements = Column(ARRAY(String), default=[])
    entities = Column(ARRAY(String), default=[])
    
    def __repr__(self):
        return f"<FeatureSpecification(name={self.name}, status={self.status})>"