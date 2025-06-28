from sqlalchemy import (Column, DateTime, Enum, ForeignKey, Integer, String,
                        Table, Text)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.basic import Base
from .enums import PermissionLevel

# Define many-to-many association table between Calendar and User
calendar_member_association = Table(
    "calendar_member_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("calendar_id", Integer, ForeignKey("calendars.id"), primary_key=True),
    Column(
        "permission",
        Enum(PermissionLevel),
        nullable=False,
        default=PermissionLevel.EDITOR,
    ),
)

class Calendar(Base):
    """Calendar model"""
    __tablename__ = "calendars"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship: each calendar must have an owner (many-to-one)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="owned_calendars")

    # Relationship: each calendar can have multiple events (one-to-many)
    events = relationship("Event", back_populates="calendar", cascade="all, delete-orphan")

    # Relationship: each calendar can have multiple members (many-to-many)
    members = relationship(
        "User", secondary=calendar_member_association, back_populates="calendars"
    )

    def __repr__(self):
        return f"<Calendar(id={self.id}, name='{self.name}')>"