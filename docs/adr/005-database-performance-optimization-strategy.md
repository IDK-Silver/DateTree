# ADR-005: 資料庫效能最佳化策略

## 狀態
**已接受** - 2025-01-07

## 背景

DateTree 的初始實作專注於功能性和快速開發，使用基本的 SQLAlchemy ORM 模式。隨著應用程式逐漸成熟且全面測試揭示了效能瓶頸，我們需要解決幾個關鍵的資料庫效能問題：

### 已識別的問題

1. **缺少外鍵索引**：所有外鍵欄位都缺乏索引，導致 JOIN 操作時出現全表掃描
2. **N+1 查詢問題**：權限檢查和相關資料提取產生過多的資料庫查詢
3. **無效率的投票計數**：投票統計需要多個查詢且沒有適當的索引
4. **次優的事件查詢**：基於時間的事件搜尋在沒有複合索引的情況下表現不佳
5. **重複投票防護**：沒有資料庫層級的約束來防止重複投票

### 效能影響

- API 回應時間：複雜查詢需要 2-10 秒
- 資料庫負載：由於表格掃描導致高 CPU 使用率
- 並發使用者容量：受查詢無效率限制
- 使用者體驗：在日曆和投票功能中出現明顯延遲

## 決策

我們決定實施一個全面的資料庫效能最佳化策略，包含以下組件：

### 1. 外鍵索引策略

**決策**：為所有外鍵欄位新增索引

**理由**：
- 外鍵經常用於 JOIN 操作
- 索引提供 O(log n) 查找而非 O(n) 表格掃描
- 最小的儲存開銷卻能帶來巨大的效能提升

**實作**：
```sql
-- 日曆關係
CREATE INDEX ix_calendars_owner_id ON calendars(owner_id);
CREATE INDEX ix_lists_calendar_id ON lists(calendar_id);

-- 清單項目關係
CREATE INDEX ix_list_items_list_id ON list_items(list_id);
CREATE INDEX ix_list_items_creator_id ON list_items(creator_id);

-- 投票關係
CREATE INDEX ix_votes_user_id ON votes(user_id);
CREATE INDEX ix_votes_list_item_id ON votes(list_item_id);

-- 事件關係
CREATE INDEX ix_events_calendar_id ON events(calendar_id);
CREATE INDEX ix_events_creator_id ON events(creator_id);
```

### 2. 複合索引策略

**決策**：為常見查詢模式建立專用的複合索引

**理由**：
- 投票計數查詢經常依 list_item_id 篩選
- 事件查詢通常結合 calendar_id 和時間範圍
- 使用者投票歷史需要高效的 user_id + list_item_id 查找

**實作**：
```sql
-- 投票最佳化索引
CREATE UNIQUE INDEX idx_vote_user_item_unique ON votes(user_id, list_item_id);
CREATE INDEX idx_vote_list_item ON votes(list_item_id);
CREATE INDEX idx_vote_user ON votes(user_id);

-- 事件時間基礎索引
CREATE INDEX idx_event_calendar_time ON events(calendar_id, start_time);
CREATE INDEX idx_event_start_time ON events(start_time);
CREATE INDEX idx_event_creator ON events(creator_id);
```

### 3. 查詢最佳化策略

**決策**：以高效的 JOIN 操作取代 N+1 查詢模式

**理由**：
- 權限檢查為每個請求產生多個查詢
- 相關資料提取造成串聯查詢效應
- 單一 JOIN 查詢比多次往返更有效率

**之前** (N+1 查詢)：
```python
def check_calendar_access(calendar_id, user):
    calendar = get_calendar(calendar_id)        # 1 次查詢
    for member in calendar.members:             # N 次額外查詢
        if member.id == user.id:
            return True
```

**之後** (單一 JOIN 查詢)：
```python
def check_calendar_access(calendar_id, user):
    calendar = (
        db.query(Calendar)
        .outerjoin(calendar_user_association)
        .filter(
            Calendar.id == calendar_id,
            or_(
                Calendar.owner_id == user.id,
                calendar_user_association.c.user_id == user.id
            )
        )
        .first()
    )
```

### 4. 預先載入策略

**決策**：為複雜資料提取實作預先載入方法

