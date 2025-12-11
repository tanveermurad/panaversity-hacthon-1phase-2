"""
Task CRUD API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.db import get_session
from app.models import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from app.middleware import verify_token


router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])


async def verify_user_access(user_id: str, authenticated_user_id: str = Depends(verify_token)):
    """
    Verify that the authenticated user matches the user_id in the path.

    Args:
        user_id: User ID from path parameter
        authenticated_user_id: User ID from JWT token

    Raises:
        403: If user_id doesn't match authenticated user
    """
    if user_id != authenticated_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own tasks"
        )
    return user_id


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    user_id: str,
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    verified_user_id: str = Depends(verify_user_access),
    session: Session = Depends(get_session)
):
    """
    List all tasks for the authenticated user.

    Supports filtering by completion status and pagination.

    Args:
        user_id: User ID from path
        completed: Optional filter by completion status
        limit: Maximum number of results (1-1000, default 100)
        offset: Pagination offset (default 0)
        verified_user_id: Verified user ID from middleware
        session: Database session

    Returns:
        TaskListResponse with list of tasks and total count
    """
    # Build query
    statement = select(Task).where(Task.user_id == UUID(user_id))

    # Apply completion filter if provided
    if completed is not None:
        statement = statement.where(Task.completed == completed)

    # Apply pagination and ordering
    statement = statement.order_by(Task.created_at.desc()).offset(offset).limit(limit)

    # Execute query
    tasks = session.exec(statement).all()

    # Get total count
    count_statement = select(Task).where(Task.user_id == UUID(user_id))
    if completed is not None:
        count_statement = count_statement.where(Task.completed == completed)
    total = len(session.exec(count_statement).all())

    return TaskListResponse(
        tasks=[TaskResponse(**task.model_dump()) for task in tasks],
        total=total
    )


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    verified_user_id: str = Depends(verify_user_access),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    Args:
        user_id: User ID from path
        task_data: Task creation data (title, description)
        verified_user_id: Verified user ID from middleware
        session: Database session

    Returns:
        TaskResponse with created task

    Raises:
        400: Invalid input data
        403: User not authorized
    """
    # Create new task
    new_task = Task(
        user_id=UUID(user_id),
        title=task_data.title,
        description=task_data.description
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return TaskResponse(**new_task.model_dump())


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    verified_user_id: str = Depends(verify_user_access),
    session: Session = Depends(get_session)
):
    """
    Get details of a specific task.

    Args:
        user_id: User ID from path
        task_id: Task ID to retrieve
        verified_user_id: Verified user ID from middleware
        session: Database session

    Returns:
        TaskResponse with task details

    Raises:
        404: Task not found or doesn't belong to user
    """
    # Find task
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == UUID(user_id)
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse(**task.model_dump())


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    verified_user_id: str = Depends(verify_user_access),
    session: Session = Depends(get_session)
):
    """
    Update an existing task.

    Args:
        user_id: User ID from path
        task_id: Task ID to update
        task_data: Task update data (title, description, completed)
        verified_user_id: Verified user ID from middleware
        session: Database session

    Returns:
        TaskResponse with updated task

    Raises:
        404: Task not found
        400: Invalid input data
    """
    # Find task
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == UUID(user_id)
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update fields if provided
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed

    # Update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse(**task.model_dump())


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: int,
    verified_user_id: str = Depends(verify_user_access),
    session: Session = Depends(get_session)
):
    """
    Delete a task permanently.

    Args:
        user_id: User ID from path
        task_id: Task ID to delete
        verified_user_id: Verified user ID from middleware
        session: Database session

    Returns:
        No content (204)

    Raises:
        404: Task not found
    """
    # Find task
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == UUID(user_id)
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Delete task
    session.delete(task)
    session.commit()

    return None


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    user_id: str,
    task_id: int,
    completed: Optional[bool] = None,
    verified_user_id: str = Depends(verify_user_access),
    session: Session = Depends(get_session)
):
    """
    Toggle or set task completion status.

    If no body is provided, completion status is toggled.
    If completed value is provided, it's set to that value.

    Args:
        user_id: User ID from path
        task_id: Task ID to update
        completed: Optional completion status to set
        verified_user_id: Verified user ID from middleware
        session: Database session

    Returns:
        TaskResponse with updated task

    Raises:
        404: Task not found
    """
    # Find task
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == UUID(user_id)
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle or set completion status
    if completed is None:
        task.completed = not task.completed
    else:
        task.completed = completed

    # Update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse(**task.model_dump())
