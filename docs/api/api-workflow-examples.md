# API 工作流程範例

這個文檔提供 DateTree API 的實際使用範例，展示不同類型的工作流程和 API 之間的關聯關係。

## 🎯 核心概念

### 資料層次結構
```
User (用戶)
└── Calendar (日曆) [1:N]
    ├── List (清單) [1:N]
    │   └── ListItem (清單項目) [1:N]
    │       └── Vote (投票) [1:N]
    └── Event (事件) [1:N]
```

### API 關聯邏輯
1. **認證流程**: 用戶註冊 → 登入 → 取得 JWT Token
2. **日曆管理**: 註冊時自動建立個人日曆，可手動建立專案日曆
3. **清單系統**: 在日曆內建立不同類型的清單 (TODO/PRIORITY)
4. **協作投票**: PRIORITY 清單支援團隊投票決策
5. **事件管理**: 在日曆內建立時程安排

## 📝 完整工作流程範例

### 範例 1: 個人任務管理

適用場景：個人日常任務追蹤和時間管理

```http
# === 第一步：用戶設置 ===

# 1.1 註冊新用戶
POST /api/v1/users/register
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "password": "mySecurePassword123"
}

# 回應 (200 OK):
{
  "id": 1,
  "email": "john.doe@example.com",
  "is_active": true
}
# 注意：系統自動建立 "john.doe@example.com's Personal Calendar"

# 1.2 用戶登入
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "password": "mySecurePassword123"
}

# 回應 (200 OK):
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}

# === 第二步：查看可用日曆 ===

# 2.1 取得我的日曆列表
GET /api/v1/calendars/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

# 回應 (200 OK):
[
  {
    "id": 1,
    "name": "john.doe@example.com's Personal Calendar",
    "description": "Personal calendar",
    "calendar_type": "PERSONAL",
    "owner_id": 1
  }
]

# === 第三步：建立任務清單 ===

# 3.1 建立每日待辦清單
POST /api/v1/lists/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "name": "今日待辦事項",
  "list_type": "TODO",
  "calendar_id": 1
}

# 回應 (200 OK):
{
  "id": 1,
  "name": "今日待辦事項",
  "list_type": "TODO",
  "calendar_id": 1,
  "created_at": "2025-07-01T09:00:00Z"
}

# 3.2 建立本週目標清單
POST /api/v1/lists/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "name": "本週重要目標",
  "list_type": "PRIORITY",
  "calendar_id": 1
}

# 回應 (200 OK):
{
  "id": 2,
  "name": "本週重要目標",
  "list_type": "PRIORITY", 
  "calendar_id": 1,
  "created_at": "2025-07-01T09:05:00Z"
}

# === 第四步：添加任務項目 ===

# 4.1 添加日常任務
POST /api/v1/list-items/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "content": "回覆重要郵件",
  "list_id": 1
}

POST /api/v1/list-items/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "content": "準備明天的會議資料",
  "list_id": 1
}

POST /api/v1/list-items/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "content": "健身房運動 1 小時",
  "list_id": 1
}

# 4.2 添加週目標
POST /api/v1/list-items/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "content": "完成專案第一階段",
  "list_id": 2
}

POST /api/v1/list-items/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "content": "學習新技術框架",
  "list_id": 2
}

# === 第五步：任務優先級投票（自我管理）===

# 5.1 為重要目標投票（設定優先級）
POST /api/v1/votes/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "list_item_id": 4  # 完成專案第一階段
}

# === 第六步：建立相關事件 ===

# 6.1 建立會議事件
POST /api/v1/events/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "title": "專案進度會議",
  "description": "討論第一階段進度和下階段規劃",
  "start_time": "2025-07-02T10:00:00Z",
  "end_time": "2025-07-02T11:30:00Z",
  "calendar_id": 1
}

# 6.2 建立健身提醒
POST /api/v1/events/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "title": "健身房運動",
  "description": "重訓 + 有氧運動",
  "start_time": "2025-07-01T18:00:00Z",
  "end_time": "2025-07-01T19:00:00Z",
  "calendar_id": 1
}

# === 第七步：追蹤進度 ===

# 7.1 完成任務
PUT /api/v1/list-items/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "is_completed": true
}

# 7.2 查看今日任務進度
GET /api/v1/list-items/list/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

# 7.3 查看週目標投票結果
GET /api/v1/list-items/list/2/with-votes
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

# 7.4 查看今日行程
GET /api/v1/events/calendar/1/date-range?start_date=2025-07-01T00:00:00Z&end_date=2025-07-01T23:59:59Z
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### 範例 2: 團隊專案協作

適用場景：多人協作的專案管理和決策

```http
# === 團隊領導設置專案 ===