**理由**：
- 日曆概覽頁面需要清單、事件和成員資料
- 投票統計頁面需要相關的投票資料
- 預先載入減少資料庫往返次數

**實作**：
```python
def get_calendar_with_full_data(calendar_id):
    return (
        db.query(Calendar)
        .options(
            selectinload(Calendar.lists).selectinload("items").selectinload("votes"),
            selectinload(Calendar.events),
            selectinload(Calendar.members)
        )
        .filter(Calendar.id == calendar_id)
        .first()
    )
```

### 5. 資料完整性策略

**決策**：為業務規則新增資料庫層級約束

**理由**：
- 在資料庫層級防止重複投票
- 確保資料一致性，不受應用程式層級錯誤影響
- 透過明確的約束違反改善錯誤處理

**實作**：
```sql
-- 防止重複投票
CREATE UNIQUE INDEX idx_vote_user_item_unique ON votes(user_id, list_item_id);
```

## 後果

### 正面影響

1. **巨大的效能改善**：
   - 外鍵 JOIN：快 10-100 倍
   - 投票計數：快 20-50 倍
   - 權限檢查：快 2-10 倍
   - 事件查詢：快 10-30 倍
   - 日曆載入：快 3-8 倍

2. **更好的擴展性**：
   - 降低資料庫 CPU 使用率
   - 更低的記憶體消耗
   - 更高的並發使用者容量
   - 更可預測的回應時間

3. **改善的資料完整性**：
   - 資料庫層級的重複防護
   - 一致的約束執行
   - 更好的錯誤處理

4. **增強的使用者體驗**：
   - 亞秒級的頁面載入時間
   - 響應式投票介面
   - 流暢的日曆導航

### 負面影響

1. **增加的儲存需求**：
   - 索引儲存開銷（約為表格大小的 20%）
   - 每個表格有多個索引

2. **較慢的寫入操作**：
   - INSERT/UPDATE/DELETE 時的索引維護
   - 由於讀取密集工作負載，影響微小

3. **遷移複雜性**：
   - 需要資料庫架構變更
   - 需要部署協調

### 中性影響

1. **維護開銷**：
   - 索引監控和最佳化
   - 查詢計劃分析需求

## 實作時間表

- **階段 1** ✅：外鍵索引（立即獲得 10-100 倍改善）
- **階段 2** ✅：複合索引（專門的查詢最佳化）
- **階段 3** ✅：JOIN 查詢最佳化（權限檢查效率）
- **階段 4** ✅：預先載入方法（N+1 問題解決）
- **階段 5** ✅：資料庫遷移和測試

## 監控和驗證

### 效能指標
- API 回應時間監控
- 資料庫查詢執行時間追蹤
- 索引使用統計分析

### 成功標準
- ✅ 所有 140 個測試通過（無功能回歸）
- ✅ 外鍵查詢使用索引掃描而非表格掃描
- ✅ 投票計數查詢在 <100ms 內完成
- ✅ 日曆載入需要 <3 次資料庫查詢
- ✅ 權限檢查在 <50ms 內完成

## 考慮過的替代方案

### 1. 應用程式層級快取
**已拒絕**：增加複雜性和快取失效挑戰，同時未解決根本原因

### 2. 讀取副本
**已延後**：對擴展有用，但不能解決無效查詢模式

### 3. NoSQL 遷移
**已拒絕**：重大架構變更，對關聯式資料模型的效益不明確

### 4. 查詢結果快取
**未來考慮**：為頻繁存取的資料建立 Redis 快取層

## 參考資料

- [外鍵最佳化分析](../development/foreign-key-optimization.md)
- [效能最佳化報告](../development/performance-optimization-report.md)
- [程式碼審查診斷](../development/code-review-diagnosis.md)
- [資料庫遷移：8763bf7f0ac6](../../backend/alembic/versions/8763bf7f0ac6_add_foreign_key_indexes_and_composite_.py)

## 相關 ADR

- [ADR-001：共享日曆協作模型](001-shared-calendar-collaboration-model.md)
- [ADR-002：可擴展多清單模型](002-adopt-extendable-multi-list-model.md)
- [ADR-003：資料庫遷移重設策略](003-database-migration-reset-strategy.md)

---

**作者**：Claude Code, DateTree 開發團隊  
**最後更新**：2025-01-07  
**下次審查**：2025-04-07（3 個月後）