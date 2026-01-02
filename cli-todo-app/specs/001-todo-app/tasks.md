# Tasks: Todo In-Memory Python Console App

**Feature**: 001-todo-app
**Generated**: 2025-12-29
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

## Implementation Strategy

**MVP Scope**: User Story 1 (Add Tasks) + User Story 2 (View Tasks) - provides basic functionality for a working todo app that users can add tasks to and view them.

**Delivery Approach**: Incremental delivery with each user story being independently testable. Tasks are organized in dependency order with foundational work first, then user stories in priority order (P1, P2, P3).

**Parallel Execution Opportunities**: Tasks within different components (models, services, CLI) can be developed in parallel after foundational setup is complete.

---

## Phase 1: Setup Tasks

### Goal
Initialize the project structure and development environment following the specified tech stack.

- [X] T001 Create project directory structure with src/, tests/, and pyproject.toml
- [X] T002 Initialize UV project and configure Python 3.13+ requirements
- [X] T003 Set up basic configuration files (.gitignore, .python-version)
- [X] T004 Create directory structure: src/models/, src/services/, src/cli/, tests/unit/, tests/integration/

---

## Phase 2: Foundational Tasks

### Goal
Implement the foundational components that all user stories depend on.

- [X] T005 [P] Create Task data model in src/models/task.py with proper type hints
- [X] T006 [P] Create TodoService class in src/services/todo_service.py with in-memory storage
- [X] T007 [P] Create basic CLI structure in src/cli/main.py using argparse
- [X] T008 [P] Implement task ID generation logic in TodoService
- [X] T009 [P] Set up basic error handling and validation in TodoService

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1)

### Goal
Enable users to add new tasks with a title and description, with unique ID auto-assignment.

### Independent Test Criteria
Can be fully tested by running the add task command with title and description parameters and verifying that a new task with a unique ID appears in the task list.

- [X] T010 [P] [US1] Implement add_task method in TodoService with title validation
- [X] T011 [P] [US1] Implement add CLI command in main.py with --title and --description arguments
- [X] T012 [P] [US1] Connect CLI add command to TodoService add_task method
- [X] T013 [US1] Test: Add a task with title and description and verify it's stored correctly
- [X] T014 [US1] Test: Add multiple tasks and verify they get unique sequential IDs
- [X] T015 [US1] Test: Attempt to add task with empty title and verify proper error handling

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

### Goal
Allow users to view all tasks in a formatted list showing ID, Status, Title, and Description.

### Independent Test Criteria
Can be fully tested by adding a few tasks and then running the view tasks command to see them displayed in a formatted table.

- [X] T016 [P] [US2] Implement get_all_tasks method in TodoService
- [X] T017 [P] [US2] Implement list CLI command in main.py
- [X] T018 [P] [US2] Connect CLI list command to TodoService get_all_tasks method
- [X] T019 [P] [US2] Format task display with ID, status ([ ] or [x]), title, and description
- [X] T020 [US2] Test: Add tasks and verify they display correctly in formatted list
- [X] T021 [US2] Test: Verify appropriate message when no tasks exist
- [X] T022 [US2] Test: Verify task status is properly displayed as [ ] or [x]

---

## Phase 5: User Story 3 - Mark Tasks Complete/Incomplete (Priority: P2)

### Goal
Allow users to mark tasks as complete or incomplete to track progress.

### Independent Test Criteria
Can be fully tested by adding a task, marking it complete, then viewing it to confirm the status has changed, and toggling it back to incomplete.

- [X] T023 [P] [US3] Implement mark_complete and mark_incomplete methods in TodoService
- [X] T024 [P] [US3] Implement complete CLI command in main.py with --id argument
- [X] T025 [P] [US3] Implement incomplete CLI command in main.py with --id argument
- [X] T026 [P] [US3] Connect CLI complete/incomplete commands to TodoService methods
- [X] T027 [US3] Test: Mark a task complete and verify status changes from [ ] to [x]
- [X] T028 [US3] Test: Mark a task incomplete and verify status changes from [x] to [ ]
- [X] T029 [US3] Test: Attempt to mark non-existent task and verify error handling

---

## Phase 6: User Story 4 - Update Task Details (Priority: P2)