# 1.1 專案經理建立專案日曆
POST /api/v1/calendars/
Authorization: Bearer <pm_token>
Content-Type: application/json

{
  "name": "新產品開發專案",
  "description": "2025年第二季新產品開發計畫"
}

# 回應: calendar_id = 5

# 1.2 建立功能需求投票清單
POST /api/v1/lists/
Authorization: Bearer <pm_token>
Content-Type: application/json

{
  "name": "產品功能優先級投票",
  "list_type": "PRIORITY",
  "calendar_id": 5
}

# 回應: list_id = 10

# 1.3 建立開發任務清單
POST /api/v1/lists/
Authorization: Bearer <pm_token>
Content-Type: application/json

{
  "name": "開發任務追蹤",
  "list_type": "TODO",
  "calendar_id": 5
}

# 回應: list_id = 11

# === 團隊成員提出功能建議 ===

# 2.1 前端開發者建議
POST /api/v1/list-items/
Authorization: Bearer <frontend_dev_token>
Content-Type: application/json

{
  "content": "響應式設計支援",
  "list_id": 10
}

# 2.2 後端開發者建議
POST /api/v1/list-items/
Authorization: Bearer <backend_dev_token>
Content-Type: application/json

{
  "content": "API 效能優化",
  "list_id": 10
}

# 2.3 UX 設計師建議
POST /api/v1/list-items/
Authorization: Bearer <ux_designer_token>
Content-Type: application/json

{
  "content": "用戶體驗流程改善",
  "list_id": 10
}

# 2.4 產品經理建議
POST /api/v1/list-items/
Authorization: Bearer <pm_token>
Content-Type: application/json

{
  "content": "多語言支援",
  "list_id": 10
}

# === 全團隊投票決定優先級 ===

# 3.1 前端開發者投票
POST /api/v1/votes/
Authorization: Bearer <frontend_dev_token>
Content-Type: application/json

{
  "list_item_id": 15  # 響應式設計支援
}

POST /api/v1/votes/
Authorization: Bearer <frontend_dev_token>
Content-Type: application/json

{
  "list_item_id": 17  # 用戶體驗流程改善
}

# 3.2 後端開發者投票
POST /api/v1/votes/
Authorization: Bearer <backend_dev_token>
Content-Type: application/json

{
  "list_item_id": 16  # API 效能優化
}

POST /api/v1/votes/
Authorization: Bearer <backend_dev_token>
Content-Type: application/json

{
  "list_item_id": 15  # 響應式設計支援
}

# 3.3 UX 設計師投票
POST /api/v1/votes/
Authorization: Bearer <ux_designer_token>
Content-Type: application/json

{
  "list_item_id": 17  # 用戶體驗流程改善
}

POST /api/v1/votes/
Authorization: Bearer <ux_designer_token>
Content-Type: application/json

{
  "list_item_id": 18  # 多語言支援
}

# 3.4 產品經理投票
POST /api/v1/votes/
Authorization: Bearer <pm_token>
Content-Type: application/json

{
  "list_item_id": 17  # 用戶體驗流程改善
}

POST /api/v1/votes/
Authorization: Bearer <pm_token>
Content-Type: application/json

{
  "list_item_id": 15  # 響應式設計支援
}

# === 查看投票結果並制定計畫 ===

# 4.1 檢視投票結果
GET /api/v1/list-items/list/10/with-votes
Authorization: Bearer <pm_token>

