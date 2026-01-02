"""
Integration tests for the CLI functionality.
"""

import sys
import subprocess
from unittest.mock import patch
import pytest
from src.cli.main import TodoCLI


class TestCLIIntegration:
    """Integration tests for the CLI functionality."""

    def test_add_and_list_tasks(self):
        """Test adding tasks and then listing them."""
        cli = TodoCLI()

        # Add a task
        cli.add_task("Test Task", "Test Description")

        # List tasks and verify the task exists
        # We'll capture the output by mocking print
        import io
        import contextlib

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            cli.list_tasks()
        output = f.getvalue()

        assert "Test Task" in output
        assert "Test Description" in output

    def test_add_update_and_list_tasks(self):
        """Test adding a task, updating it, and then listing it."""
        cli = TodoCLI()

        # Add a task
        import io
        import contextlib

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            cli.add_task("Original Task", "Original Description")
        output = f.getvalue()

        # Extract the task ID from the output
        lines = output.strip().split('\n')
        for line in lines:
            if "Task added successfully with ID:" in line:
                task_id = int(line.split()[-1])
                break

        # Update the task
        cli.update_task(task_id, "Updated Task", "Updated Description")

        # List tasks and verify the update
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            cli.list_tasks()
        output = f.getvalue()

        assert "Updated Task" in output
        assert "Updated Description" in output

    def test_add_complete_task(self):
        """Test adding a task and marking it as complete."""
        cli = TodoCLI()

        # Add a task
        import io
        import contextlib

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            cli.add_task("Test Task", "Test Description")
        output = f.getvalue()

        # Extract the task ID from the output
        lines = output.strip().split('\n')
        for line in lines:
            if "Task added successfully with ID:" in line:
                task_id = int(line.split()[-1])
                break

        # Mark as complete
        cli.mark_complete(task_id)

        # List tasks and verify it's marked complete
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            cli.list_tasks()
        output = f.getvalue()

        assert "[x]" in output  # Check for completed status

    def test_add_delete_task(self):
        """Test adding a task and then deleting it."""
        cli = TodoCLI()

        # Add a task
        import io
        import contextlib

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            cli.add_task("Test Task", "Test Description")
        output = f.getvalue()

        # Extract the task ID from the output
        lines = output.strip().split('\n')
        for line in lines:
            if "Task added successfully with ID:" in line:
                task_id = int(line.split()[-1])
                break

        # Delete the task
        cli.delete_task(task_id)

        # List tasks and verify it's gone
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            cli.list_tasks()
        output = f.getvalue()

        assert "No tasks found" in output

    def test_error_handling_for_invalid_task_id(self):
        """Test error handling when using invalid task IDs."""
        cli = TodoCLI()

        # Try to update a non-existent task
        import io
        import contextlib
        import sys

        f = io.StringIO()
        with contextlib.redirect_stderr(f):
            try:
                cli.update_task(999, "New Title")
            except SystemExit:
                pass  # Expected to exit with error
        output = f.getvalue()

        assert "not found" in output

    def test_error_handling_for_empty_title(self):
        """Test error handling when adding a task with empty title."""
        cli = TodoCLI()

        # Try to add a task with empty title
        import io
        import contextlib

        f = io.StringIO()
        with contextlib.redirect_stderr(f):
            try:
                cli.add_task("")
            except SystemExit:
                pass  # Expected to exit with error
        output = f.getvalue()

        assert "Error:" in output
        assert "Title must be a non-empty string" in output