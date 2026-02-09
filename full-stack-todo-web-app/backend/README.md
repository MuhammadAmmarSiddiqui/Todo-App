# Todo API Backend

Backend implementation for the multi-user todo web application using FastAPI, SQLModel, and Neon PostgreSQL.

## Features

- RESTful API endpoints for task management
- JWT-based authentication using Better Auth
- User isolation to ensure each user only accesses their own tasks
- SQLModel for database modeling and querying
- Neon PostgreSQL integration with connection pooling
- Request validation and response serialization

## API Endpoints

All endpoints follow the pattern: `/api/{user_id}/...`

- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks` - List all tasks for a user
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion status

## Setup

1. Copy `.env.example` to `.env` and update with your configuration
2. Install dependencies: `pip install -r requirements.txt`
3. Run database migrations: `alembic upgrade head`
4. Start the application: `./startup.sh`

## Environment Variables

- `DATABASE_URL`: PostgreSQL database connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT token signing/verification
- `ENVIRONMENT`: Environment name (development, production)
- `DEBUG`: Enable/disable debug mode

## Running Tests

```bash
pytest
```

## Architecture

The backend follows a layered architecture:

- **API Layer**: FastAPI routes and controllers
- **Service Layer**: Business logic and user isolation
- **Data Layer**: SQLModel models and database operations
- **Authentication Layer**: JWT token validation