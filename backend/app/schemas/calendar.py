# backend/app/schemas/calendar.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .user import User
from app.models.calendar import CalendarType

# --- Base Properties ---
class CalendarBase(BaseModel):
    name: str
    description: Optional[str] = None

# --- Create Schema ---
class CalendarCreate(CalendarBase):
    pass

# --- Update Schema ---
class CalendarUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# --- Read Schema ---
class Calendar(CalendarBase):
    id: int
    owner_id: int
    calendar_type: CalendarType
    created_at: datetime
    owner: User
    members: List[User] = []

    class Config:
        from_attributes = True
