"""
User model for authentication and task ownership.
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class User(SQLModel, table=True):
    """
    User database model.

    Represents a user account in the system.
    Each user can have multiple tasks.
    """

    __tablename__ = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique user identifier (UUID)"
    )

    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        description="User email address (unique)"
    )

    password_hash: str = Field(
        max_length=255,
        description="Bcrypt hashed password"
    )

    name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="User display name"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "name": "John Doe",
                "created_at": "2024-01-15T10:30:00Z"
            }
        }
