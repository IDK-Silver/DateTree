from typing import Any, List as ListTyping, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import models
from app.crud import event as event_crud
from app.schemas import event as event_schemas
from app.api import deps

router = APIRouter()

@router.get("/calendar/{calendar_id}", response_model=ListTyping[event_schemas.Event])
def read_events_by_calendar(
    calendar_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Retrieve events for a specific calendar.
    """
    # Check if user has access to the calendar
    deps.check_calendar_access(db=db, calendar_id=calendar_id, user=current_user)
    
    events = event_crud.get_multi_by_calendar(
        db, calendar_id=calendar_id, skip=skip, limit=limit
    )
    return events

@router.get("/calendar/{calendar_id}/upcoming", response_model=ListTyping[event_schemas.Event])
def read_upcoming_events(
    calendar_id: int,
    db: Session = Depends(deps.get_db),
    from_time: Optional[datetime] = Query(None, description="Start time for upcoming events"),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get upcoming events for a calendar.
    """
    events = event_crud.get_upcoming_events(
        db, calendar_id=calendar_id, from_time=from_time, skip=skip, limit=limit
    )
    return events

@router.get("/calendar/{calendar_id}/date-range", response_model=ListTyping[event_schemas.Event])
def read_events_by_date_range(
    calendar_id: int,
    start_date: datetime = Query(..., description="Start date for event range"),
    end_date: datetime = Query(..., description="End date for event range"),
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get events within a specific date range for a calendar.
    """
    events = event_crud.get_multi_by_date_range(
        db, 
        calendar_id=calendar_id, 
        start_date=start_date, 
        end_date=end_date,
        skip=skip, 
        limit=limit
    )
    return events

@router.get("/{event_id}", response_model=event_schemas.Event)
def read_event(
    event_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get a specific event by ID.
    """
    event = event_crud.get(db=db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if user has access to the calendar
    deps.check_calendar_access(db=db, calendar_id=event.calendar_id, user=current_user)
    return event

@router.post("/", response_model=event_schemas.Event)
def create_event(
    *,
    db: Session = Depends(deps.get_db),
    event_in: event_schemas.EventCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Create a new event.
    """
    # Check if user has access to the calendar
    deps.check_calendar_access(db=db, calendar_id=event_in.calendar_id, user=current_user)
    
    event = event_crud.create_with_user(
        db=db, obj_in=event_in, creator_id=current_user.id
    )
    return event

@router.put("/{event_id}", response_model=event_schemas.Event)
def update_event(
    *,
    db: Session = Depends(deps.get_db),
    event_id: int,
    event_in: event_schemas.EventUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Update an event.
    """
    event = event_crud.get(db=db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if user has access to the calendar
    deps.check_calendar_access(db=db, calendar_id=event.calendar_id, user=current_user)
    
    event = event_crud.update(db=db, db_obj=event, obj_in=event_in)
    return event

@router.delete("/{event_id}", response_model=event_schemas.Event)
def delete_event(
    *,
    db: Session = Depends(deps.get_db),
    event_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Delete an event.
    """
    event = event_crud.get(db=db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if user has access to the calendar
    deps.check_calendar_access(db=db, calendar_id=event.calendar_id, user=current_user)
    
    event = event_crud.remove(db=db, id=event_id)
    return event