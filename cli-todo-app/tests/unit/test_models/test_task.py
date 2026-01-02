"""
Unit tests for the Task model.
"""

import pytest
from src.models.task import Task


class TestTask:
    """Test cases for the Task model."""

    def test_create_task_with_valid_data(self):
        """Test creating a task with valid data."""
        task = Task(task_id=1, title="Test Task", description="Test Description", completed=False)
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False

    def test_create_task_defaults(self):
        """Test creating a task with default values."""
        task = Task(task_id=1, title="Test Task")
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False

    def test_create_task_with_completed_true(self):
        """Test creating a task with completed status as True."""
        task = Task(task_id=1, title="Test Task", completed=True)
        assert task.completed is True

    def test_title_validation_on_creation(self):
        """Test that creating a task with empty title raises ValueError."""
        with pytest.raises(ValueError, match="Title must be a non-empty string"):
            Task(task_id=1, title="")

        with pytest.raises(ValueError, match="Title must be a non-empty string"):
            Task(task_id=1, title=None)

    def test_title_length_validation_on_creation(self):
        """Test that creating a task with title longer than 200 chars raises ValueError."""
        long_title = "t" * 201
        with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
            Task(task_id=1, title=long_title)

    def test_task_id_validation(self):
        """Test that creating a task with invalid ID raises ValueError."""
        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            Task(task_id=0, title="Test Task")

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            Task(task_id=-1, title="Test Task")

    def test_title_setter_validation(self):
        """Test that setting an empty title raises ValueError."""
        task = Task(task_id=1, title="Test Task")
        with pytest.raises(ValueError, match="Title must be a non-empty string"):
            task.title = ""

    def test_title_length_setter_validation(self):
        """Test that setting a title longer than 200 chars raises ValueError."""
        task = Task(task_id=1, title="Test Task")
        long_title = "t" * 201
        with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
            task.title = long_title

    def test_completed_setter_validation(self):
        """Test that setting completed status with non-boolean raises ValueError."""
        task = Task(task_id=1, title="Test Task")
        with pytest.raises(ValueError, match="Completed must be a boolean value"):
            task.completed = "not a boolean"

    def test_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(task_id=1, title="Test Task", description="Test Description", completed=True)
        task_dict = task.to_dict()

        assert task_dict["id"] == 1
        assert task_dict["title"] == "Test Task"
        assert task_dict["description"] == "Test Description"
        assert task_dict["completed"] is True

    def test_from_dict(self):
        """Test creating task from dictionary."""
        data = {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "completed": True
        }
        task = Task.from_dict(data)

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is True

    def test_repr(self):
        """Test string representation of task."""
        task = Task(task_id=1, title="Test Task", completed=False)
        repr_str = repr(task)
        assert "Task(id=1, title='Test Task'" in repr_str
        assert "[○]" in repr_str  # Incomplete task symbol

        task.completed = True
        repr_str = repr(task)
        assert "[✓]" in repr_str  # Complete task symbol

    def test_equality(self):
        """Test task equality comparison."""
        task1 = Task(task_id=1, title="Test Task", description="Description", completed=True)
        task2 = Task(task_id=1, title="Test Task", description="Description", completed=True)
        task3 = Task(task_id=2, title="Test Task", description="Description", completed=True)

        assert task1 == task2
        assert task1 != task3
        assert task1 != "not a task"