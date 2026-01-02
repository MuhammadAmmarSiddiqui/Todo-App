# Data Model: Session Commands for CLI Todo App

## Entities

### Task
- **id**: int (unique identifier, auto-generated)
- **title**: str (required, non-empty)
- **description**: Optional[str] (nullable)
- **completed**: bool (default: False)
- **created_at**: datetime (auto-generated when created)

### Session
- **active**: bool (indicates if session is running)
- **tasks**: List[Task] (in-memory storage of tasks during session)
- **prompt**: str (interactive prompt indicator, e.g., "todo> ")

## State Transitions

### Task States
- **Incomplete** (default) → **Complete** (via complete command)
- **Complete** → **Incomplete** (via incomplete command)

### Session States
- **Inactive** (default) → **Active** (via start command)
- **Active** → **Inactive** (via exit command or Ctrl+C/Ctrl+D)

## Validation Rules

### Task Validation
- Title must not be empty or whitespace-only
- ID must be positive integer
- Description length must not exceed 500 characters (optional)

### Session Validation
- Commands can only be executed in active session state
- Invalid commands during session should show error but maintain session state
- Session must maintain data isolation between different runs