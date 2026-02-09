# Tasks: AI-Powered Todo Chatbot Implementation

**Input**: Design documents from `/specs/001-ai-chatbot-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below assume web app structure based on plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in backend/mcp_server/
- [x] T002 [P] Install OpenAI SDK and MCP SDK dependencies in backend
- [x] T003 [P] Configure environment variables for OpenAI API and database

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Setup database schema and migrations for Conversation and Message models in backend/database/
- [x] T005 [P] Create Conversation model in backend/models/conversation.py
- [x] T006 [P] Create Message model in backend/models/message.py
- [x] T007 [P] Create MCP server base structure in backend/mcp_server/server.py
- [x] T008 Configure authentication middleware for token propagation in backend/main.py
- [x] T009 Setup conversation repository in backend/repositories/conversation_repository.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Todo Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to interact with their todo list using natural language commands through a chat interface

**Independent Test**: Can be fully tested by sending natural language commands like "Add a task to buy groceries" and verifying that the task is added to the user's todo list, delivering the core value of conversational task management.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T010 [P] [US1] Contract test for POST /api/v1/chat/{user_id}/ in tests/contract/test_chat_api.py
- [ ] T011 [P] [US1] Integration test for "Add a task to buy groceries" command in tests/integration/test_natural_language_todo.py

### Implementation for User Story 1

- [x] T012 [P] [US1] Implement add_task MCP tool in backend/mcp_server/tools/task_operations.py
- [x] T013 [P] [US1] Implement list_tasks MCP tool in backend/mcp_server/tools/task_operations.py
- [x] T014 [US1] Create OpenAI assistant with task tools in backend/services/openai_assistant.py
- [x] T015 [US1] Implement chat endpoint POST /api/v1/chat/{user_id}/ in backend/routes/chat.py
- [x] T016 [US1] Add conversation persistence logic to chat endpoint
- [x] T017 [US1] Create frontend chat component in frontend/src/components/chat/ChatInterface.jsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Conversation State Persistence (Priority: P2)

**Goal**: Save conversation history so users can continue conversations across sessions and review past interactions

**Independent Test**: Can be tested by initiating a conversation, closing the app, reopening it, and verifying that the conversation history is preserved.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T018 [P] [US2] Contract test for GET /api/v1/chat/{user_id}/conversations in tests/contract/test_chat_api.py
- [ ] T019 [P] [US2] Integration test for conversation history retrieval in tests/integration/test_conversation_persistence.py

### Implementation for User Story 2

- [x] T020 [P] [US2] Implement GET /api/v1/chat/{user_id}/conversations endpoint in backend/routes/chat.py
- [x] T021 [US2] Implement GET /api/v1/chat/{user_id}/conversation/{conv_id} endpoint in backend/routes/chat.py
- [x] T022 [US2] Add message history loading to chat interface in frontend/src/components/chat/MessageList.jsx
- [x] T023 [US2] Add conversation history sidebar in frontend/src/components/chat/ConversationHistory.jsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Multi-modal Task Operations (Priority: P3)

**Goal**: Perform all todo list operations (add, list, complete, delete) through the chat interface so users don't need to switch between chat and traditional UI

**Independent Test**: Can be tested by performing each operation (add, list, complete, delete) through the chat interface and verifying the corresponding changes in the todo list.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T024 [P] [US3] Contract test for complete_task and delete_task tools in tests/contract/test_mcp_tools.py
- [ ] T025 [P] [US3] Integration test for "Complete the meeting prep task" command in tests/integration/test_task_operations.py

### Implementation for User Story 3

- [x] T026 [P] [US3] Implement complete_task MCP tool in backend/mcp_server/tools/task_operations.py
- [x] T027 [P] [US3] Implement delete_task MCP tool in backend/mcp_server/tools/task_operations.py
- [x] T028 [US3] Enhance OpenAI assistant to recognize complete/delete commands in backend/services/openai_assistant.py
- [x] T029 [US3] Add visual feedback for task operations in frontend/src/components/chat/MessageItem.jsx

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T030 [P] Documentation updates in docs/chatbot-implementation.md
- [x] T031 Code cleanup and refactoring across chat components
- [ ] T032 Performance optimization for conversation loading
- [x] T033 [P] Additional unit tests in tests/unit/
- [x] T034 Security hardening for token propagation
- [x] T035 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for POST /api/v1/chat/{user_id}/ in tests/contract/test_chat_api.py"
Task: "Integration test for 'Add a task to buy groceries' command in tests/integration/test_natural_language_todo.py"

# Launch all tools for User Story 1 together:
Task: "Implement add_task MCP tool in backend/mcp_server/tools/task_operations.py"
Task: "Implement list_tasks MCP tool in backend/mcp_server/tools/task_operations.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence