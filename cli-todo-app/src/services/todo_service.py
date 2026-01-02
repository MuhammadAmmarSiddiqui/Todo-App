"""
TodoService class for managing tasks in the todo application.
Handles all business logic for task operations using in-memory storage.
"""

import logging
from typing import List, Dict, Any, Optional
from src.models.task import Task


# Set up logging
logger = logging.getLogger(__name__)


class TodoService:
    """
    Service class that manages all todo operations.
    Uses in-memory storage as specified in the requirements.
    """

    def __init__(self) -> None:
        """Initialize the TodoService with empty task list and next ID counter."""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def _get_next_id(self) -> int:
        """
        Get the next available task ID.

        Returns:
            int: The next available task ID
        """
        next_id = self._next_id
        self._next_id += 1
        return next_id

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Add a new task to the todo list.

        Args:
            title (str): Title of the task (required)
            description (Optional[str]): Description of the task (optional)

        Returns:
            Task: The newly created task

        Raises:
            ValueError: If title is empty or invalid
        """
        logger.info(f"Adding new task: title='{title}', description='{description}'")
        if not title or not isinstance(title, str):
            logger.error("Invalid title provided for new task")
            raise ValueError("Title must be a non-empty string")
        if len(title) < 1 or len(title) > 200:
            logger.error(f"Title length {len(title)} is outside allowed range (1-200)")
            raise ValueError("Title must be between 1 and 200 characters")
        if description and len(description) > 1000:
            logger.error(f"Description length {len(description)} exceeds maximum allowed (1000)")
            raise ValueError("Description must be 1000 characters or less")

        task_id = self._get_next_id()
        task = Task(task_id=task_id, title=title, description=description, completed=False)
        self._tasks.append(task)
        logger.info(f"Task added successfully with ID: {task_id}")
        return task

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id (int): ID of the task to retrieve

        Returns:
            Optional[Task]: The task if found, None otherwise
        """
        logger.debug(f"Attempting to retrieve task with ID: {task_id}")
        if not isinstance(task_id, int) or task_id < 1:
            logger.error(f"Invalid task ID provided: {task_id}")
            raise ValueError("Task ID must be a positive integer")

        for task in self._tasks:
            if task.id == task_id:
                logger.debug(f"Task found with ID: {task_id}")
                return task
        logger.debug(f"Task with ID {task_id} not found")
        return None

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in the todo list.

        Returns:
            List[Task]: List of all tasks
        """
        return self._tasks.copy()

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id (int): ID of the task to update
            title (Optional[str]): New title (optional)
            description (Optional[str]): New description (optional)

        Returns:
            Optional[Task]: Updated task if found, None otherwise

        Raises:
            ValueError: If task_id is invalid or title is empty
        """
        logger.info(f"Attempting to update task with ID: {task_id}, title='{title}', description='{description}'")
        if not isinstance(task_id, int) or task_id < 1:
            logger.error(f"Invalid task ID provided for update: {task_id}")
            raise ValueError("Task ID must be a positive integer")

        task = self.get_task_by_id(task_id)
        if task is None:
            logger.warning(f"Attempted to update non-existent task with ID: {task_id}")
            return None

        if title is not None:
            if not title or not isinstance(title, str):
                logger.error("Invalid title provided for update")
                raise ValueError("Title must be a non-empty string")
            if len(title) < 1 or len(title) > 200:
                logger.error(f"Title length {len(title)} is outside allowed range (1-200) for update")
                raise ValueError("Title must be between 1 and 200 characters")
            logger.debug(f"Updating task {task_id} title from '{task.title}' to '{title}'")
            task.title = title

        if description is not None:
            if len(description) > 1000:
                logger.error(f"Description length {len(description)} exceeds maximum allowed (1000) for update")
                raise ValueError("Description must be 1000 characters or less")
            logger.debug(f"Updating task {task_id} description")
            task.description = description

        logger.info(f"Task {task_id} updated successfully")
        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id (int): ID of the task to delete

        Returns:
            bool: True if task was deleted, False if not found

        Raises:
            ValueError: If task_id is invalid
        """
        logger.info(f"Attempting to delete task with ID: {task_id}")
        if not isinstance(task_id, int) or task_id < 1:
            logger.error(f"Invalid task ID provided for deletion: {task_id}")
            raise ValueError("Task ID must be a positive integer")

        task = self.get_task_by_id(task_id)
        if task is None:
            logger.warning(f"Attempted to delete non-existent task with ID: {task_id}")
            return False

        self._tasks.remove(task)
        logger.info(f"Task with ID {task_id} deleted successfully")
        return True

    def mark_complete(self, task_id: int) -> bool:
        """
        Mark a task as complete.

        Args:
            task_id (int): ID of the task to mark complete

        Returns:
            bool: True if task was marked complete, False if not found

        Raises:
            ValueError: If task_id is invalid
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer")

        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        task.completed = True
        return True

    def mark_incomplete(self, task_id: int) -> bool:
        """
        Mark a task as incomplete.

        Args:
            task_id (int): ID of the task to mark incomplete

        Returns:
            bool: True if task was marked incomplete, False if not found

        Raises:
            ValueError: If task_id is invalid
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer")

        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        task.completed = False
        return True

    def get_next_id(self) -> int:
        """
        Get the next available ID without incrementing the counter.

        Returns:
            int: The next available ID
        """
        return self._next_id