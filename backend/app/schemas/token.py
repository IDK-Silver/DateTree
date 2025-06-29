# backend/app/schemas/token.py

from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """
    Schema for the access token response.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for the data stored within the JWT token.
    """
    email: Optional[str] = None