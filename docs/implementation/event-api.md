# Event API 實施詳情

## 概覽

Event API 提供完整的日曆事件管理功能，支援排程事件的創建、查詢、更新和刪除，並提供強大的時間範圍查詢和即將到來的事件查詢功能。

## 實施日期

**開發完成**: 2025-07-01

## API 端點

### 基礎路徑
```
/api/v1/events/
```

### 端點列表

#### 1. 查詢日曆事件

```http
GET /api/v1/events/calendar/{calendar_id}
```

**功能**: 獲取指定日曆的所有事件  
**參數**:
- `calendar_id`: 日曆ID (路徑參數)
- `skip`: 分頁偏移 (查詢參數，預設 0)
- `limit`: 分頁限制 (查詢參數，預設 100)

**回應**: `List[Event]`

#### 2. 查詢即將到來的事件

```http
GET /api/v1/events/calendar/{calendar_id}/upcoming
```

**功能**: 獲取指定日曆即將到來的事件  
**參數**:
- `calendar_id`: 日曆ID (路徑參數)
- `from_time`: 起始時間 (查詢參數，可選，預設為當前時間)
- `skip`, `limit`: 分頁參數

**特色**: 按時間排序，預設從當前時間開始

#### 3. 按日期範圍查詢事件

```http
GET /api/v1/events/calendar/{calendar_id}/date-range
```

**功能**: 獲取指定日期範圍內的事件  
**參數**:
- `calendar_id`: 日曆ID (路徑參數)
- `start_date`: 開始日期 (查詢參數，必填)
- `end_date`: 結束日期 (查詢參數，必填)
- `skip`, `limit`: 分頁參數

**用途**: 月/週/日視圖的事件查詢

#### 4. 獲取單一事件

```http
GET /api/v1/events/{event_id}
```

**功能**: 獲取指定事件的詳細資訊

#### 5. 創建事件

```http
POST /api/v1/events/
```

**請求體**:
```json
{
  "title": "會議",
  "description": "團隊週會",
  "start_time": "2025-07-01T10:00:00Z",
  "end_time": "2025-07-01T11:00:00Z",
  "calendar_id": 1
}
```

**功能**: 創建新的日曆事件，自動記錄創建者

#### 6. 更新事件

```http
PUT /api/v1/events/{event_id}
```

**請求體**:
```json
{
  "title": "更新的會議標題",
  "start_time": "2025-07-01T14:00:00Z"
}
```

**功能**: 更新指定事件的資訊

#### 7. 刪除事件

```http
DELETE /api/v1/events/{event_id}
```

**功能**: 刪除指定的日曆事件

## 資料模型

### Event Schema

#### 基礎屬性 (EventBase)
```python
{
  "title": str,                    # 事件標題
  "description": Optional[str],    # 事件描述（可選）
  "start_time": datetime,          # 開始時間
  "end_time": Optional[datetime],  # 結束時間（可選）
  "calendar_id": int              # 所屬日曆ID
}
```

#### 創建 Schema (EventCreate)
- 繼承所有基礎屬性
- 用於 POST 請求

#### 更新 Schema (EventUpdate)
```python
{
  "title": Optional[str],          # 可選更新標題
  "description": Optional[str],    # 可選更新描述
  "start_time": Optional[datetime], # 可選更新開始時間
  "end_time": Optional[datetime]   # 可選更新結束時間
}
```

#### 回應 Schema (Event)
```python
{
  "id": int,                      # 事件ID
  "title": str,                   # 事件標題
  "description": Optional[str],    # 事件描述
  "start_time": datetime,         # 開始時間
  "end_time": Optional[datetime], # 結束時間
  "calendar_id": int,             # 所屬日曆ID
  "creator_id": Optional[int]     # 創建者ID
}
```

## CRUD 操作

### 核心類別: CRUDEvent

位置: `app/crud/crud_event.py`

#### 特殊方法

1. **create_with_user()**
   - 自動記錄創建者ID
   - 確保事件與創建用戶關聯

2. **get_multi_by_calendar()**
   - 按日曆ID查詢所有事件
   - 支援分頁

3. **get_multi_by_date_range()**
   - 按日期範圍查詢事件
   - 支援月/週/日視圖
   - 高效的時間範圍SQL查詢

