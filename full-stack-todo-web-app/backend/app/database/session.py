from sqlmodel import create_engine, Session
from typing import Generator
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL - using environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine with connection pool settings for NeonDB
# pool_pre_ping: Test connections before using them
# pool_recycle: Recycle connections after 300 seconds to avoid SSL timeout
engine = create_engine(
    DATABASE_URL, 
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10
)

def get_session() -> Generator[Session, None, None]:
    """
    Get database session using dependency injection pattern.

    Yields:
        Session: Database session for use in API endpoints
    """
    with Session(engine) as session:
        yield session