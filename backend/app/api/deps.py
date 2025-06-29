# backend/app/api/deps.py

from typing import Generator, Optional
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.core.database import SessionLocal

# This defines the URL that clients will use to get the token.
# We've already created this endpoint in `login.py`.
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/login/access-token"
)

def get_db() -> Generator:
    """
    Dependency to get a database session.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    """
    Dependency to get the current user from a JWT token.

    This function is now the gatekeeper for authenticated endpoints.
    1. It takes the token from the request's Authorization header.
    2. It decodes the JWT to get the subject (user's email).
    3. It fetches the user from the database.
    4. It handles all potential errors (invalid token, user not found).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = crud.user.get_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    Dependency that builds on get_current_user.
    It ensures the user is not only authenticated but also active.
    This is the dependency you'll most commonly use to protect routes.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user