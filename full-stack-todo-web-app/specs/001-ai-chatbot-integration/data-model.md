# Data Model: AI-Powered Todo Chatbot

## Entity Definitions

### Conversation
Represents a user's chat session with metadata

**Fields**:
- id (UUID, primary key)
- user_id (int, foreign key to existing User table, required)
- title (string, optional, auto-generated from first message)
- created_at (datetime, required, default: now)
- updated_at (datetime, required, default: now, auto-update)

**Validation rules**:
- user_id must reference an existing user
- created_at and updated_at must be valid timestamps
- title length limited to 200 characters

**State transitions**:
- Created when user initiates first chat
- Updated when new messages are added
- Archived/deleted based on retention policy

### Message
Represents individual exchanges within a conversation

**Fields**:
- id (UUID, primary key)
- conversation_id (UUID, foreign key to Conversation, required)
- role (enum: 'user' | 'assistant' | 'tool', required)
- content (text, required)
- timestamp (datetime, required, default: now)
- tool_calls (JSON, optional, for tool invocations)
- tool_responses (JSON, optional, for tool results)

**Validation rules**:
- conversation_id must reference an existing conversation
- role must be one of the allowed values
- content must not exceed 10,000 characters
- tool_calls and tool_responses must be valid JSON when present

**State transitions**:
- Created when new message is added to conversation
- Immutable once created (append-only model)

## Relationships

### Conversation ↔ Message
- One Conversation to Many Messages (one-to-many)
- Messages are cascade deleted when Conversation is deleted
- Foreign key constraint ensures referential integrity

### Conversation ↔ User
- Many Conversations to One User (many-to-one)
- Foreign key constraint ensures referential integrity
- Conversations remain when user is deactivated (for audit purposes)

## Indexes

### Conversation Table
- Index on user_id for efficient user-specific queries
- Index on updated_at for chronological ordering
- Composite index on (user_id, updated_at) for user timeline queries

### Message Table
- Index on conversation_id for conversation-specific queries
- Index on timestamp for chronological ordering
- Composite index on (conversation_id, timestamp) for conversation timeline queries

## Constraints

### Referential Integrity
- All foreign key references must point to existing records
- Cascade deletion for messages when conversation is deleted

### Data Validation
- All required fields must be present
- Field length limits enforced
- Enum values restricted to allowed options

## Migration Plan

### From Current Schema
1. Add Conversation table with all required fields
2. Add Message table with all required fields
3. Create indexes for optimal query performance
4. Update application code to use new models
5. Add repository/DAO methods for new operations

### Backward Compatibility
- Existing User and Task tables remain unchanged
- New tables integrate seamlessly with existing authentication
- No disruption to existing functionality