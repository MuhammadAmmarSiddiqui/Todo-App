# CLI Contract: Todo In-Memory App

## Command Structure
```
todo [subcommand] [options]
```

## Subcommands

### `add`
Add a new task to the todo list.

**Usage**:
```
todo add --title "Task Title" [--description "Task Description"]
```

**Parameters**:
- `--title` (required): Task title (string, non-empty)
- `--description` (optional): Task description (string, can be empty)

**Success Response**:
- Task created with unique ID
- Success message with assigned ID

**Error Responses**:
- Title is required
- Invalid parameters

### `list`
Display all tasks in the todo list.

**Usage**:
```
todo list
```

**Parameters**: None

**Success Response**:
- Formatted table showing all tasks with ID, Status ([ ] or [x]), Title, and Description
- If no tasks exist, display "No tasks found"

**Error Responses**: None

### `update`
Update an existing task's title and/or description.

**Usage**:
```
todo update --id ID [--title "New Title"] [--description "New Description"]
```

**Parameters**:
- `--id` (required): Task ID (integer)
- `--title` (optional): New task title (string, non-empty)
- `--description` (optional): New task description (string, can be empty)

**Success Response**:
- Task updated successfully
- Confirmation message

**Error Responses**:
- Task with ID not found
- Invalid ID format
- Missing required parameters

### `delete`
Remove a task from the todo list.

**Usage**:
```
todo delete --id ID
```

**Parameters**:
- `--id` (required): Task ID (integer)

**Success Response**:
- Task deleted successfully
- Confirmation message

**Error Responses**:
- Task with ID not found
- Invalid ID format

### `complete`
Mark a task as complete.

**Usage**:
```
todo complete --id ID
```

**Parameters**:
- `--id` (required): Task ID (integer)

**Success Response**:
- Task marked as complete
- Confirmation message

**Error Responses**:
- Task with ID not found
- Invalid ID format

### `incomplete`
Mark a task as incomplete.

**Usage**:
```
todo incomplete --id ID
```

**Parameters**:
- `--id` (required): Task ID (integer)

**Success Response**:
- Task marked as incomplete
- Confirmation message

**Error Responses**:
- Task with ID not found
- Invalid ID format

### `help`
Display help information.

**Usage**:
```
todo help
todo --help
```

**Parameters**: None

**Success Response**:
- Help text for all commands
- Usage examples

**Error Responses**: None