# 預期回應:
[
  {
    "id": 15,
    "content": "響應式設計支援",
    "vote_count": 3,
    "list_id": 10,
    "creator_id": 2
  },
  {
    "id": 17,
    "content": "用戶體驗流程改善", 
    "vote_count": 3,
    "list_id": 10,
    "creator_id": 4
  },
  {
    "id": 16,
    "content": "API 效能優化",
    "vote_count": 1,
    "list_id": 10,
    "creator_id": 3
  },
  {
    "id": 18,
    "content": "多語言支援",
    "vote_count": 1,
    "list_id": 10,
    "creator_id": 1
  }
]

# 結果分析：響應式設計和UX改善並列第一優先級

# === 根據投票結果建立開發任務 ===

# 5.1 建立第一優先級任務
POST /api/v1/list-items/
Authorization: Bearer <pm_token>
Content-Type: application/json

{
  "content": "設計響應式佈局架構",
  "list_id": 11
}

POST /api/v1/list-items/
Authorization: Bearer <pm_token>
Content-Type: application/json

{
  "content": "進行用戶體驗研究",
  "list_id": 11
}

POST /api/v1/list-items/
Authorization: Bearer <pm_token>
Content-Type: application/json

{
  "content": "建立新的使用者流程圖",
  "list_id": 11
}

# === 規劃開發時程 ===

# 6.1 建立專案啟動會議
POST /api/v1/events/
Authorization: Bearer <pm_token>
Content-Type: application/json

{
  "title": "新產品開發啟動會議",
  "description": "討論優先級投票結果和開發計畫",
  "start_time": "2025-07-03T09:00:00Z",
  "end_time": "2025-07-03T10:30:00Z",
  "calendar_id": 5
}

# 6.2 建立設計衝刺週期
POST /api/v1/events/
Authorization: Bearer <pm_token>
Content-Type: application/json

{
  "title": "UX設計衝刺第一週",
  "description": "用戶體驗研究和流程設計",
  "start_time": "2025-07-07T09:00:00Z",
  "end_time": "2025-07-11T17:00:00Z",
  "calendar_id": 5
}

# 6.3 建立開發衝刺週期
POST /api/v1/events/
Authorization: Bearer <pm_token>
Content-Type: application/json

{
  "title": "響應式設計開發衝刺",
  "description": "前端響應式佈局實作",
  "start_time": "2025-07-14T09:00:00Z",
  "end_time": "2025-07-18T17:00:00Z",
  "calendar_id": 5
}

# === 追蹤專案進度 ===

# 7.1 開發者更新任務狀態
PUT /api/v1/list-items/19
Authorization: Bearer <ux_designer_token>
Content-Type: application/json

{
  "content": "進行用戶體驗研究 - 已完成初步調查",
  "is_completed": true
}

# 7.2 查看專案整體進度
GET /api/v1/lists/calendar/5
Authorization: Bearer <pm_token>

# 7.3 查看本週開發行程
GET /api/v1/events/calendar/5/upcoming
Authorization: Bearer <pm_token>

# 7.4 查看團隊投票記錄
GET /api/v1/votes/user/my-votes
Authorization: Bearer <frontend_dev_token>
```

### 範例 3: 活動規劃與協調

適用場景：團隊活動、會議或聚會的規劃

```http
# === 活動負責人初始設置 ===

# 1.1 建立活動專用日曆
POST /api/v1/calendars/
Authorization: Bearer <organizer_token>
Content-Type: application/json

{
  "name": "公司春季團建活動",
  "description": "2025年春季團隊建設活動規劃"
}

# 回應: calendar_id = 8

# 1.2 建立活動地點投票清單
POST /api/v1/lists/
Authorization: Bearer <organizer_token>
Content-Type: application/json

{
  "name": "團建地點投票",
  "list_type": "PRIORITY",
  "calendar_id": 8
}

# 1.3 建立活動準備事項清單
POST /api/v1/lists/
Authorization: Bearer <organizer_token>
Content-Type: application/json

{
  "name": "活動準備清單",
  "list_type": "TODO",
  "calendar_id": 8
}

# === 收集地點建議 ===

# 2.1 各團隊提出建議
POST /api/v1/list-items/
Authorization: Bearer <team_a_token>
{
  "content": "陽明山國家公園 - 自然健行",
  "list_id": 15
}

POST /api/v1/list-items/
Authorization: Bearer <team_b_token>
{
  "content": "淡水漁人碼頭 - 海景休閒",
  "list_id": 15
}

