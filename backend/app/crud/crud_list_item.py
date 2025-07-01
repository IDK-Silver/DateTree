from sqlalchemy.orm import Session
from typing import List as ListTyping, Optional
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.list_item import ListItem
from app.models.vote import Vote
from app.schemas.list_item import ListItemCreate, ListItemUpdate

class CRUDListItem(CRUDBase[ListItem, ListItemCreate, ListItemUpdate]):
    def create_with_user(
        self, db: Session, *, obj_in: ListItemCreate, creator_id: int
    ) -> ListItem:
        """
        Create a new list item with creator information.
        """
        obj_in_data = obj_in.model_dump()
        obj_in_data["creator_id"] = creator_id
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_list(
        self, db: Session, *, list_id: int, skip: int = 0, limit: int = 100
    ) -> ListTyping[ListItem]:
        """
        Retrieve list items associated with a specific list.
        """
        return (
            db.query(self.model)
            .filter(ListItem.list_id == list_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_with_vote_count(
        self, db: Session, *, list_item_id: int
    ) -> Optional[tuple]:
        """
        Get list item with vote count.
        """
        return (
            db.query(ListItem, func.count(Vote.id).label("vote_count"))
            .outerjoin(Vote, ListItem.id == Vote.list_item_id)
            .filter(ListItem.id == list_item_id)
            .group_by(ListItem.id)
            .first()
        )

    def get_multi_with_vote_counts(
        self, db: Session, *, list_id: int, skip: int = 0, limit: int = 100
    ) -> ListTyping[tuple]:
        """
        Get list items with their vote counts for a specific list.
        """
        return (
            db.query(ListItem, func.count(Vote.id).label("vote_count"))
            .outerjoin(Vote, ListItem.id == Vote.list_item_id)
            .filter(ListItem.list_id == list_id)
            .group_by(ListItem.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

# Create an instance of the CRUDListItem class for use in the API.
list_item = CRUDListItem(ListItem)