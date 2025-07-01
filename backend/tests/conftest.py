import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from typing import Generator
import os

from app.main import app
from app.models.base import Base
from app.api.deps import get_db
from app import crud, models
from app.core.security import create_access_token
from app.schemas.user import UserCreate
from app.schemas.calendar import CalendarCreate
from app.models.calendar import CalendarType

# Create test database URL (using SQLite for testing)
TEST_DATABASE_URL = "sqlite:///./blob/pytest/test.db"

# Create sync engine for testing
engine = create_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the dependency
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    """Set up and tear down the database for each test."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Clean up after test
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session() -> Generator:
    """Create a database session for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create a test client."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def test_user(db_session) -> models.User:
    """Create a test user with a personal calendar."""
    user_data = UserCreate(
        email="test@example.com",
        password="testpassword123"
    )
    user = crud.user.create(db_session, obj_in=user_data)
    
    # Create personal calendar for user (mimicking registration)
    calendar_data = CalendarCreate(
        name=f"{user.email}'s Calendar",
        description="Personal calendar"
    )
    personal_calendar = crud.calendar.create_with_owner(
        db_session, 
        obj_in=calendar_data, 
        owner_id=user.id,
        calendar_type=CalendarType.PERSONAL
    )
    
    return user

@pytest.fixture
def test_calendar(db_session, test_user: models.User) -> models.Calendar:
    """Create a test calendar for the test user."""
    calendar_data = CalendarCreate(
        name="Test Calendar",
        description="Calendar for testing"
    )
    calendar = crud.calendar.create_with_owner(
        db_session, 
        obj_in=calendar_data, 
        owner_id=test_user.id,
        calendar_type=CalendarType.GENERAL
    )
    return calendar

@pytest.fixture
def test_list(db_session, test_calendar: models.Calendar) -> models.List:
    """Create a test list in the test calendar."""
    from app.schemas.list import ListCreate
    from app.models.list import ListType
    
    list_data = ListCreate(
        name="Test List",
        list_type=ListType.TODO,
        calendar_id=test_calendar.id
    )
    test_list = crud.list_crud.create(db_session, obj_in=list_data)
    return test_list

@pytest.fixture
def test_token(test_user: models.User) -> str:
    """Create a test token for authentication."""
    return create_access_token(subject=test_user.email)

@pytest.fixture
def auth_headers(test_token: str) -> dict:
    """Create authentication headers."""
    return {"Authorization": f"Bearer {test_token}"}

@pytest.fixture
def authenticated_client(client: TestClient, auth_headers: dict) -> TestClient:
    """Create an authenticated test client."""
    client.headers.update(auth_headers)
    return client