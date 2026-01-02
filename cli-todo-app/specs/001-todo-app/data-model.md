# Data Model: Todo In-Memory App

## Task Entity

### Fields
- **id**: `int` - Unique integer identifier for the task (auto-assigned)
- **title**: `str` - Required title of the task (cannot be empty)
- **description**: `str` - Optional description of the task (can be empty/null)
- **completed**: `bool` - Boolean indicating completion status (default: False)

### Validation Rules
- ID must be unique within the task list
- Title must be a non-empty string (required)
- Description can be any string or empty (optional)
- Completed status defaults to False when creating new tasks

### State Transitions
- **Initial State**: `completed = False`
- **Transition to Complete**: `completed = True` (via mark_complete operation)
- **Transition to Incomplete**: `completed = False` (via mark_incomplete operation)

## TaskList Structure

### Data Structure
- **Type**: `List[dict]` - Simple in-memory list of task dictionaries
- **Access Pattern**: Index-based access using task ID (sequential search for matching ID)

### Operations
- **Add**: Append new task dictionary to the list
- **Find**: Iterate through list to find task with matching ID
- **Update**: Find task by ID and update its properties
- **Delete**: Remove task dictionary from list by ID
- **List All**: Return all task dictionaries in the list

### Constraints
- Task IDs must be unique integers
- Task IDs should be sequentially assigned starting from 1
- In-memory only - data is lost when application closes