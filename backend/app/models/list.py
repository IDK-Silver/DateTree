import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

# Defines the possible types for a List.
class ListType(enum.Enum):
    TODO = "TODO"
    PRIORITY = "PRIORITY"

class List(Base):
    """
    Represents a list within a calendar (e.g., a to-do list, a priority list).
    """
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    list_type = Column(Enum(ListType), nullable=False, name="list_type_enum")
    calendar_id = Column(Integer, ForeignKey("calendars.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    calendar = relationship("Calendar", back_populates="lists")
    items = relationship("ListItem", back_populates="list_obj", cascade="all, delete-orphan")
