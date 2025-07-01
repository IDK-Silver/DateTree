from typing import Any, List as ListTyping
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.crud import vote as vote_crud
from app.schemas import vote as vote_schemas
from app.api import deps

router = APIRouter()

@router.get("/item/{item_id}", response_model=ListTyping[vote_schemas.Vote])
def read_votes_for_item(
    item_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get all votes for a specific list item.
    """
    votes = vote_crud.get_multi_by_item(
        db, list_item_id=item_id, skip=skip, limit=limit
    )
    return votes

@router.get("/user/my-votes", response_model=ListTyping[vote_schemas.Vote])
def read_my_votes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get all votes by the current user.
    """
    votes = vote_crud.get_multi_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return votes

@router.post("/", response_model=vote_schemas.Vote)
def create_vote(
    *,
    db: Session = Depends(deps.get_db),
    vote_in: vote_schemas.VoteCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Cast a vote for a list item.
    Prevents duplicate votes by the same user on the same item.
    """
    # Check if user has already voted for this item
    existing_vote = vote_crud.get_by_user_and_item(
        db, user_id=current_user.id, list_item_id=vote_in.list_item_id
    )
    
    if existing_vote:
        raise HTTPException(
            status_code=400, 
            detail="User has already voted for this item"
        )
    
    # TODO: Add permission check to ensure user has access to the list
    vote = vote_crud.create_with_user(
        db=db, obj_in=vote_in, user_id=current_user.id
    )
    return vote

@router.delete("/item/{item_id}")
def remove_vote(
    item_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Remove the current user's vote from a list item.
    """
    vote = vote_crud.remove_by_user_and_item(
        db, user_id=current_user.id, list_item_id=item_id
    )
    
    if not vote:
        raise HTTPException(
            status_code=404,
            detail="Vote not found"
        )
    
    return {"message": "Vote removed successfully"}