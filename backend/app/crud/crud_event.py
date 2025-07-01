from sqlalchemy.orm import Session
from typing import List as ListTyping
from datetime import datetime

from app.crud.base import CRUDBase
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate

class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):
    def create_with_user(
        self, db: Session, *, obj_in: EventCreate, creator_id: int
    ) -> Event:
        """
        Create a new event with creator information.
        """
        obj_in_data = obj_in.model_dump()
        obj_in_data["creator_id"] = creator_id
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_calendar(
        self, db: Session, *, calendar_id: int, skip: int = 0, limit: int = 100
    ) -> ListTyping[Event]:
        """
        Retrieve events associated with a specific calendar.
        """
        return (
            db.query(self.model)
            .filter(Event.calendar_id == calendar_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_date_range(
        self, 
        db: Session, 
        *, 
        calendar_id: int,
        start_date: datetime,
        end_date: datetime,
        skip: int = 0,
        limit: int = 100
    ) -> ListTyping[Event]:
        """
        Get events within a specific date range for a calendar.
        """
        return (
            db.query(self.model)
            .filter(Event.calendar_id == calendar_id)
            .filter(Event.start_time >= start_date)
            .filter(Event.start_time <= end_date)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_upcoming_events(
        self, 
        db: Session, 
        *, 
        calendar_id: int,
        from_time: datetime = None,
        skip: int = 0,
        limit: int = 100
    ) -> ListTyping[Event]:
        """
        Get upcoming events for a calendar.
        """
        if from_time is None:
            from_time = datetime.utcnow()
        
        return (
            db.query(self.model)
            .filter(Event.calendar_id == calendar_id)
            .filter(Event.start_time >= from_time)
            .order_by(Event.start_time)
            .offset(skip)
            .limit(limit)
            .all()
        )

# Create an instance of the CRUDEvent class for use in the API.
event = CRUDEvent(Event)