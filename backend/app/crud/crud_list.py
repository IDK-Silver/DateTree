from sqlalchemy.orm import Session
from typing import List as ListTyping

from app.crud.base import CRUDBase
from app.models.list import List
from app.schemas.list import ListCreate, ListUpdate

class CRUDList(CRUDBase[List, ListCreate, ListUpdate]):
    def get_multi_by_calendar(
        self, db: Session, *, calendar_id: int, skip: int = 0, limit: int = 100
    ) -> ListTyping[List]:
        """
        Retrieve lists associated with a specific calendar.
        """
        return (
            db.query(self.model)
            .filter(List.calendar_id == calendar_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_calendar_and_type(
        self, db: Session, *, calendar_id: int, list_type: str
    ) -> ListTyping[List]:
        """
        Retrieve lists by calendar and type.
        """
        return (
            db.query(self.model)
            .filter(List.calendar_id == calendar_id)
            .filter(List.list_type == list_type)
            .all()
        )

# Create an instance of the CRUDList class for use in the API.
list_crud = CRUDList(List)
