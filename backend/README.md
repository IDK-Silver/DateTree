# DateTree Backend

此目錄包含 DateTree 後端應用程式的原始碼，使用 FastAPI 建構。

## 資料架構概覽

DateTree 採用模組化的資料模型設計，支持靈活的協作和任務管理：

- **User** (使用者)：基本的使用者帳號資訊
- **Calendar** (日曆)：支援多使用者共享的日曆容器
- **List** (清單)：各種類型的任務清單（待辦、優先級等）
- **ListItem** (清單項目)：清單中的具體項目
- **Vote** (投票)：支援團隊決策的投票機制
- **Event** (事件)：已排程的確定事項

詳細的資料模型設計理念請參閱 [ADR 002](../docs/adr/002-adopt-extendable-multi-list-model.md)。

## 快速開始

### 1. 環境設定

本專案使用 [uv](https://github.com/astral-sh/uv) 進行環境和套件管理。

```bash
# 同步環境與依賴套件
uv sync

# 複製環境變數檔案
cp .env.example .env
# 編輯 .env 檔案設定您的資料庫連線資訊
```

### 2. 資料庫設定

```bash
# 套用資料庫遷移
uv run alembic upgrade head
```

### 3. 啟動開發伺服器

```bash
# 啟動 FastAPI 開發伺服器
uv run uvicorn app.main:app --reload
```

伺服器將在 <http://127.0.0.1:8000> 啟動，API 文檔位於 <http://127.0.0.1:8000/docs>。

## 開發指令

### 資料庫遷移

```bash
# 修改模型後產生新的遷移檔案
uv run alembic revision --autogenerate -m "您的描述訊息"

# 套用遷移
uv run alembic upgrade head

# 查看遷移歷史
uv run alembic history

# 降級一個版本（較少使用）
uv run alembic downgrade -1
```

#### 重大架構變更時的遷移重置

在開發階段，當進行重大資料模型重構時（如從 Calendar-Event 架構遷移到 Calendar-List-ListItem-Vote-Event 架構），建議重置遷移歷史：

```bash
# 1. 刪除資料庫中的所有資料和架構（謹慎使用！）
# 如果使用 Docker：
docker-compose down -v
docker-compose up -d

# 或者直接重建資料庫：
dropdb your_database_name
createdb your_database_name

# 2. 刪除舊的遷移檔案
rm -rf alembic/versions/*.py

# 3. 產生新的初始遷移
uv run alembic revision --autogenerate -m "Initial migration with new model structure"

# 4. 套用新的遷移
uv run alembic upgrade head
```

**重要提醒**：遷移重置只應在開發階段進行，生產環境中應使用漸進式遷移。

### 執行測試

```bash
# 執行所有測試
uv run pytest

# 執行測試並顯示覆蓋率
uv run pytest --cov=app

# 執行特定測試檔案
uv run pytest tests/test_crud_list.py

# 執行特定測試類別
uv run pytest tests/test_api_list.py::TestListAPI

# 執行特定測試函數
uv run pytest tests/test_crud_list.py::TestListCRUD::test_create_list

# 顯示詳細輸出
uv run pytest -v

# 執行測試並停在第一個失敗
uv run pytest -x
```

## API 文檔

* **Swagger UI**: <http://127.0.0.1:8000/docs>
* **ReDoc**: <http://127.0.0.1:8000/redoc>

## 架構與貢獻

關於以下詳細資訊：

* 程式碼架構和專案結構
* 開發指南和最佳實踐
* 如何貢獻程式碼

請參閱 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 故障排除

### 常見問題

#### 資料庫連線失敗

- 檢查 `.env` 檔案中的 `DATABASE_URL` 設定
- 確保 PostgreSQL 服務正在執行

#### 遷移失敗

- 驗證資料庫權限
- 確保所有模型都已匯入到 `alembic/env.py`
- 檢查是否存在衝突的資料庫物件

#### 模型重構後的資料庫問題

如果在重大模型重構後遇到資料庫相關錯誤：

1. **檢查模型匯入**：確認所有新模型都已在 `app/models/__init__.py` 中正確匯入
2. **驗證 Alembic 設定**：檢查 `alembic/env.py` 是否正確匯入了新的 Base 和所有模型
3. **清理並重建**：考慮刪除舊遷移並重新產生初始遷移（僅開發環境）

#### 套件安裝問題

- 刪除 `.venv` 目錄並重新執行 `uv sync`
- 如果 `uv.lock` 損壞，可刪除後重新執行 `uv sync`
