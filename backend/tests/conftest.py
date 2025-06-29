import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.models.base import Base
from app.api.deps import get_db
from app import crud, models
from app.core.security import create_access_token

# Create test database URL (using SQLite for testing)
SQLALCHEMY_DATABASE_URL = "sqlite:///./blob/pytest/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Needed for SQLite
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the dependency
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)

@pytest.fixture
def db_session():
    """Create a database session for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def cleanup_db():
    """Clean up the database after each test."""
    yield
    # Clean up: drop all tables and recreate them
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    from app.schemas.user import UserCreate
    user_data = UserCreate(
        email="test@example.com",
        password="testpassword123"
    )
    user = crud.user.create(db_session, obj_in=user_data)
    return user

@pytest.fixture
def test_token(test_user):
    """Create a test token for authentication."""
    return create_access_token(subject=test_user.email)

@pytest.fixture
def auth_headers(test_token):
    """Create authentication headers."""
    return {"Authorization": f"Bearer {test_token}"}

@pytest.fixture
def authenticated_client(client, auth_headers):
    """Create an authenticated test client."""
    client.headers.update(auth_headers)
    return client
