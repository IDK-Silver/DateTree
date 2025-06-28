# DateTree Backend

此目錄包含 DateTree 後端應用程式的原始碼，使用 FastAPI 建構。

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

### 執行測試

```bash
# 執行所有測試（未來實作）
uv run pytest

# 執行測試並顯示覆蓋率（未來實作）
uv run pytest --cov=app
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

**資料庫連線失敗**

* 檢查 `.env` 檔案中的 `DATABASE_URL` 設定
* 確保 PostgreSQL 服務正在執行

**遷移失敗**

* 驗證資料庫權限
* 確保所有模型都已匯入到 `alembic/env.py`

**套件安裝問題**

* 刪除 `.venv` 目錄並重新執行 `uv sync`
