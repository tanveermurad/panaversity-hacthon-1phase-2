"""
Database connection and session management using SQLModel.
Configured for Neon Serverless PostgreSQL.
"""

from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.pool import NullPool
from app.config import settings


# Ensure SSL mode for Neon
database_url = settings.DATABASE_URL
if "sslmode" not in database_url:
    database_url += "?sslmode=require"

# Create engine with NullPool for serverless
# NullPool is recommended for serverless environments like Neon
engine = create_engine(
    database_url,
    echo=not settings.is_production,  # Log SQL in development
    poolclass=NullPool,  # No connection pooling for serverless
)


def create_db_and_tables():
    """
    Create all tables in the database.
    Should be called on application startup.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency for getting database session.
    Use with FastAPI Depends.

    Example:
        @app.get("/items")
        def get_items(session: Session = Depends(get_session)):
            ...
    """
    with Session(engine) as session:
        yield session
