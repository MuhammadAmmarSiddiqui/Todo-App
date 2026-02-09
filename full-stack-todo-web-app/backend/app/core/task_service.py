from sqlmodel import Session, select
from typing import List, Optional
from app.models.task import Task, TaskCreate, TaskUpdate, TaskPublic, TaskUpdateComplete
from fastapi import HTTPException, status
from datetime import datetime

class TaskService:
    """
    Service layer for Task operations with user isolation
    """

    @staticmethod
    def create_task(session: Session, task_data: TaskCreate, user_id: int) -> TaskPublic:
        """
        Create a new task for a specific user

        Args:
            session: Database session
            task_data: Task creation data
            user_id: ID of the user creating the task

        Returns:
            Created task as TaskPublic object
        """
        # Verify user owns the resource (redundant check but added for security)
        if task_data.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot create task for another user"
            )

        db_task = Task.from_orm(task_data) if hasattr(Task, 'from_orm') else Task(**task_data.dict())
        db_task.user_id = user_id

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return TaskPublic.from_orm(db_task) if hasattr(TaskPublic, 'from_orm') else TaskPublic(**db_task.dict())

    @staticmethod
    def get_tasks_by_user(session: Session, user_id: int) -> List[TaskPublic]:
        """
        Get all tasks for a specific user

        Args:
            session: Database session
            user_id: ID of the user whose tasks to retrieve

        Returns:
            List of tasks owned by the user
        """
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()

        return [TaskPublic.from_orm(task) if hasattr(TaskPublic, 'from_orm') else TaskPublic(**task.dict()) for task in tasks]

    @staticmethod
    def get_task_by_id_and_user(session: Session, task_id: int, user_id: int) -> Optional[TaskPublic]:
        """
        Get a specific task by ID for a specific user

        Args:
            session: Database session
            task_id: ID of the task to retrieve
            user_id: ID of the user who owns the task

        Returns:
            Task if found and owned by user, None otherwise
        """
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            return None

        return TaskPublic.from_orm(task) if hasattr(TaskPublic, 'from_orm') else TaskPublic(**task.dict())

    @staticmethod
    def update_task(session: Session, task_id: int, task_update: TaskUpdate, user_id: int) -> Optional[TaskPublic]:
        """
        Update a specific task for a specific user

        Args:
            session: Database session
            task_id: ID of the task to update
            task_update: Update data
            user_id: ID of the user who owns the task

        Returns:
            Updated task if found and owned by user, None otherwise
        """
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if not db_task:
            return None

        # Update the task with provided values
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        db_task.updated_at = datetime.utcnow()

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return TaskPublic.from_orm(db_task) if hasattr(TaskPublic, 'from_orm') else TaskPublic(**db_task.dict())

    @staticmethod
    def toggle_task_completion(session: Session, task_id: int, user_id: int) -> Optional[TaskPublic]:
        """
        Toggle completion status of a specific task for a specific user

        Args:
            session: Database session
            task_id: ID of the task to update
            user_id: ID of the user who owns the task

        Returns:
            Updated task if found and owned by user, None otherwise
        """
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if not db_task:
            return None

        # Toggle completion status
        db_task.completed = not db_task.completed
        db_task.updated_at = datetime.utcnow()

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return TaskPublic.from_orm(db_task) if hasattr(TaskPublic, 'from_orm') else TaskPublic(**db_task.dict())

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: int) -> bool:
        """
        Delete a specific task for a specific user

        Args:
            session: Database session
            task_id: ID of the task to delete
            user_id: ID of the user who owns the task

        Returns:
            True if task was deleted, False if not found
        """
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if not db_task:
            return False

        session.delete(db_task)
        session.commit()

        return True