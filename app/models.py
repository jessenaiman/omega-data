from sqlalchemy import Column, Integer, String, DateTime, JSON, UUID, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid

Base = declarative_base()

class Party(Base):
    __tablename__ = "parties"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String, unique=True, nullable=False)  # "shard-472-demo"
    name = Column(String, nullable=False)
    heroes = Column(JSON, nullable=False)      # full hero list with HP
    symbol_choice = Column(String, nullable=True)
    scene_index = Column(Integer, default=1)   # ← KEY FIELD
    choices = Column(JSON, default=dict)       # {"scene8": "fight"}
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())