# CLI Todo App - Running Instructions

A command-line interface application for managing todo tasks with both traditional single-command mode and interactive session mode.

## Prerequisites

- Python 3.12+ installed on your system

## Running the Application

### 1. Traditional Single-Command Mode

Run individual commands as before:

```bash
# Add a task
python -m src.cli.main add --title "My Task" --description "Task description"

# List all tasks
python -m src.cli.main list

# Update a task
python -m src.cli.main update --id 1 --title "Updated Title"

# Delete a task
python -m src.cli.main delete --id 1

# Mark task as complete
python -m src.cli.main complete --id 1

# Mark task as incomplete
python -m src.cli.main incomplete --id 1

# Show help
python -m src.cli.main --help
```

### 2. Interactive Session Mode

Start an interactive session where commands persist in memory:

```bash
# Start an interactive session
python -m src.cli.main start
```

Once in session mode, you'll see the prompt `todo> ` and can run commands like:

```
todo> add --title "My Task" --description "Task description"
todo> list
todo> complete --id 1
todo> update --id 1 --title "Updated Title"
todo> delete --id 1
todo> help  # Shows available commands
todo> exit  # Exits the session
```

## Session Mode Commands

When in session mode, the following commands are available:

- `add --title <title> [--description <description>]` - Add a new task
- `list` - List all tasks
- `update --id <id> [--title <title>] [--description <description>]` - Update a task
- `delete --id <id>` - Delete a task
- `complete --id <id>` - Mark task as complete
- `incomplete --id <id>` - Mark task as incomplete
- `help` - Show available commands
- `exit` - Exit the session

## Important Notes

- **Backward Compatibility**: All existing commands continue to work in traditional mode
- **Session Persistence**: Data persists in memory during a session but is cleared when exiting
- **Quoted Strings**: Use quotes for titles/descriptions containing spaces (e.g., `--title "Task with spaces"`)
- **Task IDs**: Automatically assigned incrementally during each session

## Example Session

```bash
$ python -m src.cli.main start
Session started. Enter commands (type 'help' for available commands, 'exit' to quit):
todo> add --title "Learn Python" --description "Complete Python tutorial"
Task added successfully with ID: 1
todo> add --title "Build CLI App" --description "Create a command-line application"
Task added successfully with ID: 2
todo> list
ID   Status   Title                          Description
------------------------------------------------------------
1    [ ]      Learn Python                   Complete Python tutorial
2    [ ]      Build CLI App                  Create a command-line application
todo> complete --id 1
Task 1 marked as complete
todo> list
ID   Status   Title                          Description
------------------------------------------------------------
1    [x]      Learn Python                   Complete Python tutorial
2    [ ]      Build CLI App                  Create a command-line application
todo> exit
Session terminated.
```