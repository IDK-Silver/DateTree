from typing import Generator
from sqlalchemy.orm import Session
from app.core.database import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# For now, we'll create a simple current user dependency
# In a real application, this would check JWT tokens or sessions
def get_current_active_user():
    """
    Simple current user dependency.
    In a real application, this would validate JWT tokens and return the actual user.
    For now, we'll return a mock user dict.
    """
    # This is a placeholder - replace with actual authentication logic
    return {"id": 1, "username": "admin", "is_active": True}
