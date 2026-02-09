# AI-Powered Todo Chatbot Implementation

This document describes the implementation of the AI-powered todo chatbot feature that allows users to manage their todo lists using natural language commands.

## Architecture

The chatbot implementation consists of several components:

### Backend Components

1. **Models**:
   - `Conversation` - Represents a chat session with metadata
   - `Message` - Represents individual exchanges within a conversation

2. **Repositories**:
   - `ConversationRepository` - Handles CRUD operations for conversations
   - `MessageRepository` - Handles CRUD operations for messages

3. **Services**:
   - `OpenAIAssistantService` - Integrates with OpenAI's API to process natural language

4. **MCP Server**:
   - Implements Model Context Protocol server
   - Provides tools for task operations (add, list, complete, delete)

5. **API Routes**:
   - `/api/v1/chat/{user_id}/` - Process natural language input
   - `/api/v1/chat/{user_id}/conversations` - Retrieve conversation history
   - `/api/v1/chat/{user_id}/conversation/{conversation_id}` - Retrieve specific conversation

### Frontend Components

1. **ChatInterface** - Main chat component with conversation history sidebar
2. **MessageList** - Displays conversation messages with appropriate styling
3. **MessageInput** - Handles user input submission
4. **ConversationHistory** - Shows list of previous conversations

## Data Flow

1. User sends a natural language command (e.g., "Add a task to buy groceries")
2. Frontend sends the message to the backend chat API
3. Backend creates a message record and sends the request to OpenAI
4. OpenAI assistant determines if tools are needed (e.g., add_task)
5. If tools are needed, the MCP server executes the appropriate task operation
6. OpenAI generates a response based on the tool results
7. Backend stores the assistant's response as a message
8. Response is sent back to the frontend for display

## Security Considerations

- JWT tokens are validated for all requests
- Users can only access their own conversations
- User ID in token is validated against the requested user ID
- MCP tools validate that users can only operate on their own tasks

## Environment Variables

The following environment variables need to be configured:

- `OPENAI_API_KEY` - API key for OpenAI services
- `DATABASE_URL` - Connection string for the PostgreSQL database
- `SECRET_KEY` - Secret key for JWT token signing
- `MCP_SERVER_URL` - URL for the MCP server (if running separately)

## Error Handling

- API requests return appropriate HTTP status codes
- Client-side error handling with toast notifications
- Server-side logging of errors for debugging
- Graceful degradation when OpenAI services are unavailable

## Future Enhancements

- Streaming responses for better user experience
- Support for file attachments in chat
- Enhanced conversation memory and context
- Voice input/output capabilities
- Advanced task management features (due dates, priorities, categories)