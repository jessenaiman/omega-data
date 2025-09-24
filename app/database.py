from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import urlparse

# Get database URL from environment, default to SQLite for demo
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./omega.db")

# For PostgreSQL URLs, we might need to handle connection pooling
if DATABASE_URL.startswith("postgresql"):
    # Add connection parameters for PostgreSQL if needed
    DATABASE_URL = DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)  # Set echo=True for SQL debugging
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()