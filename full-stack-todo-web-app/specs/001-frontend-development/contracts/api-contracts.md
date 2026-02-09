# API Contracts: Frontend-Backend Integration

## Base URL
```
http://localhost:8000/api/{user_id}
```

## Authentication
All endpoints require JWT token in Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Common Response Format

### Success Response
```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Optional message"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message",
    "details": { /* optional details */ }
  }
}
```

## Endpoints

### Task Management

#### GET /tasks
**Description**: Retrieve all tasks for the authenticated user

**Headers**:
- Authorization: Bearer `<token>`

**Query Parameters**:
- limit: number (optional, default: 50)
- offset: number (optional, default: 0)
- status: string (optional, filter by completion status)

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": "task_id",
      "userId": "user_id",
      "title": "Task title",
      "description": "Task description",
      "completed": false,
      "createdAt": "2024-01-01T00:00:00Z",
      "updatedAt": "2024-01-01T00:00:00Z",
      "completedAt": null
    }
  ]
}
```

#### POST /tasks
**Description**: Create a new task for the authenticated user

**Headers**:
- Authorization: Bearer `<token>`

**Request Body**:
```json
{
  "title": "Task title",
  "description": "Task description",
  "completed": false
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "new_task_id",
    "userId": "user_id",
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-01T00:00:00Z",
    "completedAt": null
  }
}
```

#### GET /tasks/{id}
**Description**: Get details of a specific task

**Headers**:
- Authorization: Bearer `<token>`

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "task_id",
    "userId": "user_id",
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-01T00:00:00Z",
    "completedAt": null
  }
}
```

#### PUT /tasks/{id}
**Description**: Update a specific task

**Headers**:
- Authorization: Bearer `<token>`

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "task_id",
    "userId": "user_id",
    "title": "Updated task title",
    "description": "Updated task description",
    "completed": true,
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-01T00:00:00Z",
    "completedAt": "2024-01-01T00:00:00Z"
  }
}
```

#### DELETE /tasks/{id}
**Description**: Delete a specific task

**Headers**:
- Authorization: Bearer `<token>`

**Response**:
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

#### PATCH /tasks/{id}/complete
**Description**: Toggle task completion status

**Headers**:
- Authorization: Bearer `<token>`

**Request Body**:
```json
{
  "completed": true
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "task_id",
    "userId": "user_id",
    "title": "Task title",
    "description": "Task description",
    "completed": true,
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-01T00:00:00Z",
    "completedAt": "2024-01-01T00:00:00Z"
  }
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| AUTH_001 | 401 | Invalid or expired JWT token |
| AUTH_002 | 401 | User not authorized to access this resource |
| AUTH_003 | 403 | Insufficient permissions |
| TASK_001 | 404 | Task not found |
| TASK_002 | 400 | Invalid task data provided |
| VALIDATION_001 | 400 | Request validation failed |
| SERVER_001 | 500 | Internal server error |