4. **get_upcoming_events()**
   - 獲取即將到來的事件
   - 自動從當前時間或指定時間開始
   - 按開始時間排序

## 時間處理

### 時區支援
- 使用 `DateTime(timezone=True)` 儲存
- 支援 UTC 時間戳
- 前端需處理本地時區轉換

### 時間查詢優化
```python
# 日期範圍查詢
db.query(Event)\
  .filter(Event.start_time >= start_date)\
  .filter(Event.start_time <= end_date)

# 即將到來的事件
db.query(Event)\
  .filter(Event.start_time >= from_time)\
  .order_by(Event.start_time)
```

## 安全性與權限

### 認證要求
- 所有端點都需要有效的 JWT token
- 事件操作綁定到特定用戶

### 權限控制
- 當前實施: 基礎用戶身份驗證
- TODO: 添加日曆存取權限檢查
- TODO: 區分事件的查看/編輯權限

## 錯誤處理

### HTTP 狀態碼
- `200`: 成功
- `404`: 事件或日曆不存在
- `401`: 未授權訪問
- `422`: 請求資料驗證錯誤（如無效日期格式）

### 日期驗證
- 開始時間不能晚於結束時間
- 日期格式必須符合 ISO 8601
- 時區資訊需正確處理

## 資料庫關聯

### 關聯關係
```
Event
├── belongs_to: Calendar (calendar_id)
└── belongs_to: User (creator_id)
```

### 索引優化
- `calendar_id`: 支援按日曆查詢
- `start_time`: 支援時間範圍查詢
- `creator_id`: 支援按創建者查詢
- 複合索引: `(calendar_id, start_time)` 用於最佳化日期範圍查詢

## 使用範例

### 創建事件
```bash
curl -X POST "http://localhost:8000/api/v1/events/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "團隊會議",
    "description": "週例會討論專案進度",
    "start_time": "2025-07-02T10:00:00Z",
    "end_time": "2025-07-02T11:00:00Z",
    "calendar_id": 1
  }'
```

### 查詢本週事件
```bash
curl -X GET "http://localhost:8000/api/v1/events/calendar/1/date-range?start_date=2025-07-01T00:00:00Z&end_date=2025-07-07T23:59:59Z" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 查詢即將到來的事件
```bash
curl -X GET "http://localhost:8000/api/v1/events/calendar/1/upcoming" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 更新事件時間
```bash
curl -X PUT "http://localhost:8000/api/v1/events/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "start_time": "2025-07-02T14:00:00Z",
    "end_time": "2025-07-02T15:00:00Z"
  }'
```

## 應用場景

### 1. 個人行程管理
```
- 創建日常會議、約會事件
- 查看今日/本週行程
- 設定提醒和通知
```

### 2. 團隊協作
```
- 創建團隊會議
- 查看團隊共享日曆
- 安排專案里程碑
```

### 3. 專案管理
```
- 設定專案截止日期
- 追蹤重要里程碑
- 規劃工作時程
```

## 與 ListItem 的整合

### 從待辦到事件
```python
# 將高票 ListItem 轉換為 Event
# 未來功能：支援一鍵轉換
```

### 事件狀態同步
```python
# 完成的事件可更新相關 ListItem 狀態
# 支援雙向同步
```

## 未來改進

### 短期
- [ ] 實施日曆存取權限檢查
- [ ] 事件重複設定（週期性事件）
- [ ] 事件提醒功能

### 中期
- [ ] 事件邀請和回覆
- [ ] 事件衝突檢測
- [ ] 事件範本系統

### 長期
- [ ] 智能時程安排
- [ ] 跨時區支援優化
- [ ] 事件分析和報告

## 效能考量

### 查詢優化
- 使用適當的資料庫索引
- 分頁查詢避免大量資料載入
- 時間範圍查詢使用高效的 WHERE 條件

### 快取策略
- 考慮對頻繁查詢的日曆事件進行快取
- 即將到來的事件可以快取短時間

## 相關文檔

- [ListItem API 實施詳情](list-item-api.md)
- [Vote API 實施詳情](vote-api.md)
- [Calendar Management API](calendar-management-api.md)
- [ADR-002: 採用可擴展的多清單協作模型](../adr/002-adopt-extendable-multi-list-model.md)