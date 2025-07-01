from sqlalchemy.orm import Session
from typing import List as ListTyping, Optional

from app.crud.base import CRUDBase
from app.models.vote import Vote
from app.schemas.vote import VoteCreate

class CRUDVote(CRUDBase[Vote, VoteCreate, VoteCreate]):
    def create_with_user(
        self, db: Session, *, obj_in: VoteCreate, user_id: int
    ) -> Vote:
        """
        Create a new vote with user information.
        """
        obj_in_data = obj_in.model_dump()
        obj_in_data["user_id"] = user_id
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_user_and_item(
        self, db: Session, *, user_id: int, list_item_id: int
    ) -> Optional[Vote]:
        """
        Get vote by user and list item.
        """
        return (
            db.query(self.model)
            .filter(Vote.user_id == user_id)
            .filter(Vote.list_item_id == list_item_id)
            .first()
        )

    def get_multi_by_item(
        self, db: Session, *, list_item_id: int, skip: int = 0, limit: int = 100
    ) -> ListTyping[Vote]:
        """
        Get all votes for a specific list item.
        """
        return (
            db.query(self.model)
            .filter(Vote.list_item_id == list_item_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> ListTyping[Vote]:
        """
        Get all votes by a specific user.
        """
        return (
            db.query(self.model)
            .filter(Vote.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def remove_by_user_and_item(
        self, db: Session, *, user_id: int, list_item_id: int
    ) -> Optional[Vote]:
        """
        Remove vote by user and list item.
        """
        vote = self.get_by_user_and_item(db, user_id=user_id, list_item_id=list_item_id)
        if vote:
            db.delete(vote)
            db.commit()
        return vote

# Create an instance of the CRUDVote class for use in the API.
vote = CRUDVote(Vote)