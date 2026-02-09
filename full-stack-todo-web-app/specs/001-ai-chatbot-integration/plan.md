# Implementation Plan: AI-Powered Todo Chatbot

**Feature**: AI-Powered Todo Chatbot Implementation  
**Spec File**: [spec.md](spec.md)  
**Branch**: `001-ai-chatbot-integration`  
**Created**: 2026-02-07  
**Status**: Active  

## Technical Context

### System Overview
- **Existing Components**: Full-stack todo web app with authentication, task management, and UI
- **New Components**: MCP server, OpenAI Agents integration, chat UI, conversation persistence
- **Integration Points**: Existing task database, authentication system, API layer

### Dependencies
- OpenAI Agents SDK
- MCP (Model Context Protocol) Server
- ChatKit frontend library
- PostgreSQL database for conversation storage
- Existing backend authentication system

### Architecture Elements
- **Frontend**: React components for chat interface using ChatKit
- **Backend**: FastAPI endpoints for chat functionality
- **Database**: New Conversation and Message models alongside existing Task/User models
- **External Services**: OpenAI API, MCP tools for task operations

### Known Unknowns
- Specific MCP server setup and configuration details
- OpenAI Agents SDK integration patterns with FastAPI
- Performance implications of real-time chat processing
- Token propagation mechanism from frontend to MCP tools

### Technology Stack
- **Frontend**: React, ChatKit, Tailwind CSS
- **Backend**: Python, FastAPI, SQLAlchemy
- **Database**: PostgreSQL
- **AI/ML**: OpenAI Agents SDK, MCP SDK
- **Authentication**: JWT tokens

## Constitution Check

### Compliance Verification
- [x] Library-first approach: Isolate chatbot logic as reusable components
- [x] CLI Interface: Consider if any components need CLI access
- [x] Test-first development: All new functionality must have tests
- [x] Integration testing: Test chatbot integration with existing features
- [x] Observability: Implement proper logging for debugging
- [x] Backward compatibility: Preserve existing functionality

### Security Requirements
- [x] JWT token propagation to maintain user identity
- [x] Input validation for natural language commands
- [x] Rate limiting for API endpoints
- [x] Proper authentication for all new endpoints

### Performance Standards
- [x] Real-time response for chat interactions
- [x] Efficient database queries for conversation history
- [x] Caching mechanisms where appropriate

## Gates

### Pre-Development
- [x] Architecture approval for new components
- [x] Security review for token propagation mechanism
- [x] Database schema review for new models
- [x] Performance requirements validated

### During Development
- [x] All new code follows existing project conventions
- [x] Authentication tokens properly propagated through system
- [x] New database models compatible with existing schema
- [x] MCP tools properly isolated and secure

### Pre-Merge
- [x] All tests passing (unit, integration, E2E)
- [x] Security audit passed
- [x] Performance benchmarks met
- [x] Documentation updated
- [x] Backwards compatibility verified

## Phase 0: Outline & Research

### Research Tasks
1. **MCP Server Setup**: Research best practices for implementing an MCP server with the official SDK
2. **OpenAI Agents Integration**: Investigate patterns for integrating OpenAI Agents SDK with FastAPI
3. **Token Propagation**: Study methods for securely propagating JWT tokens to MCP tools
4. **ChatKit Integration**: Explore ChatKit implementation with React and existing UI
5. **Database Schema**: Validate new Conversation/Message models with existing schema

### Expected Outcomes
- Detailed understanding of MCP server implementation
- Clear approach for OpenAI Agents integration
- Secure token propagation mechanism
- Efficient database design for conversation history
- Integration plan with existing components

## Phase 1: Design & Contracts

### Data Model Design
#### New Database Models
- **Conversation Model**:
  - id (UUID)
  - user_id (foreign key to existing User table)
  - created_at (timestamp)
  - updated_at (timestamp)
  - title (optional, auto-generated from first message)

- **Message Model**:
  - id (UUID)
  - conversation_id (foreign key to Conversation)
  - role ('user' | 'assistant' | 'tool')
  - content (text)
  - timestamp
  - tool_calls (JSON for tool invocations)
  - tool_responses (JSON for tool results)

### API Contract Design
#### New Endpoints
- `POST /api/v1/chat/{user_id}/` - Process natural language input and return AI response
- `GET /api/v1/chat/{user_id}/conversations` - Retrieve user's conversation history
- `GET /api/v1/chat/{user_id}/conversation/{conv_id}` - Retrieve specific conversation
- `DELETE /api/v1/chat/{user_id}/conversation/{conv_id}` - Delete specific conversation

### MCP Tool Definitions
#### Available Tools
- `add_task(description: str)` - Creates a new task for the authenticated user
- `list_tasks(completed: bool = False)` - Lists tasks for the authenticated user
- `complete_task(task_id: int)` - Marks a task as completed for the authenticated user
- `delete_task(task_id: int)` - Deletes a task for the authenticated user

## Phase 2: Implementation Plan

### Implementation Steps
1. **Database Layer**
   - Create Conversation and Message models
   - Implement database migrations
   - Add repository/DAO classes for new models

2. **MCP Server**
   - Set up MCP server with official SDK
   - Implement task operation tools
   - Connect tools to existing task management system
   - Ensure proper user isolation

3. **Backend API**
   - Create chat endpoints in FastAPI
   - Integrate OpenAI Agents SDK
   - Implement token propagation mechanism
   - Connect to MCP server
   - Add conversation persistence

4. **Frontend Components**
   - Create chat UI components using ChatKit
   - Integrate with existing authentication
   - Connect to backend chat API
   - Handle conversation history display

5. **Integration & Testing**
   - End-to-end testing of chat functionality
   - Natural language command validation
   - Security testing for token handling
   - Performance testing

## Phase 3: Validation & Deployment

### Acceptance Criteria
- [ ] Natural language commands like "What's pending?" work correctly
- [ ] Conversation history persists across sessions
- [ ] All task operations (add/list/complete/delete) work via chat
- [ ] JWT tokens properly propagate to MCP tools
- [ ] User isolation maintained in multi-user environment
- [ ] Existing functionality remains unaffected

### Testing Strategy
- Unit tests for MCP tools
- Integration tests for chat API
- E2E tests for full chat workflow
- Security tests for authentication
- Performance tests for response times

### Deployment Plan
- Deploy MCP server separately or as part of main service
- Update environment configurations
- Migrate database schema
- Monitor performance and usage