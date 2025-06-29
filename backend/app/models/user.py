from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class User(Base):
    """
    Represents a user in the system.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships are defined using strings to avoid circular imports.
    # The actual relationship object is resolved by SQLAlchemy at runtime.
    calendars = relationship(
        "Calendar", secondary="calendar_user_association", back_populates="members"
    )
    votes = relationship("Vote", back_populates="user")