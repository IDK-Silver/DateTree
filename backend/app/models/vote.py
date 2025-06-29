from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Vote(Base):
    """
    Represents a single vote cast by a user for a list item.
    """
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    list_item_id = Column(Integer, ForeignKey("list_items.id"), nullable=False)

    user = relationship("User", back_populates="votes")
    list_item = relationship("ListItem", back_populates="votes")
