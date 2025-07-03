# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DateTree is a collaborative task and event management system with a FastAPI backend and Flutter frontend. The backend uses PostgreSQL with async operations, while the Flutter app provides cross-platform mobile access. The project follows modern development practices with comprehensive testing and documentation.

## Essential Commands

### Development Server
```bash
cd backend
uv run uvicorn app.main:app --reload
```
- API runs at http://127.0.0.1:8000
- Swagger docs at http://127.0.0.1:8000/docs

### Testing
```bash
cd backend
uv run pytest                                    # Run all tests
uv run pytest -v                                 # Verbose output
uv run pytest tests/test_api_list.py            # Run specific test file
uv run pytest -k "test_create_list"             # Run tests matching pattern
```

### Database Operations
```bash
cd backend
uv run alembic upgrade head                      # Apply migrations
uv run alembic revision --autogenerate -m "msg"  # Create new migration
uv run alembic downgrade -1                      # Rollback one migration
```

### Code Quality
```bash
cd backend
uv run ruff check .                              # Check code style
uv run ruff format .                             # Format code
```

### Flutter Development
```bash
cd mobile
flutter pub get                                  # Install dependencies
flutter run -d chrome                           # Run on web
flutter run                                      # Run on default device
flutter test                                     # Run unit tests
flutter packages pub run build_runner build     # Generate code
```

## Architecture Overview

### Directory Structure

#### Backend
```
backend/app/
├── api/v1/          # API endpoints (users, lists, calendars)
├── core/            # Config, database, security utilities
├── crud/            # Database operations layer
├── models/          # SQLAlchemy ORM models
└── schemas/         # Pydantic validation schemas
```

#### Flutter Frontend
```
mobile/lib/
├── core/
│   ├── constants/   # App constants and configuration
│   ├── theme/       # Material 3 theme definitions
│   ├── providers/   # Global Riverpod providers
│   └── services/    # Core services
├── features/
│   ├── auth/        # Authentication screens and logic
│   ├── todo/        # Todo management features
│   ├── vote/        # Voting and collaboration features
│   ├── calendar/    # Calendar views and events
│   └── profile/     # User profile and settings
└── shared/
    ├── widgets/     # Atomic design components
    │   ├── atoms/   # Basic UI elements
    │   ├── molecules/ # Composite components
    │   ├── organisms/ # Complex components
    │   └── templates/ # Page layouts
    └── models/      # Data models
```

### Key Architectural Patterns

#### Backend
1. **Layered Architecture**: API → CRUD → Models with Schemas for validation
2. **Async Database Operations**: All database queries use async SQLAlchemy
3. **Dependency Injection**: FastAPI dependencies for database sessions and authentication
4. **Multi-tenant Calendars**: Users can own/share multiple calendars with different permissions

#### Frontend
1. **Atomic Design**: Modular component hierarchy (atoms → molecules → organisms → templates)
2. **State Management**: Riverpod for reactive state management
3. **Mobile-first Design**: Cross-platform with platform-specific optimizations
4. **Offline-first**: Local storage with server synchronization

### Database Relationships
- User ↔ Calendar (many-to-many via UserCalendar with permissions)
- Calendar → List (one-to-many, different list types)
- List → ListItem (one-to-many)
- ListItem ← Vote (for collaborative prioritization)
- Calendar → Event (scheduled events)

### Authentication Flow
1. JWT tokens stored in HTTP-only cookies
2. User registration creates default personal calendar
3. Calendar access controlled by UserCalendar permissions (owner/editor/viewer)

## Development Guidelines

### Code Style Requirements
- **No non-text symbols in code**: Avoid using Unicode symbols, emojis, or special characters in Python code comments, variable names, or strings
- **Documentation files (.md) can use non-ASCII**: Markdown files, including Chinese characters and Unicode symbols, are allowed for better readability
- Use plain ASCII characters for all Python code elements to ensure compatibility across different systems and editors

### When Adding New Features
1. Check existing patterns in similar files (e.g., other CRUD operations)
2. Update both schemas and models if database changes needed
3. Create Alembic migration for model changes
4. Write tests following existing test patterns
5. API endpoints should follow RESTful conventions in `api/v1/`

### Before Making Major Changes
**ALWAYS ask the user first** when planning:
- **Architectural changes**: Modifying database schemas, API structure, or core patterns
- **New features**: Adding new entities, endpoints, or significant functionality
- **Breaking changes**: Changes that affect existing API contracts or database structure
- **File restructuring**: Moving or renaming core files and directories
- **Dependency changes**: Adding new major libraries or changing package versions

