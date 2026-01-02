"""
Unit tests for the TodoService.
"""

import pytest
from src.services.todo_service import TodoService
from src.models.task import Task


class TestTodoService:
    """Test cases for the TodoService."""

    def test_initial_state(self):
        """Test that TodoService starts with empty task list and ID counter."""
        service = TodoService()
        assert len(service.get_all_tasks()) == 0
        assert service.get_next_id() == 1

    def test_add_task(self):
        """Test adding a task."""
        service = TodoService()
        task = service.add_task("Test Task", "Test Description")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False

        tasks = service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0] == task

    def test_add_task_with_long_title(self):
        """Test adding a task with title longer than 200 characters raises ValueError."""
        service = TodoService()
        long_title = "t" * 201

        with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
            service.add_task(long_title)

    def test_add_task_with_long_description(self):
        """Test adding a task with description longer than 1000 characters raises ValueError."""
        service = TodoService()
        long_description = "d" * 1001

        with pytest.raises(ValueError, match="Description must be 1000 characters or less"):
            service.add_task("Test Task", long_description)

    def test_add_task_with_empty_title(self):
        """Test adding a task with empty title raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError, match="Title must be a non-empty string"):
            service.add_task("")

    def test_get_task_by_id(self):
        """Test getting a task by ID."""
        service = TodoService()
        task = service.add_task("Test Task")

        found_task = service.get_task_by_id(task.id)
        assert found_task is not None
        assert found_task.id == task.id
        assert found_task.title == task.title

        # Test getting non-existent task
        not_found_task = service.get_task_by_id(999)
        assert not_found_task is None

    def test_get_task_by_id_invalid_id(self):
        """Test getting a task with invalid ID raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.get_task_by_id(0)

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.get_task_by_id(-1)

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        service = TodoService()
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")

        all_tasks = service.get_all_tasks()
        assert len(all_tasks) == 2
        assert task1 in all_tasks
        assert task2 in all_tasks

        # Verify it returns a copy, not the internal list
        original_length = len(service.get_all_tasks())
        all_tasks.append("dummy")
        assert len(service.get_all_tasks()) == original_length

    def test_update_task(self):
        """Test updating a task."""
        service = TodoService()
        original_task = service.add_task("Original Title", "Original Description")

        updated_task = service.update_task(original_task.id, "New Title", "New Description")
        assert updated_task is not None
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"

        # Verify the task was actually updated in the service
        retrieved_task = service.get_task_by_id(original_task.id)
        assert retrieved_task.title == "New Title"
        assert retrieved_task.description == "New Description"

    def test_update_task_partial(self):
        """Test updating only title or description."""
        service = TodoService()
        original_task = service.add_task("Original Title", "Original Description")

        # Update only title
        service.update_task(original_task.id, title="New Title")
        updated_task = service.get_task_by_id(original_task.id)
        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"

        # Reset and update only description
        service = TodoService()
        original_task = service.add_task("Original Title", "Original Description")
        service.update_task(original_task.id, description="New Description")
        updated_task = service.get_task_by_id(original_task.id)
        assert updated_task.title == "Original Title"
        assert updated_task.description == "New Description"

    def test_update_nonexistent_task(self):
        """Test updating a non-existent task returns None."""
        service = TodoService()
        result = service.update_task(999, "New Title")
        assert result is None

    def test_update_task_with_invalid_data(self):
        """Test updating a task with invalid data raises ValueError."""
        service = TodoService()
        task = service.add_task("Test Task")

        with pytest.raises(ValueError, match="Title must be a non-empty string"):
            service.update_task(task.id, title="")

        with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
            service.update_task(task.id, title="t" * 201)

        with pytest.raises(ValueError, match="Description must be 1000 characters or less"):
            service.update_task(task.id, description="d" * 1001)

    def test_update_task_with_invalid_id(self):
        """Test updating a task with invalid ID raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.update_task(0, title="New Title")

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.update_task(-1, title="New Title")

    def test_delete_task(self):
        """Test deleting a task."""
        service = TodoService()
        task = service.add_task("Test Task")

        result = service.delete_task(task.id)
        assert result is True
        assert service.get_task_by_id(task.id) is None
        assert len(service.get_all_tasks()) == 0

    def test_delete_nonexistent_task(self):
        """Test deleting a non-existent task returns False."""
        service = TodoService()
        result = service.delete_task(999)
        assert result is False

    def test_delete_task_with_invalid_id(self):
        """Test deleting a task with invalid ID raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.delete_task(0)

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.delete_task(-1)

    def test_mark_complete(self):
        """Test marking a task as complete."""
        service = TodoService()
        task = service.add_task("Test Task")

        result = service.mark_complete(task.id)
        assert result is True

        updated_task = service.get_task_by_id(task.id)
        assert updated_task.completed is True

    def test_mark_incomplete(self):
        """Test marking a task as incomplete."""
        service = TodoService()
        task = service.add_task("Test Task")
        service.mark_complete(task.id)  # First mark as complete

        result = service.mark_incomplete(task.id)
        assert result is True

        updated_task = service.get_task_by_id(task.id)
        assert updated_task.completed is False

    def test_mark_nonexistent_task(self):
        """Test marking a non-existent task returns False."""
        service = TodoService()
        result = service.mark_complete(999)
        assert result is False

        result = service.mark_incomplete(999)
        assert result is False

    def test_mark_task_with_invalid_id(self):
        """Test marking a task with invalid ID raises ValueError."""
        service = TodoService()

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.mark_complete(0)

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.mark_complete(-1)

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.mark_incomplete(0)

        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            service.mark_incomplete(-1)

    def test_task_id_sequential_assignment(self):
        """Test that task IDs are assigned sequentially."""
        service = TodoService()
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3