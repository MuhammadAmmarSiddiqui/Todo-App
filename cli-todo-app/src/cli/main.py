"""
Main CLI entry point for the todo application.
Uses argparse to handle command-line arguments and subcommands.
"""

import argparse
import logging
import re
import sys
from typing import Optional
from src.services.todo_service import TodoService


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TodoCLI:
    """
    Command-Line Interface for the todo application.
    Handles all user interactions through subcommands.
    """

    def __init__(self) -> None:
        """Initialize the CLI with a TodoService instance."""
        self.service = TodoService()
        self.session_active = False

    def add_task(self, title: str, description: Optional[str] = None) -> None:
        """
        Add a new task to the todo list.

        Args:
            title (str): Title of the task
            description (Optional[str]): Description of the task
        """
        logger.info(f"CLI: Adding task - title='{title}', description='{description}'")
        try:
            task = self.service.add_task(title, description)
            print(f"Task added successfully with ID: {task.id}")
            logger.info(f"CLI: Task added successfully with ID: {task.id}")
        except ValueError as e:
            logger.error(f"CLI: Error adding task - {e}")
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    def list_tasks(self) -> None:
        """List all tasks in the todo list."""
        logger.info("CLI: Listing all tasks")
        tasks = self.service.get_all_tasks()

        if not tasks:
            logger.info("CLI: No tasks found to display")
            print("No tasks found")
            return

        logger.info(f"CLI: Displaying {len(tasks)} tasks")
        # Print header
        print(f"{'ID':<4} {'Status':<8} {'Title':<30} {'Description'}")
        print("-" * 60)

        # Print each task
        for task in tasks:
            status = "[x]" if task.completed else "[ ]"
            title = task.title[:27] + "..." if len(task.title) > 30 else task.title
            description = task.description[:30] + "..." if len(task.description) > 30 else task.description
            print(f"{task.id:<4} {status:<8} {title:<30} {description}")

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> None:
        """
        Update an existing task.

        Args:
            task_id (int): ID of the task to update
            title (Optional[str]): New title for the task
            description (Optional[str]): New description for the task
        """
        try:
            result = self.service.update_task(task_id, title, description)
            if result is None:
                print(f"Error: Task with ID {task_id} not found", file=sys.stderr)
                sys.exit(1)
            else:
                print(f"Task {task_id} updated successfully")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    def delete_task(self, task_id: int) -> None:
        """
        Delete a task by its ID.

        Args:
            task_id (int): ID of the task to delete
        """
        logger.info(f"CLI: Attempting to delete task with ID: {task_id}")
        try:
            deleted = self.service.delete_task(task_id)
            if not deleted:
                logger.warning(f"CLI: Task with ID {task_id} not found for deletion")
                print(f"Error: Task with ID {task_id} not found", file=sys.stderr)
                sys.exit(1)
            else:
                logger.info(f"CLI: Task {task_id} deleted successfully")
                print(f"Task {task_id} deleted successfully")
        except ValueError as e:
            logger.error(f"CLI: Error deleting task {task_id} - {e}")
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    def mark_complete(self, task_id: int) -> None:
        """
        Mark a task as complete.

        Args:
            task_id (int): ID of the task to mark complete
        """
        try:
            marked = self.service.mark_complete(task_id)
            if not marked:
                print(f"Error: Task with ID {task_id} not found", file=sys.stderr)
                sys.exit(1)
            else:
                print(f"Task {task_id} marked as complete")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    def mark_incomplete(self, task_id: int) -> None:
        """
        Mark a task as incomplete.

        Args:
            task_id (int): ID of the task to mark incomplete
        """
        try:
            marked = self.service.mark_incomplete(task_id)
            if not marked:
                print(f"Error: Task with ID {task_id} not found", file=sys.stderr)
                sys.exit(1)
            else:
                print(f"Task {task_id} marked as incomplete")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    def start_session(self) -> None:
        """Start an interactive session for the todo application."""
        self.session_active = True
        print("Session started. Enter commands (type 'help' for available commands, 'exit' to quit):")
        self.interactive_loop()

    def exit_session(self) -> None:
        """Exit the current session."""
        if self.session_active:
            print("Session terminated.")
        self.session_active = False
        sys.exit(0)

    def interactive_loop(self) -> None:
        """Main interactive loop for session mode."""
        while self.session_active:
            try:
                # Display prompt
                command_input = input("todo> ").strip()

                if not command_input:
                    continue

                # Parse the command with proper argument handling (handles quoted strings)
                parts = self.parse_command_line(command_input)
                if not parts:
                    continue

                command = parts[0].lower()

                if command == 'exit':
                    self.exit_session()
                elif command == 'help':
                    self.show_help()
                elif command == 'add':
                    self.handle_add_command(parts[1:])
                elif command == 'list':
                    self.list_tasks()
                elif command == 'update':
                    self.handle_update_command(parts[1:])
                elif command == 'delete':
                    self.handle_delete_command(parts[1:])
                elif command == 'complete':
                    self.handle_complete_command(parts[1:])
                elif command == 'incomplete':
                    self.handle_incomplete_command(parts[1:])
                else:
                    print(f"Unknown command: {command}. Type 'help' for available commands.")
            except KeyboardInterrupt:
                print("\nReceived interrupt signal. Exiting session...")
                self.exit_session()
            except EOFError:
                print("\nEnd of input. Exiting session...")
                self.exit_session()

    def parse_command_line(self, command_input: str) -> list:
        """
        Parse command line input handling quoted arguments.

        Args:
            command_input: The raw command line input

        Returns:
            List of parsed arguments
        """
        # This pattern matches quoted strings (both single and double quotes) and unquoted words
        import re
        pattern = r'"([^"]*)"|\'([^\']*)\'|(\S+)'
        matches = re.findall(pattern, command_input)
        args = []
        for match in matches:
            # Each match is a tuple of 3 elements, one of which will be non-empty
            arg = match[0] or match[1] or match[2]
            if arg:  # Only add non-empty arguments
                args.append(arg)
        return args

    def show_help(self) -> None:
        """Show help information for available commands in session mode."""
        help_text = """
Available commands:
  add --title <title> [--description <description>]    Add a new task
  list                                              List all tasks
  update --id <id> [--title <title>] [--description <description>]    Update a task
  delete --id <id>                                  Delete a task
  complete --id <id>                                Mark task as complete
  incomplete --id <id>                              Mark task as incomplete
  help                                              Show this help message
  exit                                              Exit the session
        """
        print(help_text.strip())

    def handle_add_command(self, args: list) -> None:
        """Handle the add command in session mode."""
        if len(args) < 2:
            print("Usage: add --title <title> [--description <description>]")
            return

        title = None
        description = None

        i = 0
        while i < len(args):
            if args[i] == '--title' and i + 1 < len(args):
                title = args[i + 1]
                # Remove quotes if present
                if title.startswith('"') and title.endswith('"') and len(title) > 1:
                    title = title[1:-1]
                elif title.startswith("'") and title.endswith("'") and len(title) > 1:
                    title = title[1:-1]
                i += 2
            elif args[i] == '--description' and i + 1 < len(args):
                description = args[i + 1]
                # Remove quotes if present
                if description.startswith('"') and description.endswith('"') and len(description) > 1:
                    description = description[1:-1]
                elif description.startswith("'") and description.endswith("'") and len(description) > 1:
                    description = description[1:-1]
                i += 2
            else:
                print(f"Unknown argument: {args[i]}")
                return
            # The i += 1 was the issue - it should only increment when needed,
            # but the i += 2 above already handles the incrementing properly

        if title is None:
            print("Title is required for add command")
            return

        self.add_task(title, description)

    def handle_update_command(self, args: list) -> None:
        """Handle the update command in session mode."""
        if len(args) < 2:
            print("Usage: update --id <id> [--title <title>] [--description <description>]")
            return

        task_id = None
        title = None
        description = None

        i = 0
        while i < len(args):
            if args[i] == '--id' and i + 1 < len(args):
                try:
                    task_id = int(args[i + 1])
                except ValueError:
                    print(f"Invalid task ID: {args[i + 1]}")
                    return
                i += 2
            elif args[i] == '--title' and i + 1 < len(args):
                title = args[i + 1]
                # Remove quotes if present
                if title.startswith('"') and title.endswith('"') and len(title) > 1:
                    title = title[1:-1]
                elif title.startswith("'") and title.endswith("'") and len(title) > 1:
                    title = title[1:-1]
                i += 2
            elif args[i] == '--description' and i + 1 < len(args):
                description = args[i + 1]
                # Remove quotes if present
                if description.startswith('"') and description.endswith('"') and len(description) > 1:
                    description = description[1:-1]
                elif description.startswith("'") and description.endswith("'") and len(description) > 1:
                    description = description[1:-1]
                i += 2
            else:
                print(f"Unknown argument: {args[i]}")
                return
            # The i += 1 was the issue - it should only increment when needed,
            # but the i += 2 above already handles the incrementing properly

        if task_id is None:
            print("Task ID is required for update command")
            return

        self.update_task(task_id, title, description)

    def handle_delete_command(self, args: list) -> None:
        """Handle the delete command in session mode."""
        if len(args) < 2:
            print("Usage: delete --id <id>")
            return

        if args[0] != '--id' or len(args) < 2:
            print("Usage: delete --id <id>")
            return

        try:
            task_id = int(args[1])
            self.delete_task(task_id)
        except ValueError:
            print(f"Invalid task ID: {args[1]}")

    def handle_complete_command(self, args: list) -> None:
        """Handle the complete command in session mode."""
        if len(args) < 2:
            print("Usage: complete --id <id>")
            return

        if args[0] != '--id' or len(args) < 2:
            print("Usage: complete --id <id>")
            return

        try:
            task_id = int(args[1])
            self.mark_complete(task_id)
        except ValueError:
            print(f"Invalid task ID: {args[1]}")

    def handle_incomplete_command(self, args: list) -> None:
        """Handle the incomplete command in session mode."""
        if len(args) < 2:
            print("Usage: incomplete --id <id>")
            return

        if args[0] != '--id' or len(args) < 2:
            print("Usage: incomplete --id <id>")
            return

        try:
            task_id = int(args[1])
            self.mark_incomplete(task_id)
        except ValueError:
            print(f"Invalid task ID: {args[1]}")

    def run(self) -> None:
        """Run the CLI application."""
        # Check if this is a session command (start/exit) that should be handled separately
        if len(sys.argv) > 1 and sys.argv[1] in ['start', 'exit']:
            command = sys.argv[1]
            if command == 'start':
                self.start_session()
            elif command == 'exit':
                self.exit_session()
        else:
            # Traditional single command mode
            parser = argparse.ArgumentParser(description="Todo CLI Application")
            subparsers = parser.add_subparsers(dest="command", help="Available commands")

            # Add command
            add_parser = subparsers.add_parser("add", help="Add a new task")
            add_parser.add_argument("--title", required=True, help="Title of the task")
            add_parser.add_argument("--description", help="Description of the task")

            # List command
            list_parser = subparsers.add_parser("list", help="List all tasks")

            # Update command
            update_parser = subparsers.add_parser("update", help="Update an existing task")
            update_parser.add_argument("--id", type=int, required=True, help="ID of the task to update")
            update_parser.add_argument("--title", help="New title for the task")
            update_parser.add_argument("--description", help="New description for the task")

            # Delete command
            delete_parser = subparsers.add_parser("delete", help="Delete a task")
            delete_parser.add_argument("--id", type=int, required=True, help="ID of the task to delete")

            # Complete command
            complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
            complete_parser.add_argument("--id", type=int, required=True, help="ID of the task to mark complete")

            # Incomplete command
            incomplete_parser = subparsers.add_parser("incomplete", help="Mark a task as incomplete")
            incomplete_parser.add_argument("--id", type=int, required=True, help="ID of the task to mark incomplete")

            # Parse arguments
            args = parser.parse_args()

            # Handle commands
            if args.command == "add":
                self.add_task(args.title, args.description)
            elif args.command == "list":
                self.list_tasks()
            elif args.command == "update":
                self.update_task(args.id, args.title, args.description)
            elif args.command == "delete":
                self.delete_task(args.id)
            elif args.command == "complete":
                self.mark_complete(args.id)
            elif args.command == "incomplete":
                self.mark_incomplete(args.id)
            else:
                parser.print_help()


def main() -> None:
    """Main entry point for the application."""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()