from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class ListItem(Base):
    """
    Represents a single item within a list.
    """
    __tablename__ = "list_items"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    is_completed = Column(Boolean, default=False)
    list_id = Column(Integer, ForeignKey("lists.id"), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    list_obj = relationship("List", back_populates="items")
    votes = relationship("Vote", back_populates="list_item", cascade="all, delete-orphan")
