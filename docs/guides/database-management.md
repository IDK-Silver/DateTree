# 資料庫管理指南

本指南說明 DateTree 專案的資料庫管理，包括遷移、備份、和故障排除。

## 🏗️ 資料庫架構

DateTree 使用 PostgreSQL 作為主要資料庫，採用 SQLAlchemy ORM 和 Alembic 進行遷移管理。

### 核心資料表

* **users** - 使用者基本資訊
* **calendars** - 日曆容器
* **calendar_user_association** - 使用者與日曆的多對多關聯
* **lists** - 各類型清單（待辦、優先級等）
* **list_items** - 清單中的具體項目
* **votes** - 投票記錄
* **events** - 已排程的確定事件

詳細的資料模型請參閱 [資料模型架構文檔](../architecture/data-models.md)。

## 🔄 Alembic 遷移管理

### 基本操作

#### 查看遷移狀態

```bash
# 查看當前遷移版本
uv run alembic current

# 查看遷移歷史
uv run alembic history

# 查看詳細遷移歷史
uv run alembic history --verbose
```

#### 執行遷移

```bash
# 升級到最新版本
uv run alembic upgrade head

# 升級到特定版本
uv run alembic upgrade <revision_id>

# 升級一個版本
uv run alembic upgrade +1
```

#### 回滾遷移

```bash
# 回滾到上一個版本
uv run alembic downgrade -1

# 回滾到特定版本
uv run alembic downgrade <revision_id>

# 回滾到初始狀態 (小心使用!)
uv run alembic downgrade base
```

### 創建新遷移

#### 自動生成遷移

```bash
# 根據模型變更自動生成遷移
uv run alembic revision --autogenerate -m "描述變更內容"

# 例如：
uv run alembic revision --autogenerate -m "add user preferences table"
uv run alembic revision --autogenerate -m "add index to list_items.created_at"
```

#### 手動創建遷移

```bash
# 創建空的遷移檔案
uv run alembic revision -m "描述變更內容"
```

然後編輯生成的遷移檔案：

```python
"""add custom constraint

Revision ID: abc123
Revises: def456
Create Date: 2025-06-29 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'abc123'
down_revision = 'def456'
branch_labels = None
depends_on = None

def upgrade():
    # 升級操作
    op.create_check_constraint(
        'ck_list_name_not_empty',
        'lists',
        'length(name) > 0'
    )

def downgrade():
    # 回滾操作
    op.drop_constraint('ck_list_name_not_empty', 'lists')
```

### 遷移最佳實踐

#### 開發環境

* **頻繁測試**：每次模型變更後立即生成和測試遷移
* **檢查自動生成**：Alembic 自動生成的遷移不一定完美，需要人工檢查
* **測試回滾**：確保 downgrade 函式正確實作

#### 生產環境

* **備份優先**：執行遷移前務必備份資料庫
* **分階段部署**：在測試環境完全驗證後才部署到生產環境
* **監控性能**：大型遷移可能影響性能，需要在維護時間執行

#### 遷移檢查清單

在提交遷移之前，請確認：

- [ ] 遷移可以正常執行 (`upgrade`)
- [ ] 遷移可以正常回滾 (`downgrade`)
- [ ] 沒有資料遺失的風險
- [ ] 大型變更已在測試環境驗證
- [ ] 提供了適當的遷移說明

## 💾 資料庫備份與恢復

### 開發環境備份

#### 使用 pg_dump

```bash
# 備份整個資料庫
pg_dump -h localhost -U your_user -d datetree_dev > backup.sql

# 僅備份資料 (不包括結構)
pg_dump -h localhost -U your_user -d datetree_dev --data-only > data_backup.sql

# 僅備份特定表
pg_dump -h localhost -U your_user -d datetree_dev -t users -t calendars > partial_backup.sql
```

#### 使用 Docker

```bash
# 如果使用 Docker Compose
docker-compose exec db pg_dump -U postgres datetree_dev > backup.sql
```

### 恢復資料庫

```bash
# 從備份恢復
psql -h localhost -U your_user -d datetree_dev < backup.sql

# 如果使用 Docker
docker-compose exec -T db psql -U postgres -d datetree_dev < backup.sql
```

### 生產環境策略

生產環境應該實施：

* **定期自動備份**：每日完整備份 + 更頻繁的增量備份
* **異地備份**：將備份儲存在不同的地理位置
* **備份驗證**：定期測試備份的完整性和可恢復性
* **災害恢復計劃**：明確的恢復步驟和責任分工

