# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DateTree is a collaborative task and event management API built with FastAPI and PostgreSQL. The project uses modern Python practices with type hints and comprehensive testing. Note: Currently using synchronous database operations (not async).

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

## Architecture Overview

### Directory Structure
```
backend/app/
├── api/v1/          # API endpoints (users, lists, calendars)
├── core/            # Config, database, security utilities
├── crud/            # Database operations layer
├── models/          # SQLAlchemy ORM models
└── schemas/         # Pydantic validation schemas
```

### Key Architectural Patterns

1. **Layered Architecture**: API → CRUD → Models with Schemas for validation
2. **Async Database Operations**: All database queries use async SQLAlchemy
3. **Dependency Injection**: FastAPI dependencies for database sessions and authentication
4. **Multi-tenant Calendars**: Users can own/share multiple calendars with different permissions

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
- ✅ User registration and authentication (JWT)
- ✅ Calendar management with permissions
- ✅ List CRUD operations
- ✅ ListItem, Vote, and Event APIs - Complete REST API system
- ✅ Comprehensive test suite (104+ tests) with full coverage
- ✅ Complete API documentation with relationship explanations and usage examples
- 📋 Frontend not yet implemented

## Important Notes
1. Always run tests before committing changes
2. Database migrations must be tested with upgrade/downgrade cycle
3. Use environment variables from `.env` (copy from `.env.example`)
4. Docker Compose provides PostgreSQL database for development
5. Package management uses `uv` (not pip or poetry)

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