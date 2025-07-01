from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    ## 🌳 DateTree - 協作任務與事件管理 API

    DateTree 是一個現代化的協作任務和事件管理系統，支援團隊投票決策和個人任務追蹤。

    ### 🚀 主要功能

    * **👤 用戶管理**: 用戶註冊、登入、JWT 認證
    * **📅 日曆系統**: 個人和共享日曆管理
    * **📋 清單管理**: TODO 和 PRIORITY 兩種清單類型
    * **✅ 任務追蹤**: 清單項目的完成狀態管理
    * **🗳️ 協作投票**: PRIORITY 清單支援團隊投票決策
    * **📆 事件管理**: 行程安排和時間管理

    ### 🏗️ 資料結構

    ```
    User (用戶)
    └── Calendar (日曆) [1:N]
        ├── List (清單) [1:N]
        │   └── ListItem (清單項目) [1:N]
        │       └── Vote (投票) [1:N]
        └── Event (事件) [1:N]
    ```

    ### 🔧 如何開始

    1. **註冊用戶**: 使用 `/api/v1/users/register` 建立帳號
    2. **登入取得 Token**: 使用 `/api/v1/auth/login` 獲得認證令牌
    3. **建立日曆**: 註冊時自動建立個人日曆，可手動建立專案日曆
    4. **管理清單**: 在日曆中建立 TODO 或 PRIORITY 類型清單
    5. **協作投票**: 在 PRIORITY 清單中進行團隊決策投票
    6. **規劃事件**: 建立時程安排和提醒

    ### 🔑 認證方式

    大部分 API 需要 JWT Token 認證，請在 Header 中包含：
    ```
    Authorization: Bearer <your-jwt-token>
    ```

    ### 💡 使用建議

    * **個人任務管理**: 使用個人日曆 + TODO 清單
    * **團隊協作決策**: 使用共享日曆 + PRIORITY 清單 + 投票系統
    * **專案管理**: 混合使用多種清單類型 + 事件時程規劃

    ### 📚 相關文檔

    * [完整 API 文檔](https://github.com/your-repo/DateTree/blob/main/docs/api/rest-api.md)
    * [工作流程範例](https://github.com/your-repo/DateTree/blob/main/docs/api/api-workflow-examples.md)
    """,
    version="1.0.0",
    contact={
        "name": "DateTree Development Team",
        "email": "support@datetree.dev",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_PREFIX)