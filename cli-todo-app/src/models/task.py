"""
Task data model for the todo application.
Represents a single task with ID, title, description, and completion status.
"""

from typing import Dict, Any, Optional


class Task:
    """
    A simple Task class that represents a todo item.
    Uses a dictionary structure internally as specified in the data model.
    """

    def __init__(self, task_id: int, title: str, description: Optional[str] = None, completed: bool = False):
        """
        Initialize a new Task.

        Args:
            task_id (int): Unique identifier for the task
            title (str): Title of the task (required)
            description (Optional[str]): Description of the task (optional)
            completed (bool): Completion status (default: False)
        """
        if not title or not isinstance(title, str):
            raise ValueError("Title must be a non-empty string")
        if len(title) < 1 or len(title) > 200:
            raise ValueError("Title must be between 1 and 200 characters")

        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer")

        self._task_dict: Dict[str, Any] = {
            "id": task_id,
            "title": title,
            "description": description or "",
            "completed": completed
        }

    @property
    def id(self) -> int:
        """Get the task ID."""
        return self._task_dict["id"]

    @property
    def title(self) -> str:
        """Get the task title."""
        return self._task_dict["title"]

    @title.setter
    def title(self, value: str) -> None:
        """Set the task title."""
        if not value or not isinstance(value, str):
            raise ValueError("Title must be a non-empty string")
        self._task_dict["title"] = value

    @property
    def description(self) -> str:
        """Get the task description."""
        return self._task_dict["description"]

    @description.setter
    def description(self, value: Optional[str]) -> None:
        """Set the task description."""
        self._task_dict["description"] = value or ""

    @property
    def completed(self) -> bool:
        """Get the completion status."""
        return self._task_dict["completed"]

    @completed.setter
    def completed(self, value: bool) -> None:
        """Set the completion status."""
        if not isinstance(value, bool):
            raise ValueError("Completed must be a boolean value")
        self._task_dict["completed"] = value

    def to_dict(self) -> Dict[str, Any]:
        """Convert the task to a dictionary representation."""
        return self._task_dict.copy()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """
        Create a Task instance from a dictionary.

        Args:
            data: Dictionary containing task data

        Returns:
            Task: A new Task instance
        """
        return cls(
            task_id=data["id"],
            title=data["title"],
            description=data.get("description"),
            completed=data.get("completed", False)
        )

    def __repr__(self) -> str:
        """String representation of the task."""
        status = "✓" if self.completed else "○"
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', completed={self.completed}) [{status}]"

    def __eq__(self, other) -> bool:
        """Check equality with another task."""
        if not isinstance(other, Task):
            return False
        return self.to_dict() == other.to_dict()