import asyncio
import os
import json
import sys
from typing import Dict, Any, Optional, List
from uuid import UUID

from openai import OpenAI
# Removed agents import
from mcp import ClientSession
from mcp.client.sse import sse_client
import httpx

from services.gemini_config import gemini_client

# Removed environment variable hacks as we are using the client directly

from app.database.session import engine
from repositories.conversation_repository import ConversationRepository, MessageRepository
from sqlmodel import Session


class OpenAIAssistantService:
    def __init__(self):
        # Use Gemini client (OpenAI-compatible)
        self.client = gemini_client
        # List of models to try
        self.model_name = "gemini-2.5-flash"
        self.mcp_base_url = "http://localhost:8080/sse"

    async def _call_mcp_tool(self, name: str, arguments: dict) -> str:
        """Low-level helper to call an MCP tool via SSE"""
        try:
            async with sse_client(self.mcp_base_url) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool(name, arguments)
                    # result.content is usually a list of content blocks
                    if hasattr(result, 'content'):
                        return "\n".join([str(c.text) if hasattr(c, 'text') else str(c) for c in result.content])
                    return str(result)
        except Exception as e:
            print(f"MCP Tool Call Error ({name}): {e}")
            return f"Error: Failed to execute tool {name}. {str(e)}"

    def _get_tools_definitions(self):
        """Return OpenAI tool definitions"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Creates a new task for the user.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "description": {"type": "string", "description": "The description or title of the task to add."}
                        },
                        "required": ["description"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Lists tasks for the user.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "completed": {"type": "boolean", "description": "Filter by completion status. Defaults to False (pending tasks)."}
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Marks a task as completed.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "The ID of the task to complete."}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Deletes a task.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "The ID of the task to delete."}
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]

    async def _execute_tool(self, tool_name: str, tool_args: dict, user_id: int) -> str:
        """Execute a tool based on its name"""
        if tool_name == "add_task":
            return await self._call_mcp_tool("add_task", {"description": tool_args.get("description"), "user_id": user_id})
        elif tool_name == "list_tasks":
            return await self._call_mcp_tool("list_tasks", {"user_id": user_id, "completed": tool_args.get("completed", False)})
        elif tool_name == "complete_task":
            return await self._call_mcp_tool("complete_task", {"task_id": tool_args.get("task_id"), "user_id": user_id})
        elif tool_name == "delete_task":
            return await self._call_mcp_tool("delete_task", {"task_id": tool_args.get("task_id"), "user_id": user_id})
        return f"Error: Unknown tool {tool_name}"

    async def process_chat_message(self, user_message: str, user_id: int, conversation_id: str) -> Dict[str, Any]:
        """Process a chat message using standard OpenAI Client with manual tool calling loop"""
        try:
            conv_uuid = UUID(conversation_id)
            
            with Session(engine) as session:
                message_repo = MessageRepository(session)
                db_messages = message_repo.get_messages_by_conversation(conv_uuid)
                
                # Build message history
                messages = []
                # System prompt
                messages.append({
                    "role": "system",
                    "content": (
                        f"You are a helpful Todo Management Assistant for user {user_id}. "
                        "Help them manage their tasks using the provided tools. "
                        "When adding a task, just use the description provided by the user."
                    )
                })
                
                # History
                for msg in db_messages:
                    messages.append({
                        "role": msg.role.value,
                        "content": msg.content
                    })
                
                # Current user message
                # Check if the last message in history is the same as current user message
                # This prevents duplication since the route handler saves the message before calling this service
                is_duplicate = False
                if db_messages and db_messages[-1].content == user_message and db_messages[-1].role.value == "user":
                    is_duplicate = True
                
                if not is_duplicate:
                    messages.append({"role": "user", "content": user_message})
                
                tools = self._get_tools_definitions()
                
                # First call to model
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    tools=tools,
                    tool_choice="auto"
                )
                
                response_message = response.choices[0].message
                
                # Handle tool calls
                final_response_content = ""
                tool_calls_data = []

                if response_message.tool_calls:
                    print(f"DEBUG: Received {len(response_message.tool_calls)} tool calls")
                    for tc in response_message.tool_calls:
                        print(f"DEBUG: Tool call: {tc.function.name} args={tc.function.arguments}")
                    
                    messages.append(response_message)
                    
                    for tool_call in response_message.tool_calls:
                        function_name = tool_call.function.name
                        try:
                            function_args = json.loads(tool_call.function.arguments)
                        except json.JSONDecodeError:
                            function_args = {}
                        
                        tool_output = await self._execute_tool(function_name, function_args, user_id)
                        
                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": tool_output,
                        })
                        
                        tool_calls_data.append(tool_call)

                    # Add delay to prevent rate limiting
                    await asyncio.sleep(2)

                    # Second call to model to get final response
                    second_response = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=messages
                    )
                    final_response_content = second_response.choices[0].message.content
                else:
                    final_response_content = response_message.content

                
                return {
                    "response": final_response_content,
                    "conversation_id": conversation_id,
                    "status": "success",
                    "tool_calls": [tc.model_dump() for tc in tool_calls_data]
                }
                
        except Exception as e:
            error_message = str(e)
            print(f"Error in Chat Processing: {error_message}")
            return {
                "response": "Processing error. Please try again.",
                "conversation_id": conversation_id,
                "status": "error",
                "error": error_message
            }


# Global instance
assistant_service = OpenAIAssistantService()


async def initialize_assistant_service():
    """No-op initialization for now"""
    pass