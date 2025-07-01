from sqlalchemy import Column, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from .base import Base

class Vote(Base):
    """
    Represents a single vote cast by a user for a list item.
    """
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    list_item_id = Column(Integer, ForeignKey("list_items.id"), nullable=False, index=True)

    user = relationship("User", back_populates="votes")
    list_item = relationship("ListItem", back_populates="votes")
    
    __table_args__ = (
        # Unique constraint to prevent duplicate votes
        Index('idx_vote_user_item_unique', 'user_id', 'list_item_id', unique=True),
        # Index for efficient vote counting by list item
        Index('idx_vote_list_item', 'list_item_id'),
        # Index for user's vote history
        Index('idx_vote_user', 'user_id'),
    )
