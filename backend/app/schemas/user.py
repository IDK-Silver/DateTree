# backend/app/schemas/user.py

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    """
    Base schema for a User, containing common attributes.
    """
    email: EmailStr

class UserCreate(UserBase):
    """
    Schema for creating a new user. Inherits from UserBase.
    Requires a password.
    """
    password: str

class UserUpdate(UserBase):
    """
    Schema for updating a user. All fields are optional.
    """
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserInDBBase(UserBase):
    """
    Base schema for user data stored in the database.
    Includes the user ID and active status.
    """
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class User(UserInDBBase):
    """
    Schema for returning a user to the client.
    This can be used when reading a single user or a list of users.
    """
    pass

class UserInDB(UserInDBBase):
    """
    Schema for the full user data in the database, including the hashed password.
    This should NEVER be returned to the client.
    """
    hashed_password: str