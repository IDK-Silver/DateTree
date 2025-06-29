from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
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
    calendar_id = Column(Integer, ForeignKey("calendars.id"), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"))

    calendar = relationship("Calendar", back_populates="events")