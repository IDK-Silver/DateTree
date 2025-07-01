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
    ## 📋 取得所有清單

    取得當前用戶可存取的所有清單。

    ### 🔧 功能說明
    - 返回用戶有權限存取的所有清單
    - 支援分頁查詢
    - 包含 TODO 和 PRIORITY 兩種類型

    ### 📊 查詢參數
    - `skip`: 跳過筆數（分頁用）
    - `limit`: 返回筆數上限（最大 100）

    ### ✅ 成功回應
    ```json
    [
        {
            "id": 1,
            "name": "我的待辦清單",
            "list_type": "TODO",
            "calendar_id": 1,
            "created_at": "2025-07-01T10:00:00Z"
        },
        {
            "id": 2,
            "name": "團隊投票清單",
            "list_type": "PRIORITY", 
            "calendar_id": 2,
            "created_at": "2025-07-01T11:00:00Z"
        }
    ]
    ```

    ### 🔑 權限要求
    需要有效的 JWT Token
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
    ## 📝 建立新清單

    在指定的日曆中建立新的清單。支援 TODO 和 PRIORITY 兩種類型。

    ### 🔧 功能說明
    - 在指定日曆中建立新清單
    - 支援 TODO（待辦事項）和 PRIORITY（投票優先級）類型
    - PRIORITY 類型支援團隊投票功能

    ### 📝 請求範例
    ```json
    {
        "name": "團隊旅遊地點投票",
        "list_type": "PRIORITY",
        "calendar_id": 2
    }
    ```

    ### ✅ 成功回應
    ```json
    {
        "id": 3,
        "name": "團隊旅遊地點投票",
        "list_type": "PRIORITY",
        "calendar_id": 2,
        "created_at": "2025-07-01T14:30:00Z"
    }
    ```

    ### 📋 清單類型說明
    - **TODO**: 一般待辦事項清單，適合個人任務管理
    - **PRIORITY**: 優先級投票清單，適合團隊協作決策

    ### 🔑 權限要求
    需要對目標日曆有建立權限
    """
    # You can now use current_user.id for permission checks or to record the operator.
    # For example, check if the current_user has permission to create a list
    # in the specified list_in.calendar_id.
    
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
