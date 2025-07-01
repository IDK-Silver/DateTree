from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        try:
            obj_in_data = obj_in.model_dump()
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            db.rollback()
            if "unique constraint" in str(e).lower():
                raise HTTPException(status_code=409, detail="Resource already exists")
            elif "foreign key constraint" in str(e).lower():
                raise HTTPException(status_code=400, detail="Invalid reference to related resource")
            else:
                raise HTTPException(status_code=400, detail="Database constraint violation")
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error occurred")

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        try:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)
            
            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            db.rollback()
            if "unique constraint" in str(e).lower():
                raise HTTPException(status_code=409, detail="Resource already exists")
            elif "foreign key constraint" in str(e).lower():
                raise HTTPException(status_code=400, detail="Invalid reference to related resource")
            else:
                raise HTTPException(status_code=400, detail="Database constraint violation")
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error occurred")

    def remove(self, db: Session, *, id: int) -> ModelType:
        try:
            obj = db.query(self.model).get(id)
            if obj is None:
                raise HTTPException(status_code=404, detail="Resource not found")
            
            db.delete(obj)
            db.commit()
            return obj
        except IntegrityError as e:
            db.rollback()
            if "foreign key constraint" in str(e).lower():
                raise HTTPException(status_code=400, detail="Cannot delete: resource is referenced by other entities")
            else:
                raise HTTPException(status_code=400, detail="Database constraint violation")
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error occurred")
