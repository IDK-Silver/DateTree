# 用戶管理 API 實施文檔

## 📋 概述

本文檔描述 DateTree 用戶管理系統的實施詳情，包括用戶註冊 API 和相關的測試架構。

## 🚀 已實施功能

### 用戶註冊 API

- **端點**: `POST /api/v1/users/register`
- **功能**: 註冊新用戶帳號
- **認證**: 不需要（公開端點）

#### 請求格式

```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

#### 成功回應 (200 OK)

```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true
}
```

#### 錯誤回應

- **400 Bad Request**: 電子郵件已存在
- **422 Unprocessable Entity**: 資料驗證錯誤

## 🏗️ 架構實施

### 資料模型

使用 SQLAlchemy 定義的 `User` 模型：

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
```

### Pydantic Schemas

- `UserCreate`: 用戶註冊請求 schema
- `User`: 用戶回應 schema
- `UserInDB`: 資料庫用戶 schema（包含 hashed_password）

### CRUD 操作

- `crud.user.create()`: 建立用戶（密碼雜湊）
- `crud.user.get_by_email()`: 根據電子郵件查找用戶

## 🔐 安全實施

### 密碼處理

- 使用 `passlib` 進行密碼雜湊
- bcrypt 雜湊演算法
- 原始密碼不會儲存在資料庫中
- API 回應不包含密碼或雜湊密碼

### 輸入驗證

- 電子郵件格式驗證（使用 EmailStr）
- 必填欄位驗證
- 重複註冊檢查

## 🧪 測試覆蓋

### 測試檔案: `test_api_user.py`

包含 7 個完整測試用例：

1. **成功註冊測試**
   - 驗證正確的註冊流程
   - 檢查資料庫中的用戶建立
   - 確認回應格式正確

2. **重複電子郵件測試**
   - 驗證重複註冊防護
   - 確認錯誤訊息正確

3. **輸入驗證測試**
   - 無效電子郵件格式
   - 缺少必填欄位
   - 空密碼處理

4. **邊界條件測試**
   - 弱密碼接受（記錄當前行為）

### 測試特色

- **資料隔離**: 每個測試使用獨立的資料庫
- **完整覆蓋**: 包含正常流程和錯誤情況
- **真實環境**: 使用 FastAPI TestClient 進行整合測試

## 📈 測試結果

```bash
$ uv run pytest tests/test_api_user.py -v

tests/test_api_user.py::TestUserRegistration::test_register_user_success PASSED
tests/test_api_user.py::TestUserRegistration::test_register_user_duplicate_email PASSED
tests/test_api_user.py::TestUserRegistration::test_register_user_invalid_email PASSED
tests/test_api_user.py::TestUserRegistration::test_register_user_missing_password PASSED
tests/test_api_user.py::TestUserRegistration::test_register_user_missing_email PASSED
tests/test_api_user.py::TestUserRegistration::test_register_user_empty_password PASSED
tests/test_api_user.py::TestUserRegistration::test_register_user_weak_password_accepted PASSED

========================= 7 passed in 0.78s =========================
```

## 🔄 待完成功能

### 高優先級

1. **用戶登入 API**
   - JWT token 產生
   - 密碼驗證
   - Token 回應格式

2. **密碼強度驗證**
   - 最小長度要求
   - 複雜度規則
   - 錯誤訊息改善

3. **權限驗證中間件**
   - JWT token 驗證
   - 用戶身分識別
   - 權限檢查

### 中優先級

1. **用戶資料管理**
   - 更新用戶資訊
   - 修改密碼
   - 帳號停用

2. **電子郵件驗證**
   - 註冊確認信
   - 帳號啟用流程

## 🚀 部署注意事項

### 環境變數

確保以下環境變數正確設定：

```bash
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

### 資料庫遷移

用戶表結構已包含在現有的 Alembic 遷移中：

```bash
# 執行遷移
uv run alembic upgrade head
```

## 📝 更新記錄

### 2025-06-30

- ✅ 實施用戶註冊 API (`POST /api/v1/users/register`)
- ✅ 創建完整的測試覆蓋（7 個測試用例）
- ✅ 更新 API 文檔
- ✅ 更新專案 README
- ✅ 密碼雜湊安全實施
- ✅ 輸入驗證和錯誤處理

---

**作者**: DateTree 開發團隊  
**最後更新**: 2025-06-30
