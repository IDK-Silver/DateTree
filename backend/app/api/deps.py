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


def check_calendar_access(
    db: Session, calendar_id: int, user: models.User
) -> models.Calendar:
    """
    Check if user has access to the calendar.
    Returns the calendar if user has access, raises HTTPException otherwise.
    Uses optimized JOIN query instead of N+1 queries.
    """
    from sqlalchemy import or_
    from app.models.calendar import calendar_user_association
    
    # Single query to check calendar existence and user access
    calendar = (
        db.query(models.Calendar)
        .outerjoin(
            calendar_user_association, 
            models.Calendar.id == calendar_user_association.c.calendar_id
        )
        .filter(
            models.Calendar.id == calendar_id,
            or_(
                models.Calendar.owner_id == user.id,  # User is owner
                calendar_user_association.c.user_id == user.id  # User is member
            )
        )
        .first()
    )
    
    if not calendar:
        # Check if calendar exists at all to provide better error message
        calendar_exists = db.query(models.Calendar).filter(
            models.Calendar.id == calendar_id
        ).first()
        
        if not calendar_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Calendar not found"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access this calendar"
            )
    
    return calendar


def check_list_access(
    db: Session, list_id: int, user: models.User
) -> models.List:
    """
    Check if user has access to the list through calendar access.
    Returns the list if user has access, raises HTTPException otherwise.
    Uses optimized JOIN query to check both list and calendar access in one query.
    """
    from sqlalchemy import or_
    from app.models.calendar import calendar_user_association
    
    # Single query to check list existence and user access through calendar
    list_obj = (
        db.query(models.List)
        .join(models.Calendar, models.List.calendar_id == models.Calendar.id)
        .outerjoin(
            calendar_user_association,
            models.Calendar.id == calendar_user_association.c.calendar_id
        )
        .filter(
            models.List.id == list_id,
            or_(
                models.Calendar.owner_id == user.id,  # User owns calendar
                calendar_user_association.c.user_id == user.id  # User is member
            )
        )
        .first()
    )
    
    if not list_obj:
        # Check if list exists at all to provide better error message
        list_exists = db.query(models.List).filter(
            models.List.id == list_id
        ).first()
        
        if not list_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="List not found"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access this list"
            )
    
    return list_obj