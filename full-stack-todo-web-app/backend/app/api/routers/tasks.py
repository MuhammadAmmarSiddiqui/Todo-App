from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from app.database.session import get_session
from app.models.task import TaskCreate, TaskUpdate, TaskPublic, TaskUpdateComplete
from app.core.auth import verify_jwt_token, verify_user_owns_resource, authenticate_and_authorize
from app.core.jwt_utils import authenticate_and_authorize as jwt_authenticate_and_authorize
from app.core.task_service import TaskService

router = APIRouter()

@router.post("/tasks", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: str,
    task_data: TaskCreate,
    token_payload: dict = Depends(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    Args:
        user_id: User ID from path parameter
        task_data: Task creation data
        token_payload: JWT token payload containing user info
        session: Database session

    Returns:
        Created task object
    """
    # Verify user owns the resource using the enhanced authentication function
    verify_user_owns_resource(user_id, token_payload)

    # Convert user_id to int for database operations
    user_id_int = int(user_id)

    # Ensure task belongs to the correct user
    if task_data.user_id != user_id_int:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task user_id must match the authenticated user"
        )

    return TaskService.create_task(session, task_data, user_id_int)


@router.get("/tasks", response_model=List[TaskPublic])
def get_tasks(
    user_id: str,
    token_payload: dict = Depends(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.

    Args:
        user_id: User ID from path parameter
        token_payload: JWT token payload containing user info
        session: Database session

    Returns:
        List of user's tasks
    """
    # Verify user owns the resource using the enhanced authentication function
    verify_user_owns_resource(user_id, token_payload)

    # Convert user_id to int for database operations
    user_id_int = int(user_id)

    return TaskService.get_tasks_by_user(session, user_id_int)


@router.get("/tasks/{task_id}", response_model=TaskPublic)
def get_task(
    user_id: str,
    task_id: int,
    token_payload: dict = Depends(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the authenticated user.

    Args:
        user_id: User ID from path parameter
        task_id: Task ID to retrieve
        token_payload: JWT token payload containing user info
        session: Database session

    Returns:
        Task object if found and owned by user
    """
    # Verify user owns the resource using the enhanced authentication function
    verify_user_owns_resource(user_id, token_payload)

    # Convert user_id to int for database operations
    user_id_int = int(user_id)

    task = TaskService.get_task_by_id_and_user(session, task_id, user_id_int)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/tasks/{task_id}", response_model=TaskPublic)
def update_task(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate,
    token_payload: dict = Depends(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """
    Update a specific task for the authenticated user.

    Args:
        user_id: User ID from path parameter
        task_id: Task ID to update
        task_update: Update data
        token_payload: JWT token payload containing user info
        session: Database session

    Returns:
        Updated task object if found and owned by user
    """
    # Verify user owns the resource using the enhanced authentication function
    verify_user_owns_resource(user_id, token_payload)

    # Convert user_id to int for database operations
    user_id_int = int(user_id)

    updated_task = TaskService.update_task(session, task_id, task_update, user_id_int)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task


@router.patch("/tasks/{task_id}/complete", response_model=TaskPublic)
def toggle_task_completion(
    user_id: str,
    task_id: int,
    token_payload: dict = Depends(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """
    Toggle completion status of a specific task for the authenticated user.

    Args:
        user_id: User ID from path parameter
        task_id: Task ID to update
        token_payload: JWT token payload containing user info
        session: Database session

    Returns:
        Updated task object with toggled completion status
    """
    # Verify user owns the resource using the enhanced authentication function
    verify_user_owns_resource(user_id, token_payload)

    # Convert user_id to int for database operations
    user_id_int = int(user_id)

    updated_task = TaskService.toggle_task_completion(session, task_id, user_id_int)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: str,
    task_id: int,
    token_payload: dict = Depends(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task for the authenticated user.

    Args:
        user_id: User ID from path parameter
        task_id: Task ID to delete
        token_payload: JWT token payload containing user info
        session: Database session
    """
    # Verify user owns the resource using the enhanced authentication function
    verify_user_owns_resource(user_id, token_payload)

    # Convert user_id to int for database operations
    user_id_int = int(user_id)

    success = TaskService.delete_task(session, task_id, user_id_int)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Return 204 No Content on successful deletion
    return