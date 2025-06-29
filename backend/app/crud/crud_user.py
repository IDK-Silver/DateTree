# backend/app/crud/crud_user.py

from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        Get a user by their email address.

        :param db: The database session.
        :param email: The user's email.
        :return: The user object or None if not found.
        """
        return db.query(self.model).filter(self.model.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        Create a new user.

        :param db: The database session.
        :param obj_in: The user creation data.
        :return: The created user object.
        """
        db_obj = User(
            email=obj_in.email,
            username=obj_in.email,  # Use email as username for now
            hashed_password=get_password_hash(obj_in.password),
            is_active=True,  # Default to active
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """
        Update a user's data.

        :param db: The database session.
        :param db_obj: The existing user object from the database.
        :param obj_in: The new data to update.
        :return: The updated user object.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
            
        return super().update(db, db_obj=db_obj, obj_in=update_data)


user = CRUDUser(User)