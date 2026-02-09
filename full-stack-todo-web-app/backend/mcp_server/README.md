# Model Context Protocol (MCP) Server

The MCP server provides a standardized way for the AI assistant to interact with the todo management system. It implements the Model Context Protocol to expose tools that the AI can call to perform specific actions.

## Available Tools

### add_task
- **Description**: Creates a new task for the authenticated user
- **Parameters**:
  - `description`: Description of the task to create
  - `user_id`: ID of the user for whom to create the task

### list_tasks
- **Description**: Lists tasks for the authenticated user
- **Parameters**:
  - `user_id`: ID of the user whose tasks to list
  - `completed`: Whether to list completed tasks (default: false)

### complete_task
- **Description**: Marks a task as completed for the authenticated user
- **Parameters**:
  - `task_id`: ID of the task to complete
  - `user_id`: ID of the user who owns the task

### delete_task
- **Description**: Deletes a task for the authenticated user
- **Parameters**:
  - `task_id`: ID of the task to delete
  - `user_id`: ID of the user who owns the task

## Security

- All tools validate that the requesting user has permission to perform the action
- Tools verify that users can only operate on their own tasks
- Input validation is performed on all parameters

## Implementation

The MCP server is implemented using the `mcp` Python package and integrated with the existing database models and repositories to ensure consistent data handling and security.