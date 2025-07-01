# ListItem API 實施詳情

## 概覽

ListItem API 提供完整的清單項目管理功能，支援在不同類型的清單中創建、查詢、更新和刪除項目，並整合了投票計數功能。

## 實施日期

**開發完成**: 2025-07-01

## API 端點

### 基礎路徑
```
/api/v1/list-items/
```

### 端點列表

#### 1. 查詢列表項目

```http
GET /api/v1/list-items/list/{list_id}
```

**功能**: 獲取指定清單的所有項目  
**參數**:
- `list_id`: 清單ID (路徑參數)
- `skip`: 分頁偏移 (查詢參數，預設 0)
- `limit`: 分頁限制 (查詢參數，預設 100)

**回應**: `List[ListItem]`

#### 2. 查詢帶投票數的列表項目

```http
GET /api/v1/list-items/list/{list_id}/with-votes
```

**功能**: 獲取指定清單的所有項目及其投票數  
**特色**: 使用 SQL 聚合查詢優化效能  
**回應**: 包含 `vote_count` 欄位的項目列表

#### 3. 獲取單一項目

```http
GET /api/v1/list-items/{item_id}
```

**功能**: 獲取指定的清單項目詳情

#### 4. 創建項目

```http
POST /api/v1/list-items/
```

**請求體**:
```json
{
  "content": "項目內容",
  "is_completed": false,
  "list_id": 1
}
```

**功能**: 創建新的清單項目，自動記錄創建者

#### 5. 更新項目

```http
PUT /api/v1/list-items/{item_id}
```

**請求體**:
```json
{
  "content": "更新的內容",
  "is_completed": true
}
```

**功能**: 更新指定項目的內容或完成狀態

#### 6. 刪除項目

```http
DELETE /api/v1/list-items/{item_id}
```

**功能**: 刪除指定的清單項目

## 資料模型

### ListItem Schema

#### 基礎屬性 (ListItemBase)
```python
{
  "content": str,          # 項目內容
  "is_completed": bool,    # 完成狀態，預設 false
  "list_id": int          # 所屬清單ID
}
```

#### 創建 Schema (ListItemCreate)
- 繼承所有基礎屬性
- 用於 POST 請求

#### 更新 Schema (ListItemUpdate)
```python
{
  "content": Optional[str],      # 可選更新內容
  "is_completed": Optional[bool] # 可選更新完成狀態
}
```

#### 回應 Schema (ListItem)
```python
{
  "id": int,                    # 項目ID
  "content": str,               # 項目內容
  "is_completed": bool,         # 完成狀態
  "list_id": int,              # 所屬清單ID
  "creator_id": Optional[int],  # 創建者ID
  "created_at": datetime,       # 創建時間
  "vote_count": Optional[int]   # 投票數（特定端點）
}
```

## CRUD 操作

### 核心類別: CRUDListItem

位置: `app/crud/crud_list_item.py`

#### 特殊方法

1. **create_with_user()**
   - 自動記錄創建者ID
   - 確保項目與用戶關聯

2. **get_multi_by_list()**
   - 按清單ID查詢所有項目
   - 支援分頁

3. **get_with_vote_count()**
   - 獲取單一項目及其投票數
   - 使用 SQL JOIN 和聚合函數

4. **get_multi_with_vote_counts()**
   - 批量獲取項目及投票數
   - 優化的 SQL 查詢效能

## 安全性與權限

### 認證要求
- 所有端點都需要有效的 JWT token
- 使用 `get_current_active_user` 依賴注入

### 權限控制
- 當前實施: 基礎用戶身份驗證
- TODO: 添加清單存取權限檢查
- TODO: 確保用戶只能操作有權限的清單

## 錯誤處理

### HTTP 狀態碼
- `200`: 成功
- `404`: 項目或清單不存在
- `401`: 未授權訪問
- `422`: 請求資料驗證錯誤

### 錯誤回應格式
```json
{
  "detail": "錯誤描述"
}
```

## 資料庫關聯

### 關聯關係
```
ListItem
├── belongs_to: List (list_id)
├── belongs_to: User (creator_id)
└── has_many: Vote (投票)
```

### 索引優化
- `list_id`: 支援按清單查詢
- `creator_id`: 支援按創建者查詢
- `created_at`: 支援時間排序

## 使用範例

### 創建待辦事項
```bash
curl -X POST "http://localhost:8000/api/v1/list-items/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "買牛奶",
    "list_id": 1
  }'
```

### 查詢清單項目（含投票數）
```bash
curl -X GET "http://localhost:8000/api/v1/list-items/list/1/with-votes" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 標記項目為完成
```bash
curl -X PUT "http://localhost:8000/api/v1/list-items/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "is_completed": true
  }'
```

## 未來改進

### 短期
- [ ] 實施清單存取權限檢查
- [ ] 添加項目排序功能
- [ ] 支援批量操作

### 中期
- [ ] 項目標籤系統
- [ ] 項目優先級
- [ ] 項目依賴關係

### 長期
- [ ] 項目歷史追蹤
- [ ] 項目範本系統
- [ ] 智能建議功能

## 相關文檔

- [Vote API 實施詳情](vote-api.md)
- [List CRUD API](list-crud-api.md)
- [ADR-002: 採用可擴展的多清單協作模型](../adr/002-adopt-extendable-multi-list-model.md)