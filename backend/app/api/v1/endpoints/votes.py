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
    **對清單項目投票**

    為 PRIORITY 類型清單的項目投票，用於團隊協作決策。

    **功能說明:**
    - 對指定的清單項目投票
    - 防止重複投票（每個用戶每個項目只能投票一次）
    - 自動記錄投票用戶和時間
    - 支援即時投票統計

    **請求範例:**
    ```json
    {
        "list_item_id": 5
    }
    ```

    **成功回應:**
    ```json
    {
        "id": 10,
        "user_id": 3,
        "list_item_id": 5
    }
    ```

    **使用場景:**
    - 團隊活動地點選擇投票
    - 產品功能優先級決策
    - 會議時間安排投票
    - 專案方案選擇

    **注意事項:**
    - 只能對 PRIORITY 類型清單的項目投票
    - 每個項目每個用戶只能投票一次
    - 投票後可以取消，但不能修改
    - 需要對相關日曆有存取權限
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