### Documentation Requirements
For any significant changes, **MUST update documentation FIRST**:
1. **Create/update implementation docs** in `/docs/implementation/` for new APIs
2. **Update API documentation** in `/docs/api/rest-api.md` for new endpoints
3. **Create ADR** in `/docs/adr/` for architectural decisions
4. **Update README.md** status section for completed features
5. **Update this CLAUDE.md** for process or guideline changes

### Git Commit Guidelines
**NEVER automatically commit changes** unless explicitly requested by the user. Instead:

1. **Complete the work** requested by the user
2. **At appropriate milestones**, proactively suggest committing:
   - After completing a significant feature
   - After fixing important bugs
   - After updating documentation
   - After adding comprehensive tests
   - Before starting major refactoring

3. **Suggested commit prompts**:
   - "Would you like me to create a git commit for the new API implementation?"
   - "Should I commit these test improvements and documentation updates?"
   - "Ready to commit the bug fixes and enhancements?"

4. **Always prepare commit messages** when suggesting, but wait for user approval

5. **Exception**: Only auto-commit when user explicitly says "commit this" or "git commit"

### Testing Approach
- Tests use SQLite in-memory database (not PostgreSQL)
- Each test gets isolated database via fixtures
- Mock external dependencies (like password hashing in some tests)
- Test files mirror source structure (test_api_*, test_crud_*, test_schemas_*)

### Common Patterns
```python
# CRUD operations always use async
async def create_item(db: AsyncSession, item: ItemCreate) -> Item:
    db_item = Item(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

# API endpoints use dependency injection
@router.post("/items")
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await crud.create_item(db, item)
```

## Current Implementation Status

### Backend (Complete ✅)
- ✅ User registration and authentication (JWT)
- ✅ Calendar management with permissions
- ✅ List CRUD operations
- ✅ ListItem, Vote, and Event APIs - Complete REST API system
- ✅ Comprehensive test suite (140+ tests) with full coverage
- ✅ Complete API documentation with relationship explanations and usage examples

### Flutter Frontend (In Development 🚧)
- ✅ Project architecture with atomic design pattern
- ✅ Core navigation with 4 main screens (Todo, Vote, Calendar, Profile)
- ✅ Authentication screens (Login, Register)
- ✅ UI component library (atoms, molecules, templates)
- ✅ State management with Riverpod
- ✅ Material 3 theme system with dark mode support
- ✅ Complete API integration with backend FastAPI service
- ✅ Dynamic calendar management (removed hardcoded categories)
- ✅ Data model alignment with backend API specifications
- ✅ Proper HTTP endpoint mapping and JSON serialization
- 🚧 Core functionality implementation (todo management, voting, events)
- 🚧 Offline-first data synchronization

## Important Notes

### Backend Development
1. Always run tests before committing changes
2. Database migrations must be tested with upgrade/downgrade cycle
3. Use environment variables from `.env` (copy from `.env.example`)
4. Docker Compose provides PostgreSQL database for development
5. Package management uses `uv` (not pip or poetry)

### Flutter Development
1. Follow atomic design pattern for UI components
2. Use Riverpod for state management, avoid direct state mutations
3. Implement offline-first approach with local caching
4. Test on both iOS and Android simulators/devices
5. Use code generation for serialization and API clients
6. Follow Material 3 design guidelines
7. Maintain performance targets: <3s cold start, <200ms interactions

## Project Maintenance Guidelines

### When Cleaning/Organizing Project
When asked to clean up or organize the project, **ONLY** remove these types of files:
- **AI assistant files**: `GEMINI.md`, `IMPLEMENTATION_LOG.md`, etc.
- **Migration backups**: Only when explicitly mentioned (e.g., `alembic/versions/backup/`)

### DO NOT automatically clean:
- `.DS_Store` files (macOS system files - not worth the time)
- `__pycache__/` directories (Python runtime cache - regenerated automatically)
- `*.pyc` files (Python compiled bytecode - not harmful)
- `.pytest_cache/` (pytest cache - improves test performance)
- Any files in `.venv/` (virtual environment dependencies)
- Test databases like `test.db` (unless specifically asked)

### Focus cleanup efforts on:
- Outdated documentation files
- Duplicate or conflicting files
- Large unnecessary files that impact repository size
- Files that could cause confusion for developers