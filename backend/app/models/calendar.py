import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    Table,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

# Defines the type of a calendar
class CalendarType(enum.Enum):
    PERSONAL = "PERSONAL"  # Auto-created, non-deletable personal calendar
    GENERAL = "GENERAL"    # User-created, general-purpose calendar

# This table manages the many-to-many relationship between Users and Calendars.
calendar_user_association = Table(
    "calendar_user_association",
    Base.metadata,
    Column("calendar_id", Integer, ForeignKey("calendars.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
)

class Calendar(Base):
    """
    Represents a calendar, a container for lists and events.
    """
    __tablename__ = "calendars"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    calendar_type = Column(Enum(CalendarType), nullable=False, default=CalendarType.GENERAL)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User")
    members = relationship(
        "User", secondary=calendar_user_association, back_populates="calendars"
    )
    lists = relationship("List", back_populates="calendar", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="calendar", cascade="all, delete-orphan")