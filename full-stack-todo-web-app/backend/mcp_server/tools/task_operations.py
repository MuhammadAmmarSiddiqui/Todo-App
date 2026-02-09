import asyncio
from typing import Dict, Any
from sqlmodel import Session, select
from uuid import UUID
from app.database.session import engine
from app.models.task import Task, TaskCreate
from app.models.user import User
from mcp_server.server import mcp_server_instance


async def register_task_operation_tools():
    """Register all task operation tools with the MCP server"""
    
    @mcp_server_instance.register_tool(
        name="add_task",
        description="Creates a new task for the authenticated user",
        parameters={
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "Description of the task to create"
                },
                "user_id": {
                    "type": "integer",
                    "description": "ID of the user for whom to create the task"
                }
            },
            "required": ["description", "user_id"]
        }
    )
    async def add_task(description: str, user_id: int) -> Dict[str, Any]:
        """
        Creates a new task for the authenticated user
        """
        try:
            # Validate that the user exists
            with Session(engine) as session:
                user = session.get(User, user_id)
                if not user:
                    return {"error": f"User with ID {user_id} not found"}
                
                # Create the new task
                task_data = TaskCreate(
                    title=description[:255],  # Truncate to fit field limit
                    description=description,
                    completed=False,
                    user_id=user_id
                )
                
                db_task = Task.model_validate(task_data)
                session.add(db_task)
                session.commit()
                session.refresh(db_task)
                
                return {
                    "success": True,
                    "task_id": db_task.id,
                    "message": f"Task '{description}' created successfully"
                }
        except Exception as e:
            return {"error": f"Failed to create task: {str(e)}"}

    @mcp_server_instance.register_tool(
        name="list_tasks",
        description="Lists tasks for the authenticated user",
        parameters={
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "ID of the user whose tasks to list"
                },
                "completed": {
                    "type": "boolean",
                    "description": "Whether to list completed tasks (default: false)"
                }
            },
            "required": ["user_id"]
        }
    )
    async def list_tasks(user_id: int, completed: bool = False) -> Dict[str, Any]:
        """
        Lists tasks for the authenticated user
        """
        try:
            with Session(engine) as session:
                # Build the query based on whether we want completed or pending tasks
                query = select(Task).where(Task.user_id == user_id)
                if completed is not None:
                    query = query.where(Task.completed == completed)
                
                tasks = session.exec(query).all()
                
                task_list = []
                for task in tasks:
                    task_list.append({
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": task.updated_at.isoformat()
                    })
                
                status = "completed" if completed else "pending"
                return {
                    "success": True,
                    "tasks": task_list,
                    "count": len(task_list),
                    "message": f"Found {len(task_list)} {status} tasks"
                }
        except Exception as e:
            return {"error": f"Failed to list tasks: {str(e)}"}

    @mcp_server_instance.register_tool(
        name="complete_task",
        description="Marks a task as completed for the authenticated user",
        parameters={
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "ID of the task to complete"
                },
                "user_id": {
                    "type": "integer",
                    "description": "ID of the user who owns the task"
                }
            },
            "required": ["task_id", "user_id"]
        }
    )
    async def complete_task(task_id: int, user_id: int) -> Dict[str, Any]:
        """
        Marks a task as completed for the authenticated user
        """
        try:
            with Session(engine) as session:
                # Get the task and verify it belongs to the user
                task = session.get(Task, task_id)
                if not task:
                    return {"error": f"Task with ID {task_id} not found"}
                
                if task.user_id != user_id:
                    return {"error": "Unauthorized: Task does not belong to user"}
                
                # Update the task as completed
                task.completed = True
                session.add(task)
                session.commit()
                session.refresh(task)
                
                return {
                    "success": True,
                    "task_id": task.id,
                    "message": f"Task '{task.title}' marked as completed"
                }
        except Exception as e:
            return {"error": f"Failed to complete task: {str(e)}"}

    @mcp_server_instance.register_tool(
        name="delete_task",
        description="Deletes a task for the authenticated user",
        parameters={
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "ID of the task to delete"
                },
                "user_id": {
                    "type": "integer",
                    "description": "ID of the user who owns the task"
                }
            },
            "required": ["task_id", "user_id"]
        }
    )
    async def delete_task(task_id: int, user_id: int) -> Dict[str, Any]:
        """
        Deletes a task for the authenticated user
        """
        try:
            with Session(engine) as session:
                # Get the task and verify it belongs to the user
                task = session.get(Task, task_id)
                if not task:
                    return {"error": f"Task with ID {task_id} not found"}
                
                if task.user_id != user_id:
                    return {"error": "Unauthorized: Task does not belong to user"}
                
                # Delete the task
                session.delete(task)
                session.commit()
                
                return {
                    "success": True,
                    "task_id": task.id,
                    "message": f"Task '{task.title}' deleted successfully"
                }
        except Exception as e:
            return {"error": f"Failed to delete task: {str(e)}"}

