# Quickstart Guide: Todo In-Memory App

## Prerequisites
- Python 3.13+ installed
- UV package manager installed

## Setup

1. **Initialize the project**:
   ```bash
   uv init
   ```

2. **Install dependencies** (if any are needed beyond standard library):
   ```bash
   uv add [package-name]  # Only if external packages are required
   ```

3. **Project structure**:
   ```
   src/
   ├── models/
   │   └── task.py
   ├── services/
   │   └── todo_service.py
   └── cli/
       └── main.py
   ```

## Running the Application

The application will be available as a command-line tool with the following subcommands:

### Add a new task
```bash
python -m cli.main add --title "Task title" --description "Task description"
```

### List all tasks
```bash
python -m cli.main list
```

### Update a task
```bash
python -m cli.main update --id 1 --title "New title" --description "New description"
```

### Delete a task
```bash
python -m cli.main delete --id 1
```

### Mark task as complete/incomplete
```bash
python -m cli.main complete --id 1  # Mark as complete
python -m cli.main incomplete --id 1  # Mark as incomplete
```

## Development

1. **Run tests**:
   ```bash
   uv run pytest
   ```

2. **Type checking**:
   ```bash
   uv run mypy src/
   ```

3. **Code formatting**:
   ```bash
   uv run black src/
   ```

## Architecture Overview

- **Models** (`src/models/task.py`): Contains the Task data model using dictionary structure
- **Services** (`src/services/todo_service.py`): Contains business logic for task operations
- **CLI** (`src/cli/main.py`): Contains command-line interface using argparse