POST /api/v1/list-items/
Authorization: Bearer <team_c_token>
{
  "content": "北投溫泉區 - 溫泉體驗",
  "list_id": 15
}

# === 全員投票選擇地點 ===

# 3.1 各員工進行投票（示例部分投票）
POST /api/v1/votes/
Authorization: Bearer <employee_1_token>
{
  "list_item_id": 25  # 陽明山
}

POST /api/v1/votes/
Authorization: Bearer <employee_2_token>
{
  "list_item_id": 27  # 北投溫泉
}

# ... 更多投票 ...

# 3.2 查看投票進展
GET /api/v1/list-items/list/15/with-votes
Authorization: Bearer <organizer_token>

# === 根據投票結果規劃活動 ===

# 4.1 查看最終投票結果
GET /api/v1/list-items/list/15/with-votes
Authorization: Bearer <organizer_token>

# 假設北投溫泉獲勝，建立確定的活動事件

# 4.2 建立主要活動事件
POST /api/v1/events/
Authorization: Bearer <organizer_token>
Content-Type: application/json

{
  "title": "春季團建 - 北投溫泉之旅",
  "description": "公司全員北投溫泉團建活動",
  "start_time": "2025-04-20T09:00:00Z",
  "end_time": "2025-04-20T17:00:00Z",
  "calendar_id": 8
}

# 4.3 建立集合時間
POST /api/v1/events/
Authorization: Bearer <organizer_token>
Content-Type: application/json

{
  "title": "團建集合",
  "description": "公司樓下集合出發",
  "start_time": "2025-04-20T08:30:00Z",
  "end_time": "2025-04-20T09:00:00Z",
  "calendar_id": 8
}

# === 建立準備事項 ===

# 5.1 添加各項準備工作
POST /api/v1/list-items/
Authorization: Bearer <organizer_token>
{
  "content": "預訂溫泉會館",
  "list_id": 16
}

POST /api/v1/list-items/
Authorization: Bearer <organizer_token>
{
  "content": "安排交通車輛",
  "list_id": 16
}

POST /api/v1/list-items/
Authorization: Bearer <organizer_token>
{
  "content": "準備活動物資",
  "list_id": 16
}

POST /api/v1/list-items/
Authorization: Bearer <organizer_token>
{
  "content": "確認參與人數",
  "list_id": 16
}

# === 執行階段追蹤 ===

# 6.1 逐步完成準備工作
PUT /api/v1/list-items/28
Authorization: Bearer <organizer_token>
{
  "content": "預訂溫泉會館 - 已確認30人場地",
  "is_completed": true
}

# 6.2 查看準備進度
GET /api/v1/list-items/list/16
Authorization: Bearer <organizer_token>

# 6.3 查看活動完整時程
GET /api/v1/events/calendar/8/date-range?start_date=2025-04-20T00:00:00Z&end_date=2025-04-20T23:59:59Z
Authorization: Bearer <organizer_token>
```

## 🔄 API 調用模式總結

### 標準工作流程模式

1. **初始化階段**
   ```
   用戶註冊 → 登入取得Token → 建立/查看日曆
   ```

2. **規劃階段**  
   ```
   建立清單 → 添加項目 → (可選)建立相關事件
   ```

3. **協作階段** (PRIORITY清單)
   ```
   團隊添加建議 → 投票決策 → 查看結果
   ```

4. **執行階段**
   ```
   更新任務狀態 → 追蹤進度 → 調整計畫
   ```

5. **檢視階段**
   ```
   查看清單進度 → 檢視行程安排 → 分析投票結果
   ```

### API 相依性地圖

```
認證 API → 日曆 API → 清單 API → 清單項目 API
                                        ↓
事件 API ←──────────────────────── 投票 API
```

### 最佳實踐建議

1. **認證管理**: 始終檢查 Token 有效性，適時更新
2. **錯誤處理**: 妥善處理各種 HTTP 狀態碼
3. **資料一致性**: 遵循上下層資源的關聯規則
4. **使用者體驗**: 提供即時的進度反饋和狀態更新
5. **權限控制**: 確保用戶只能存取有權限的資源

這些範例展示了 DateTree API 的完整使用模式，可以根據具體需求調整和組合使用。