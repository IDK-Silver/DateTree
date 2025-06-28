from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.basic import Base


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship: a user can own multiple calendars
    owned_calendars = relationship("Calendar", back_populates="owner")

    # Relationship: a user can be a member of multiple calendars (many-to-many)
    # Through the intermediate table `calendar_members` defined in calendar.py
    calendars = relationship(
        "Calendar", secondary="calendar_members", back_populates="members"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"