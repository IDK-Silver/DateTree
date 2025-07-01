from typing import Any, List as ListTyping
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.crud import list_item as list_item_crud
from app.schemas import list_item as list_item_schemas
from app.api import deps

router = APIRouter()

@router.get("/list/{list_id}", response_model=ListTyping[list_item_schemas.ListItem])
def read_list_items(
    list_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Retrieve list items for a specific list.
    TODO: Add permission check to ensure user has access to the list.
    """
    items = list_item_crud.get_multi_by_list(
        db, list_id=list_id, skip=skip, limit=limit
    )
    return items

@router.get("/list/{list_id}/with-votes", response_model=ListTyping[dict])
def read_list_items_with_votes(
    list_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Retrieve list items with vote counts for a specific list.
    """
    items_with_votes = list_item_crud.get_multi_with_vote_counts(
        db, list_id=list_id, skip=skip, limit=limit
    )
    
    # Convert to dict format with vote counts
    result = []
    for item, vote_count in items_with_votes:
        item_dict = {
            "id": item.id,
            "content": item.content,
            "is_completed": item.is_completed,
            "list_id": item.list_id,
            "creator_id": item.creator_id,
            "created_at": item.created_at,
            "vote_count": vote_count or 0
        }
        result.append(item_dict)
    
    return result

@router.get("/{item_id}", response_model=list_item_schemas.ListItem)
def read_list_item(
    item_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get a specific list item by ID.
    """
    item = list_item_crud.get(db=db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="List item not found")
    # TODO: Add permission check
    return item

@router.post("/", response_model=list_item_schemas.ListItem)
def create_list_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: list_item_schemas.ListItemCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Create a new list item.
    """
    # TODO: Add permission check to ensure user has access to the list
    item = list_item_crud.create_with_user(
        db=db, obj_in=item_in, creator_id=current_user.id
    )
    return item

@router.put("/{item_id}", response_model=list_item_schemas.ListItem)
def update_list_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    item_in: list_item_schemas.ListItemUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Update a list item.
    """
    item = list_item_crud.get(db=db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="List item not found")
    # TODO: Add permission check
    item = list_item_crud.update(db=db, db_obj=item, obj_in=item_in)
    return item

@router.delete("/{item_id}", response_model=list_item_schemas.ListItem)
def delete_list_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Delete a list item.
    """
    item = list_item_crud.get(db=db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="List item not found")
    # TODO: Add permission check
    item = list_item_crud.remove(db=db, id=item_id)
    return item