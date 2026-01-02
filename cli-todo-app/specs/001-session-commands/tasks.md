---
description: "Task list for implementing session commands for CLI Todo App"
---

# Tasks: Session Commands for CLI Todo App

**Input**: Design documents from `/specs/001-session-commands/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Update existing CLI structure to support session mode in src/cli/main.py
- [X] T002 [P] Update argparse to handle session commands in src/cli/main.py
- [X] T003 [P] Create session state management in src/cli/main.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Implement interactive session loop in src/cli/main.py
- [X] T005 [P] Add session state tracking to TodoCLI class in src/cli/main.py
- [X] T006 [P] Create command parsing for interactive mode in src/cli/main.py
- [X] T007 Update TodoCLI to maintain persistent data during sessions in src/cli/main.py
- [X] T008 Add error handling for session mode in src/cli/main.py
- [X] T009 Implement graceful exit functionality in src/cli/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Persistent Session Mode (Priority: P1) 🎯 MVP

**Goal**: Enable persistent session mode where tasks persist in memory between commands until user explicitly exits

**Independent Test**: Can be fully tested by starting the session, adding tasks, listing them, and then exiting. The functionality should work continuously during the session without data loss between commands within the session.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Integration test for session persistence in tests/integration/test_session_mode.py
- [ ] T011 [P] [US1] Unit test for interactive command loop in tests/unit/test_cli_session.py

### Implementation for User Story 1

- [X] T012 [P] [US1] Implement start command handler in src/cli/main.py
- [X] T013 [US1] Implement interactive command loop with persistent data in src/cli/main.py
- [X] T014 [US1] Add session state management (active/inactive) in src/cli/main.py
- [X] T015 [US1] Implement exit command handler in src/cli/main.py
- [X] T016 [US1] Add interactive prompt indicator ("todo> ") in src/cli/main.py
- [X] T017 [US1] Test session persistence with add/list/exit workflow in src/cli/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Session Command Interface (Priority: P1)

**Goal**: Implement specific commands to control the session lifecycle (start/exit) with all existing todo functionality available during the session

**Independent Test**: Can be fully tested by verifying that the start command initializes a session, commands work during the session, and exit command properly terminates it.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T018 [P] [US2] Contract test for start/exit commands in tests/contract/test_session_commands.py
- [ ] T019 [P] [US2] Integration test for session lifecycle in tests/integration/test_session_lifecycle.py

### Implementation for User Story 2

- [X] T020 [P] [US2] Implement help command for session mode in src/cli/main.py
- [X] T021 [US2] Add session command detection in src/cli/main.py
- [X] T022 [US2] Implement graceful session termination in src/cli/main.py
- [X] T023 [US2] Add session mode indicators and messaging in src/cli/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - In-Session Command Execution (Priority: P2)

**Goal**: Enable all existing todo commands (add, list, update, delete, complete, incomplete) to work within the persistent session with data persistence

**Independent Test**: Can be fully tested by starting a session, running various todo commands, and verifying they work with persistent data during the session.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T024 [P] [US3] Integration test for in-session command execution in tests/integration/test_session_commands.py
- [ ] T025 [P] [US3] Unit test for all command persistence in tests/unit/test_command_persistence.py

### Implementation for User Story 3

- [X] T026 [P] [US3] Adapt add command for session mode in src/cli/main.py
- [X] T027 [P] [US3] Adapt list command for session mode in src/cli/main.py
- [X] T028 [P] [US3] Adapt update command for session mode in src/cli/main.py
- [X] T029 [P] [US3] Adapt delete command for session mode in src/cli/main.py
- [X] T030 [P] [US3] Adapt complete command for session mode in src/cli/main.py
- [X] T031 [P] [US3] Adapt incomplete command for session mode in src/cli/main.py
- [X] T032 [US3] Ensure all commands work with persistent data in src/cli/main.py
- [X] T033 [US3] Maintain same command syntax and behavior in session mode in src/cli/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T034 [P] Documentation updates in docs/ or README.md
- [ ] T035 Code cleanup and refactoring of CLI implementation
- [ ] T036 Performance optimization for session mode
- [ ] T037 [P] Additional unit tests in tests/unit/
- [ ] T038 Error handling and edge case management
- [ ] T039 Run quickstart.md validation scenarios
- [ ] T040 [P] Update help and usage messages for session mode in src/cli/main.py

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
Task: "Integration test for session persistence in tests/integration/test_session_mode.py"
Task: "Unit test for interactive command loop in tests/unit/test_cli_session.py"

# Launch all implementation tasks for User Story 1 together:
Task: "Implement start command handler in src/cli/main.py"
Task: "Implement interactive command loop with persistent data in src/cli/main.py"
Task: "Add session state management (active/inactive) in src/cli/main.py"
Task: "Implement exit command handler in src/cli/main.py"
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