from pydantic import BaseModel

# --- Base Properties ---
# Shared properties that are common to all schemas.
class VoteBase(BaseModel):
    list_item_id: int

# --- Create Schema ---
# Properties to receive via API on creation.
class VoteCreate(VoteBase):
    pass  # user_id will be set from authentication

# --- Read Schema ---
# Properties to return to the client.
class Vote(VoteBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True