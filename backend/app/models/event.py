from sqlalchemy import (Column, DateTime, Enum, ForeignKey, Integer, String,
                        Text)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.basic import Base
from .enums import EventStatus

class Event(Base):
    """Event/Todo item model"""
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)  # For storing Markdown content
    status = Column(Enum(EventStatus), nullable=False, default=EventStatus.TODO)
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationship: each event must belong to a calendar (many-to-one)
    calendar_id = Column(Integer, ForeignKey("calendars.id"), nullable=False)
    calendar = relationship("Calendar", back_populates="events")

    def __repr__(self):
        return f"<Event(id={self.id}, title='{self.title}')>"