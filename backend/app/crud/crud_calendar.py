# backend/app/crud/crud_calendar.py
from sqlalchemy.orm import Session, joinedload, selectinload
from typing import List as ListTyping

from app.crud.base import CRUDBase
from app.models.calendar import Calendar, CalendarType
from app.schemas.calendar import CalendarCreate, CalendarUpdate

class CRUDCalendar(CRUDBase[Calendar, CalendarCreate, CalendarUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: CalendarCreate, owner_id: int, calendar_type: CalendarType = CalendarType.GENERAL
    ) -> Calendar:
        """
        Create a new calendar with an owner.
        """
        db_obj = self.model(
            **obj_in.model_dump(), 
            owner_id=owner_id, 
            calendar_type=calendar_type
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> ListTyping[Calendar]:
        """
        Retrieve calendars for a specific owner.
        """
        return (
            db.query(self.model)
            .filter(Calendar.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_with_lists_and_events(
        self, db: Session, *, calendar_id: int
    ) -> Calendar:
        """
        Get calendar with all lists and events eagerly loaded.
        Reduces N+1 queries when displaying calendar overview.
        """
        return (
            db.query(Calendar)
            .options(
                selectinload(Calendar.lists),
                selectinload(Calendar.events)
            )
            .filter(Calendar.id == calendar_id)
            .first()
        )
    
    def get_with_full_data(
        self, db: Session, *, calendar_id: int
    ) -> Calendar:
        """
        Get calendar with all related data eagerly loaded.
        Includes lists with items and votes, events, and members.
        """
        return (
            db.query(Calendar)
            .options(
                selectinload(Calendar.lists).selectinload("items").selectinload("votes"),
                selectinload(Calendar.events),
                selectinload(Calendar.members)
            )
            .filter(Calendar.id == calendar_id)
            .first()
        )

calendar_crud = CRUDCalendar(Calendar)
