from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from .base import Base

class Event(Base):
    """
    Represents a scheduled event on the calendar with a specific date and time.
    """
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    calendar_id = Column(Integer, ForeignKey("calendars.id"), nullable=False, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"), index=True)

    calendar = relationship("Calendar", back_populates="events")
    
    __table_args__ = (
        # Index for calendar events ordered by time
        Index('idx_event_calendar_time', 'calendar_id', 'start_time'),
        # Index for time-based queries (upcoming events, date ranges)
        Index('idx_event_start_time', 'start_time'),
        # Index for creator's events
        Index('idx_event_creator', 'creator_id'),
    )