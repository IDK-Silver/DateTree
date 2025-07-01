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
    ## 🗳️ 取得帶投票數的清單項目

    取得指定清單的所有項目，並包含每個項目的投票統計。特別適用於 PRIORITY 類型清單的決策分析。

    ### 🔧 功能說明
    - 返回清單中的所有項目
    - 包含每個項目的投票總數
    - 依照投票數排序（高到低）
    - 支援分頁查詢

    ### 📊 查詢參數
    - `list_id`: 清單 ID（路徑參數）
    - `skip`: 跳過筆數（分頁用）
    - `limit`: 返回筆數上限

    ### ✅ 成功回應
    ```json
    [
        {
            "id": 5,
            "content": "九份老街探索",
            "is_completed": false,
            "list_id": 2,
            "creator_id": 3,
            "created_at": "2025-07-01T10:30:00Z",
            "vote_count": 8
        },
        {
            "id": 6,
            "content": "陽明山健行",
            "is_completed": false,
            "list_id": 2,
            "creator_id": 2,
            "created_at": "2025-07-01T10:45:00Z",
            "vote_count": 5
        }
    ]
    ```

    ### 💡 使用場景
    - 檢視投票結果和排名
    - 分析團隊偏好
    - 決策制定參考
    - 投票進度追蹤

    ### 🎯 特別適用
    此端點特別適合 PRIORITY 類型清單，可以清楚看到團隊投票的結果分佈。
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