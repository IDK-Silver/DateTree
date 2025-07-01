# Vote API 實施詳情

## 概覽

Vote API 實現了民主式的協作投票機制，允許團隊成員對清單項目進行投票，支援優先級決策和協作式任務規劃。

## 實施日期

**開發完成**: 2025-07-01

## API 端點

### 基礎路徑
```
/api/v1/votes/
```

### 端點列表

#### 1. 查詢項目的所有投票

```http
GET /api/v1/votes/item/{item_id}
```

**功能**: 獲取指定清單項目的所有投票記錄  
**參數**:
- `item_id`: 清單項目ID (路徑參數)
- `skip`: 分頁偏移 (查詢參數，預設 0)
- `limit`: 分頁限制 (查詢參數，預設 100)

**回應**: `List[Vote]`

#### 2. 查詢當前用戶的投票

```http
GET /api/v1/votes/user/my-votes
```

**功能**: 獲取當前用戶的所有投票記錄  
**用途**: 讓用戶查看自己投過票的項目

#### 3. 投票

```http
POST /api/v1/votes/
```

**請求體**:
```json
{
  "list_item_id": 1
}
```

**功能**: 對清單項目進行投票  
**特色**: 
- 防重複投票機制
- 自動記錄投票用戶

#### 4. 取消投票

```http
DELETE /api/v1/votes/item/{item_id}
```

**功能**: 取消當前用戶對指定項目的投票

## 資料模型

### Vote Schema

#### 基礎屬性 (VoteBase)
```python
{
  "list_item_id": int  # 投票的清單項目ID
}
```

#### 創建 Schema (VoteCreate)
- 繼承基礎屬性
- `user_id` 自動從認證獲取

#### 回應 Schema (Vote)
```python
{
  "id": int,           # 投票ID
  "user_id": int,      # 投票用戶ID
  "list_item_id": int  # 被投票的項目ID
}
```

## CRUD 操作

### 核心類別: CRUDVote

位置: `app/crud/crud_vote.py`

#### 特殊方法

1. **create_with_user()**
   - 自動設定投票用戶ID
   - 記錄投票時間

2. **get_by_user_and_item()**
   - 檢查特定用戶是否已投票
   - 防重複投票的核心邏輯

3. **get_multi_by_item()**
   - 獲取項目的所有投票
   - 支援投票統計

4. **get_multi_by_user()**
   - 獲取用戶的所有投票
   - 支援用戶投票歷史查詢

5. **remove_by_user_and_item()**
   - 精確刪除特定用戶對特定項目的投票
   - 支援投票撤回功能

## 投票機制設計

### 防重複投票
```python
# 投票前檢查
existing_vote = vote_crud.get_by_user_and_item(
    db, user_id=current_user.id, list_item_id=vote_in.list_item_id
)

if existing_vote:
    raise HTTPException(
        status_code=400, 
        detail="User has already voted for this item"
    )
```

### 投票統計整合
- 與 ListItem API 整合
- 透過 SQL JOIN 提供即時投票數
- 支援排序和優先級決策

## 安全性與權限

### 認證要求
- 所有端點都需要有效的 JWT token
- 投票操作綁定到特定用戶

### 投票完整性
- 一人一票原則
- 投票記錄不可篡改
- 支援投票撤回（透明化）

### 權限控制
- 當前實施: 認證用戶可投票
- TODO: 添加清單存取權限檢查
- TODO: 支援投票權限設定

## 錯誤處理

### HTTP 狀態碼
- `200`: 成功
- `400`: 重複投票或業務邏輯錯誤
- `404`: 項目或投票不存在
- `401`: 未授權訪問

### 特定錯誤
```json
{
  "detail": "User has already voted for this item"
}
```

## 資料庫關聯

### 關聯關係
```
Vote
├── belongs_to: User (user_id)
└── belongs_to: ListItem (list_item_id)
```

### 唯一約束
建議在資料庫層面添加：
```sql
UNIQUE(user_id, list_item_id)
```

## 使用範例

### 對項目投票
```bash
curl -X POST "http://localhost:8000/api/v1/votes/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "list_item_id": 1
  }'
```

### 查看項目的所有投票
```bash
curl -X GET "http://localhost:8000/api/v1/votes/item/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 查看我的投票記錄
```bash
curl -X GET "http://localhost:8000/api/v1/votes/user/my-votes" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 取消投票
```bash
curl -X DELETE "http://localhost:8000/api/v1/votes/item/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 協作場景

### 1. 旅遊目的地投票
```
1. 創建 "weekend_trip" 優先級清單
2. 添加多個目的地項目
3. 團隊成員各自投票
4. 查看投票結果決定目的地
```

### 2. 功能開發優先級
```
1. 產品經理創建功能清單
2. 團隊成員對功能重要性投票
3. 根據投票數排定開發優先級
4. 高票項目優先進入開發排程
```

### 3. 餐廳選擇
```
1. 創建聚餐餐廳選項清單
2. 朋友群組投票選擇
3. 即時查看投票進度
4. 決定最終餐廳
```

## 統計與分析

### 投票數據
- 總投票數
- 參與投票用戶數
- 投票分布情況
- 熱門項目排名

### 未來分析功能
- 用戶投票偏好分析
- 項目受歡迎程度趨勢
- 協作活躍度指標

## 未來改進

### 短期
- [ ] 實施清單存取權限檢查
- [ ] 添加投票時間戳顯示
- [ ] 支援投票排序

### 中期
- [ ] 投票權重系統
- [ ] 匿名投票選項
- [ ] 投票期限設定

### 長期
- [ ] 多輪投票機制
- [ ] 投票結果可視化
- [ ] 智能投票建議

## 相關文檔

- [ListItem API 實施詳情](list-item-api.md)
- [Event API 實施詳情](event-api.md)
- [ADR-002: 採用可擴展的多清單協作模型](../adr/002-adopt-extendable-multi-list-model.md)