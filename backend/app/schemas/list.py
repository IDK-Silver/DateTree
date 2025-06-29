from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.list import ListType

# --- Base Properties ---
# Shared properties that are common to all schemas.
class ListBase(BaseModel):
    name: str
    list_type: ListType = ListType.TODO
    calendar_id: int

# --- Create Schema ---
# Properties to receive via API on creation.
# Inherits all properties from ListBase.
class ListCreate(ListBase):
    pass  # No extra fields needed for creation

# --- Update Schema ---
# Properties to receive via API on update. All fields are optional.
class ListUpdate(BaseModel):
    name: Optional[str] = None
    list_type: Optional[ListType] = None

# --- Read Schema ---
# Properties to return to the client.
# This schema includes properties that are stored in the database.
class List(ListBase):
    id: int
    created_at: datetime

    # This configuration class tells Pydantic to read data even if it's not a dict,
    # but an ORM model (or any other arbitrary object with attributes).
    class Config:
        from_attributes = True
