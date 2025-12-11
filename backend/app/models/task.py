"""
Task model for todo items.
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class Task(SQLModel, table=True):
    """
    Task database model.

    Represents a todo task owned by a user.
    Each task belongs to one user (user_id foreign key).
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Auto-incrementing task ID"
    )

    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        index=True,
        description="Owner user ID (foreign key)"
    )

    title: str = Field(
        max_length=200,
        description="Task title (required)"
    )

    description: Optional[str] = Field(
        default=None,
        description="Task description (optional)"
    )

    completed: bool = Field(
        default=False,
        index=True,
        description="Task completion status"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Task creation timestamp"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        }
