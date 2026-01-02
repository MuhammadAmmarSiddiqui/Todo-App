# Quickstart: Session Commands for CLI Todo App

## Getting Started

### Starting a Session
```bash
todo start
```
This enters interactive mode where you can run multiple commands with persistent data.

### Available Commands in Session Mode
Once in session mode, you can run:
```bash
# Add tasks
todo> add --title "My Task" --description "Task description"

# List all tasks
todo> list

# Update a task
todo> update --id 1 --title "Updated Task Title"

# Mark task as complete
todo> complete --id 1

# Mark task as incomplete
todo> incomplete --id 1

# Delete a task
todo> delete --id 1

# Exit the session
todo> exit
```

### Exiting a Session
```bash
todo> exit
```
or
```bash
todo> quit
```

### Single Command Mode (Backward Compatible)
The existing functionality remains unchanged:
```bash
todo add --title "My Task"
todo list
todo update --id 1 --title "Updated Title"
todo complete --id 1
todo delete --id 1
```

## Example Workflow
```bash
$ todo start
todo> add --title "Buy groceries" --description "Milk, bread, eggs"
Task added successfully with ID: 1
todo> add --title "Walk the dog"
Task added successfully with ID: 2
todo> list
ID   Status   Title                     Description
------------------------------------------------------------
1    [ ]      Buy groceries...          Milk, bread, eggs
2    [x]      Walk the dog
todo> complete --id 1
Task 1 marked as complete
todo> list
ID   Status   Title                     Description
------------------------------------------------------------
1    [x]      Buy groceries...          Milk, bread, eggs
2    [ ]      Walk the dog
todo> exit
$
```

## Error Handling
- Invalid commands show error message and return to prompt
- Invalid arguments show usage information
- Non-existent task IDs show error but maintain session
- Ctrl+C or Ctrl+D exits the session gracefully