### Goal
Allow users to update the title and/or description of existing tasks using the Task ID.

### Independent Test Criteria
Can be fully tested by adding a task, updating its title and description, then viewing it to confirm the changes were saved.

- [X] T030 [P] [US4] Implement update_task method in TodoService with validation
- [X] T031 [P] [US4] Implement update CLI command in main.py with --id, --title, and --description arguments
- [X] T032 [P] [US4] Connect CLI update command to TodoService update_task method
- [X] T033 [US4] Test: Update task title and description and verify changes are saved
- [X] T034 [US4] Test: Update only title and verify description remains unchanged
- [X] T035 [US4] Test: Update only description and verify title remains unchanged
- [X] T036 [US4] Test: Attempt to update non-existent task and verify error handling

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P3)

### Goal
Allow users to delete tasks that they no longer need to keep the todo list clean.

### Independent Test Criteria
Can be fully tested by adding a task, deleting it, then viewing the task list to confirm it's no longer present.

- [X] T037 [P] [US5] Implement delete_task method in TodoService
- [X] T038 [P] [US5] Implement delete CLI command in main.py with --id argument
- [X] T039 [P] [US5] Connect CLI delete command to TodoService delete_task method
- [X] T040 [US5] Test: Delete a task and verify it's removed from the list
- [X] T041 [US5] Test: Verify deleted task no longer appears in list view
- [X] T042 [US5] Test: Attempt to delete non-existent task and verify error handling

---

## Phase 8: Polish & Cross-Cutting Concerns

### Goal
Complete the application with proper error handling, validation, and user experience improvements.

- [X] T043 Add comprehensive error handling throughout CLI interface
- [X] T044 Add input validation for all CLI commands and parameters
- [X] T044A Add validation for title length (min 1 character, max 200 characters)
- [X] T044B Add validation for description length (max 1000 characters)
- [X] T044C Add validation for valid task ID format and range
- [X] T044D Add validation for required vs optional parameters
- [X] T045 Implement proper help text and usage examples for all commands
- [X] T046 Add type hints to all functions and methods
- [X] T047 Create comprehensive integration tests for all user stories
- [X] T048 Add logging for debugging and error tracking
- [X] T049 Optimize performance for typical usage scenarios
- [X] T050 Document the API and usage in README format
- [X] T051 Add pytest configuration with 80%+ coverage requirement
- [X] T052 Create unit tests for all models with 80%+ coverage
- [X] T053 Create unit tests for all services with 80%+ coverage
- [X] T054 Create integration tests for CLI with 80%+ coverage
- [X] T055 Set up coverage reporting and validation

---

## Phase 8.5: Edge Case Handling

### Goal
Address all edge cases specified in the feature specification.

- [X] T056 Handle invalid commands or parameters with appropriate error messages
- [X] T057 Validate and handle empty titles/descriptions when adding/updating tasks
- [X] T058 Implement length limits for very long titles or descriptions (e.g., max 1000 characters)
- [X] T059 Handle operations on non-existent task IDs gracefully
- [X] T060 Document in-memory data loss behavior when application closes/reopens

---

## Dependencies

- **User Story 2 (View Tasks)** depends on foundational task storage being available (Phase 2)
- **User Story 3 (Mark Complete/Incomplete)** depends on Task model with status field (Phase 2)
- **User Story 4 (Update Tasks)** depends on Task model and storage (Phase 2)
- **User Story 5 (Delete Tasks)** depends on Task model and storage (Phase 2)
- **Phase 8.5 (Edge Case Handling)** depends on all core functionality being implemented (Phase 7)

## Parallel Execution Examples

1. **After Phase 2**: User stories 1, 2, 3, 4, and 5 can be developed in parallel by different developers
2. **Within each user story**: Model, Service, and CLI components can be developed in parallel if the interfaces are well-defined
3. **Testing**: Unit tests can be written in parallel with implementation for each component

## Task Validation

All tasks follow the required format:
- [ ] Checkboxes for tracking progress
- [ ] Sequential Task IDs (T001, T002, etc.)
- [ ] [P] markers for parallelizable tasks
- [ ] [USx] labels for user story tasks
- [ ] Specific file paths mentioned in task descriptions