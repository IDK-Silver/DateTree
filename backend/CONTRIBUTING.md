# Backend Contributing Guide

感謝您對 DateTree 後端的貢獻！這份文件將引導您了解後端的開發流程與程式碼架構。

## 程式碼架構 (Code Architecture)

為了保持專案的清晰和可維護性，我們採用了分層的架構。在 `backend/app/` 目錄下，核心的商業邏輯主要分為以下幾個部分：

### `schemas/` - 資料驗證層

* **目的**: 存放所有 Pydantic 模型 (Schemas)。
* **職責**:
  * 定義 API 請求的資料格式（例如：從客戶端傳入的 JSON body）。
  * 定義 API 回應的資料格式（例如：要回傳給客戶端的資料結構）。
  * 確保資料在進入應用程式核心之前是有效且格式正確的。
* **範例**: `user_create.py`, `event_read.py`

### `crud/` - 資料庫互動層

* **目的**: 存放所有與資料庫直接進行 CRUD (Create, Read, Update, Delete) 操作的函式。
* **職責**:
  * 將 Pydantic 模型轉換為 SQLAlchemy 模型。
  * 執行資料庫查詢、新增、修改、刪除等操作。
  * 處理資料庫會話 (session)。
  * 這一層的函式應該保持單純，只負責與資料庫的互動，不包含複雜的業務邏輯。
* **範例**: `crud_user.py`, `crud_event.py`

### `api/` - API 路由層

* **目的**: 存放所有 FastAPI 的 API 端點 (Endpoints) / 路由 (Routes)。
* **職責**:
  * 定義 API 路徑（例如 `/users/`, `/calendars/{calendar_id}`）。
  * 處理 HTTP 請求和回應。
  * 呼叫 `crud` 層和 `schemas` 層來完成具體的工作。
  * 處理權限驗證、依賴注入等。

### `models/` - 資料庫模型層

* **目的**: 存放所有 SQLAlchemy 的資料庫模型。
* **職責**: 定義資料在資料庫中的結構（資料表、欄位、關聯性）。
* **架構**: 採用模組化設計，每個模型都有自己的檔案：
  * `base.py` - 基礎模型和共用功能
  * `user.py` - 使用者模型
  * `calendar.py` - 日曆模型和使用者關聯
  * `list.py` - 清單模型和清單類型
  * `list_item.py` - 清單項目模型
  * `vote.py` - 投票模型
  * `event.py` - 事件模型
  * `__init__.py` - 模型匯入（重要：確保 Alembic 能偵測到所有模型）

#### 資料模型關係

```
User ←→ Calendar (多對多，透過 calendar_user_association)
Calendar → List (一對多)
List → ListItem (一對多)
ListItem ← Vote (一對多)
User → Vote (一對多)
Calendar → Event (一對多)
User → Event (一對多，作為建立者)
```

---

## 請求流程

一個典型的 API 請求流程如下：

```
客戶端 -> api (路由層) -> crud (資料庫互動層) -> models (資料庫模型)
```

並在過程中透過 `schemas` (資料驗證層) 來驗證與格式化資料。

## 資料庫遷移最佳實踐

### 日常開發流程

1. **修改模型後**：
   ```bash
   uv run alembic revision --autogenerate -m "描述性的訊息"
   ```

2. **檢查產生的遷移檔案**：
   - 確認遷移檔案正確反映了您的變更
   - 檢查是否有意外的變更（如重新命名資料表）

3. **套用遷移**：
   ```bash
   uv run alembic upgrade head
   ```

### 重大架構變更

當進行重大模型重構時（如本專案從 Calendar-Event 架構遷移到 Calendar-List-ListItem-Vote-Event 架構）：

1. **開發環境可以考慮重置遷移**：
   - 刪除舊遷移檔案
   - 產生新的初始遷移
   - 重建資料庫

2. **生產環境必須使用漸進式遷移**：
   - 保留所有遷移歷史
   - 使用資料遷移腳本處理資料轉換
   - 測試每個遷移步驟

### 模型變更檢查清單

- [ ] 所有新模型都已在 `app/models/__init__.py` 中匯入
- [ ] `alembic/env.py` 正確匯入新的 Base 和所有模型
- [ ] 執行 `alembic check` 驗證當前模型與資料庫一致
- [ ] 測試遷移的向上和向下腳本

## 開發建議

1. **保持職責分離**: 每一層都應該專注於自己的職責，避免跨層的複雜邏輯。
2. **使用類型提示**: 所有函式都應該包含適當的類型提示。
3. **編寫測試**: 為每個新功能編寫相應的測試。
4. **遵循命名慣例**: 使用清楚且一致的命名方式。
5. **模型變更時謹慎處理**: 任何資料庫模型的變更都應該透過 Alembic 遷移來管理。
