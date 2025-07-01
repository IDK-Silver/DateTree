from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- Base Properties ---
# Shared properties that are common to all schemas.
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    calendar_id: int

# --- Create Schema ---
# Properties to receive via API on creation.
class EventCreate(EventBase):
    pass  # No extra fields needed for creation

# --- Update Schema ---
# Properties to receive via API on update. All fields are optional.
class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

# --- Read Schema ---
# Properties to return to the client.
class Event(EventBase):
    id: int
    creator_id: Optional[int] = None

    class Config:
        from_attributes = True