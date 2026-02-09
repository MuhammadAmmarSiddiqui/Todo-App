# API Documentation

## Overview
The Todo Web Application API provides secure REST endpoints for managing user tasks. All endpoints require JWT authentication and enforce user isolation.

## Authentication
All API endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token_here>
```

The JWT token must be obtained through Better Auth and contain a valid user ID in the `sub` field.

## Base URL
```
http://localhost:8000/api/{user_id}/...
```

## Endpoints

### Tasks

#### GET /api/{user_id}/tasks
**Description**: Retrieve all tasks for the authenticated user.

**Headers**:
- `Authorization: Bearer <valid_jwt_token>`

**Path Parameters**:
- `user_id` (string): User ID matching the authenticated user's ID in the JWT token

**Responses**:
- `200 OK`: List of tasks for the user
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: Token user ID does not match URL user ID
- `500 Internal Server Error`: Server error

**Example Request**:
```
GET /api/123/tasks
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### POST /api/{user_id}/tasks
**Description**: Create a new task for the authenticated user.

**Headers**:
- `Authorization: Bearer <valid_jwt_token>`
- `Content-Type: application/json`

**Path Parameters**:
- `user_id` (string): User ID matching the authenticated user's ID in the JWT token

**Request Body**:
```json
{
  "title": "Task title",
  "description": "Task description (optional)",
  "user_id": 123
}
```

**Responses**:
- `201 Created`: Task created successfully
- `400 Bad Request`: Invalid request body or user_id mismatch
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: Token user ID does not match URL user ID
- `500 Internal Server Error`: Server error

#### GET /api/{user_id}/tasks/{task_id}
**Description**: Get details of a specific task for the authenticated user.

**Headers**:
- `Authorization: Bearer <valid_jwt_token>`

**Path Parameters**:
- `user_id` (string): User ID matching the authenticated user's ID in the JWT token
- `task_id` (integer): Task ID to retrieve

**Responses**:
- `200 OK`: Task details
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: Token user ID does not match URL user ID
- `404 Not Found`: Task not found
- `500 Internal Server Error`: Server error

#### PUT /api/{user_id}/tasks/{task_id}
**Description**: Update a specific task for the authenticated user.

**Headers**:
- `Authorization: Bearer <valid_jwt_token>`
- `Content-Type: application/json`

**Path Parameters**:
- `user_id` (string): User ID matching the authenticated user's ID in the JWT token
- `task_id` (integer): Task ID to update

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description (optional)",
  "is_completed": false
}
```

**Responses**:
- `200 OK`: Task updated successfully
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: Token user ID does not match URL user ID
- `404 Not Found`: Task not found
- `500 Internal Server Error`: Server error

#### PATCH /api/{user_id}/tasks/{task_id}/complete
**Description**: Toggle completion status of a specific task for the authenticated user.

**Headers**:
- `Authorization: Bearer <valid_jwt_token>`

**Path Parameters**:
- `user_id` (string): User ID matching the authenticated user's ID in the JWT token
- `task_id` (integer): Task ID to update

**Responses**:
- `200 OK`: Task with updated completion status
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: Token user ID does not match URL user ID
- `404 Not Found`: Task not found
- `500 Internal Server Error`: Server error

#### DELETE /api/{user_id}/tasks/{task_id}
**Description**: Delete a specific task for the authenticated user.

**Headers**:
- `Authorization: Bearer <valid_jwt_token>`

**Path Parameters**:
- `user_id` (string): User ID matching the authenticated user's ID in the JWT token
- `task_id` (integer): Task ID to delete

**Responses**:
- `204 No Content`: Task deleted successfully
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: Token user ID does not match URL user ID
- `404 Not Found`: Task not found
- `500 Internal Server Error`: Server error

## Authentication Error Responses

### 401 Unauthorized
Returned when:
- No Authorization header is provided
- Invalid JWT token format
- Expired JWT token
- Invalid JWT signature

```json
{
  "detail": "Authorization header missing or invalid"
}
```

### 403 Forbidden
Returned when:
- JWT token is valid but user ID in token does not match user ID in URL
- User tries to access another user's data

```json
{
  "detail": "Access denied: User ID mismatch"
}
```

## Security Headers
The API includes the following security headers:
- `X-Frame-Options`: DENY
- `X-Content-Type-Options`: nosniff
- `Strict-Transport-Security`: max-age=31536000; includeSubDomains
- Additional security headers as configured by CORS middleware

## Error Handling
All API endpoints follow standard HTTP status codes and return error details in the response body:
```json
{
  "detail": "Descriptive error message"
}
```

## User Isolation
The API enforces strict user isolation by:
1. Requiring JWT token authentication for all endpoints
2. Validating that the user ID in the JWT token matches the user ID in the URL
3. Filtering database queries by the authenticated user's ID
4. Returning 403 Forbidden for any attempted cross-user access