## 🔧 故障排除

### 常見問題

#### 問題：遷移執行失敗

**症狀**：`alembic upgrade head` 出現錯誤

**可能原因**：
* 資料庫連線問題
* 遷移腳本錯誤
* 資料完整性約束衝突

**解決步驟**：

1. 檢查資料庫連線：
   ```bash
   # 測試連線
   psql -h localhost -U your_user -d datetree_dev -c "SELECT version();"
   ```

2. 查看詳細錯誤：
   ```bash
   uv run alembic upgrade head --verbose
   ```

3. 檢查遷移腳本：
   ```bash
   # 查看有問題的遷移檔案
   cat alembic/versions/<revision_id>_*.py
   ```

4. 手動修復或回滾：
   ```bash
   # 回滾到上一個可工作的版本
   uv run alembic downgrade -1
   ```

#### 問題：資料庫鎖定

**症狀**：操作卡住或超時

**解決方法**：

1. 檢查活動連線：
   ```sql
   SELECT pid, state, query FROM pg_stat_activity WHERE datname = 'datetree_dev';
   ```

2. 終止問題連線：
   ```sql
   SELECT pg_terminate_backend(pid) FROM pg_stat_activity 
   WHERE datname = 'datetree_dev' AND state = 'idle in transaction';
   ```

#### 問題：測試資料庫問題

**症狀**：測試執行失敗或緩慢

**解決方法**：

1. 重建測試資料庫：
   ```bash
   # 刪除並重建測試資料庫檔案 (SQLite)
   rm test.db
   uv run pytest
   ```

2. 清理測試資料：
   ```bash
   # 確保測試資料庫隔離
   uv run pytest --tb=short -v
   ```

### 效能調優

#### 查詢優化

```sql
-- 查看慢查詢
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- 分析查詢計劃
EXPLAIN ANALYZE SELECT * FROM lists 
WHERE calendar_id = 1 AND list_type = 'TODO';
```

#### 索引管理

```sql
-- 查看缺少索引的查詢
SELECT schemaname, tablename, attname, n_distinct, correlation 
FROM pg_stats 
WHERE schemaname = 'public';

-- 創建需要的索引
CREATE INDEX idx_lists_calendar_type ON lists(calendar_id, list_type);
CREATE INDEX idx_list_items_list_created ON list_items(list_id, created_at);
```

## 🚀 開發工作流程

### 日常開發

```bash
# 1. 拉取最新程式碼
git pull origin main

# 2. 檢查是否有新的遷移
uv run alembic current
uv run alembic history | head -5

# 3. 如果有新遷移，執行升級
uv run alembic upgrade head

# 4. 開始開發...
```

### 功能開發中的資料庫變更

```bash
# 1. 修改模型 (app/models/*.py)
# 2. 生成遷移
uv run alembic revision --autogenerate -m "描述你的變更"

# 3. 檢查生成的遷移檔案
cat alembic/versions/<new_revision>_*.py

# 4. 測試遷移
uv run alembic upgrade head
uv run alembic downgrade -1  # 測試回滾
uv run alembic upgrade head  # 重新升級

# 5. 執行測試確保一切正常
uv run pytest
```

### 準備部署

```bash
# 1. 確保所有遷移都已測試
uv run alembic history --verbose

# 2. 在生產類似環境中測試
# 3. 準備回滾計劃
# 4. 執行生產部署
```

## 📊 監控與維護

### 資料庫健康檢查

```sql
-- 檢查資料庫大小
SELECT pg_size_pretty(pg_database_size('datetree_dev'));

-- 檢查表大小
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- 檢查連線數
SELECT count(*) FROM pg_stat_activity;
```

### 定期維護任務

* **清理舊資料**：定期清理不需要的測試資料
* **更新統計資訊**：`ANALYZE;` 確保查詢優化器有最新資訊
* **檢查索引使用率**：移除不使用的索引
* **監控磁碟空間**：確保有足夠的儲存空間

## 📚 相關資源

* [PostgreSQL 官方文檔](https://www.postgresql.org/docs/)
* [Alembic 文檔](https://alembic.sqlalchemy.org/)
* [SQLAlchemy 文檔](https://docs.sqlalchemy.org/)
* [專案資料模型架構](../architecture/data-models.md)
* [ADR-003: 資料庫遷移重置策略](../adr/003-database-migration-reset-strategy.md)
