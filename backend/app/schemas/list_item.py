from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- Base Properties ---
# Shared properties that are common to all schemas.
class ListItemBase(BaseModel):
    content: str
    is_completed: bool = False
    list_id: int

# --- Create Schema ---
# Properties to receive via API on creation.
class ListItemCreate(ListItemBase):
    pass  # No extra fields needed for creation

# --- Update Schema ---
# Properties to receive via API on update. All fields are optional.
class ListItemUpdate(BaseModel):
    content: Optional[str] = None
    is_completed: Optional[bool] = None

# --- Read Schema ---
# Properties to return to the client.
class ListItem(ListItemBase):
    id: int
    creator_id: Optional[int] = None
    created_at: datetime
    vote_count: Optional[int] = 0  # Computed field for vote count

    class Config:
        from_attributes = True