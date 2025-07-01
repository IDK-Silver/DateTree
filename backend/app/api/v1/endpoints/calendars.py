# backend/app/api/v1/endpoints/calendars.py
from typing import Any, List as ListTyping
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.crud.crud_calendar import calendar_crud
from app.schemas import calendar as calendar_schemas
from app.api import deps

from app.models.calendar import CalendarType

router = APIRouter()

@router.get("/", response_model=ListTyping[calendar_schemas.Calendar])
def read_calendars(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Retrieve calendars owned by the current user.
    """
    calendars = calendar_crud.get_multi_by_owner(
        db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return calendars

@router.get("/{calendar_id}", response_model=calendar_schemas.Calendar)
def read_calendar(
    calendar_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get a specific calendar by ID.
    """
    calendar = calendar_crud.get(db=db, id=calendar_id)
    if not calendar:
        raise HTTPException(status_code=404, detail="Calendar not found")
    if calendar.owner_id != current_user.id:
        # You might want to check for membership as well in a real app
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return calendar

@router.post("/", response_model=calendar_schemas.Calendar)
def create_calendar(
    *,
    db: Session = Depends(deps.get_db),
    calendar_in: calendar_schemas.CalendarCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Create a new calendar.
    """
    calendar = calendar_crud.create_with_owner(
        db=db, obj_in=calendar_in, owner_id=current_user.id
    )
    return calendar

@router.put("/{calendar_id}", response_model=calendar_schemas.Calendar)
def update_calendar(
    *,
    db: Session = Depends(deps.get_db),
    calendar_id: int,
    calendar_in: calendar_schemas.CalendarUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Update a calendar.
    """
    calendar = calendar_crud.get(db=db, id=calendar_id)
    if not calendar:
        raise HTTPException(status_code=404, detail="Calendar not found")
    if calendar.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    calendar = calendar_crud.update(db=db, db_obj=calendar, obj_in=calendar_in)
    return calendar

@router.delete("/{calendar_id}", response_model=calendar_schemas.Calendar)
def delete_calendar(
    *,
    db: Session = Depends(deps.get_db),
    calendar_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Delete a calendar.
    """
    calendar = calendar_crud.get(db=db, id=calendar_id)
    if not calendar:
        raise HTTPException(status_code=404, detail="Calendar not found")
    if calendar.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if calendar.calendar_type == CalendarType.PERSONAL:
        raise HTTPException(
            status_code=403,
            detail="Personal calendars cannot be deleted."
        )
    calendar = calendar_crud.remove(db=db, id=calendar_id)
    return calendar
