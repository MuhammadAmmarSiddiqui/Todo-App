# Quickstart Guide: AI-Powered Todo Chatbot

## Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL database
- OpenAI API key
- Existing full-stack todo app deployed

## Setup

### 1. Environment Configuration

Set the required environment variables:

```bash
export OPENAI_API_KEY="your-openai-api-key"
export DATABASE_URL="postgresql://username:password@localhost:5432/todo_app"
export SECRET_KEY="your-jwt-secret-key"
export MCP_SERVER_URL="http://localhost:8080" # if running MCP server separately
```

### 2. Database Migration

Run the database migrations to create the new Conversation and Message tables:

```bash
# From the backend directory
cd backend
python -m alembic upgrade head
```

### 3. Install Dependencies

Install backend dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Install frontend dependencies:

```bash
cd frontend
npm install
```

## Running the Application

### 1. Start the MCP Server

```bash
cd backend/mcp_server
python mcp_server.py
```

### 2. Start the Backend

```bash
cd backend
uvicorn main:app --reload --port=8000
```

### 3. Start the Frontend

```bash
cd frontend
npm run dev
```

## Using the Chat Interface

### 1. Authentication

The chat interface automatically uses the existing authentication system. Users must be logged in to use the chatbot.

### 2. Starting a Conversation

Navigate to the chat interface in the application (typically at `/chat`). You can start interacting with the bot using natural language commands like:

- "Add a task to buy groceries"
- "What's pending?"
- "Complete the meeting prep task"
- "Delete the old task"

### 3. Conversation History

Previous conversations are accessible from the chat history panel. Each conversation is tied to your user account and persists between sessions.

## API Endpoints

### Chat Endpoint
```
POST /api/v1/chat/{user_id}/
```

Request:
```json
{
  "message": "What tasks do I have pending?",
  "conversation_id": "optional-conversation-id"
}
```

Response:
```json
{
  "response": "You have 3 pending tasks: Buy groceries, Call mom, Finish report",
  "conversation_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "tool_calls": [
    {
      "name": "list_tasks",
      "arguments": {"completed": false}
    }
  ]
}
```

### Conversation History
```
GET /api/v1/chat/{user_id}/conversations
```

### Specific Conversation
```
GET /api/v1/chat/{user_id}/conversation/{conversation_id}
```

## Development

### Adding New MCP Tools

To add new capabilities to the chatbot, create new MCP tools in the `backend/mcp_server/tools/` directory:

```python
from mcp import server
import openai

def register_tools(mcp_server: server.Server):
    @mcp_server.tool(
        "custom_tool_name",
        description="Description of what the tool does",
        parameters={
            "param1": {
                "type": "string",
                "description": "Description of param1"
            }
        }
    )
    async def custom_tool(param1: str) -> dict:
        # Implementation of the tool
        return {"result": "success"}
```

### Modifying the Chat UI

The chat interface components are located in `frontend/src/components/chat/`. Key files include:

- `ChatInterface.jsx` - Main chat component
- `MessageList.jsx` - Displays conversation history
- `MessageInput.jsx` - Handles user input
- `ConversationHistory.jsx` - Sidebar for conversation navigation

## Troubleshooting

### Common Issues

1. **API Keys Not Working**: Verify that your OpenAI API key is correctly set in environment variables
2. **Database Connection Errors**: Check that your DATABASE_URL is correctly configured
3. **JWT Token Issues**: Ensure the authentication flow is working correctly between frontend and backend
4. **MCP Server Not Responding**: Verify that the MCP server is running and accessible

### Debugging Tips

Enable detailed logging by setting:
```bash
export LOG_LEVEL="DEBUG"
```

Check the logs in the respective backend and frontend consoles for error messages.