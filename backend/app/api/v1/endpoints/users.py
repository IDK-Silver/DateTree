# backend/app/api/v1/endpoints/users.py

from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.post("/register", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    ## 👤 用戶註冊

    建立新的用戶帳號。註冊成功後，系統會自動為用戶建立一個個人日曆。

    ### 🔧 功能說明
    - 檢查 Email 是否已存在
    - 創建用戶帳號（密碼會自動加密）
    - 自動建立個人日曆（PERSONAL 類型）
    - 返回用戶基本資訊

    ### 📝 請求範例
    ```json
    {
        "email": "user@example.com",
        "password": "securepassword123"
    }
    ```

    ### ✅ 成功回應
    ```json
    {
        "id": 1,
        "email": "user@example.com",
        "is_active": true
    }
    ```

    ### ⚠️ 注意事項
    - Email 必須是有效格式
    - 密碼至少 8 個字符
    - Email 不能重複註冊
    - 註冊後需要使用 `/auth/login` 取得認證令牌
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user