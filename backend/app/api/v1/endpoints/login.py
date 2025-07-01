# backend/app/api/v1/endpoints/login.py

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.rate_limiter import auth_rate_limit

router = APIRouter()

@router.post("/access-token", response_model=schemas.Token)
def login_access_token(
    request: Request,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    _: None = Depends(auth_rate_limit)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = crud.user.get_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.email, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }