from typing import Any, List as ListTyping
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.crud.crud_list import list_crud
from app.schemas import list as list_schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=ListTyping[list_schemas.List])
def read_lists(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Retrieve all lists.
    NOTE: This is a simplified example. A real implementation might need
    to filter by user's accessible calendars.
    """
    lists = list_crud.get_multi(db, skip=skip, limit=limit)
    return lists

@router.get("/calendar/{calendar_id}", response_model=ListTyping[list_schemas.List])
def read_lists_by_calendar(
    calendar_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Retrieve lists for a specific calendar.
    Add permission check here in the future.
    """
    lists = list_crud.get_multi_by_calendar(
        db, calendar_id=calendar_id, skip=skip, limit=limit
    )
    return lists

@router.get("/{list_id}", response_model=list_schemas.List)
def read_list(
    list_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get a specific list by ID.
    """
    list_obj = list_crud.get(db=db, id=list_id)
    if not list_obj:
        raise HTTPException(status_code=404, detail="List not found")
    # Add permission check here in the future
    return list_obj

@router.post("/", response_model=list_schemas.List)
def create_list(
    *,
    db: Session = Depends(deps.get_db),
    list_in: list_schemas.ListCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Create a new list.
    This endpoint is now protected and requires a valid token.
    The `current_user` object is now available for use.
    """
    # 接下來，您可以在這裡使用 current_user.id 來進行權限檢查或記錄操作者
    # 例如：檢查 current_user 是否有權限在 list_in.calendar_id 中建立清單
    print(f"User {current_user.email} is creating a list.")
    
    list_obj = list_crud.create(db=db, obj_in=list_in)
    return list_obj

@router.put("/{list_id}", response_model=list_schemas.List)
def update_list(
    *,
    db: Session = Depends(deps.get_db),
    list_id: int,
    list_in: list_schemas.ListUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Update a list.
    """
    list_obj = list_crud.get(db=db, id=list_id)
    if not list_obj:
        raise HTTPException(status_code=404, detail="List not found")
    # Add permission check here: if list_obj.calendar.owner_id != current_user.id: ...
    list_obj = list_crud.update(db=db, db_obj=list_obj, obj_in=list_in)
    return list_obj

@router.delete("/{list_id}", response_model=list_schemas.List)
def delete_list(
    *,
    db: Session = Depends(deps.get_db),
    list_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Delete a list.
    """
    list_obj = list_crud.get(db=db, id=list_id)
    if not list_obj:
        raise HTTPException(status_code=404, detail="List not found")
    # Add permission check here
    list_obj = list_crud.remove(db=db, id=list_id)
    return list_obj
