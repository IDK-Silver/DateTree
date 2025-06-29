# REST API 規格文檔

DateTree REST API 提供完整的清單和事件管理功能。

## 🚀 API 概覽

* **基礎 URL**: `http://localhost:8000/api/v1`
* **認證方式**: Bearer Token (計劃中)
* **資料格式**: JSON
* **API 版本**: v1

## 📋 API 端點

### Lists (清單管理)

#### 取得所有清單

```http
GET /api/v1/lists/
```

**回應範例**：

```json
[
  {
    "id": 1,
    "name": "我的待辦清單",
    "list_type": "TODO",
    "calendar_id": 1,
    "created_at": "2025-06-29T10:00:00Z"
  },
  {
    "id": 2,
    "name": "旅遊地點投票",
    "list_type": "PRIORITY",
    "calendar_id": 1,
    "created_at": "2025-06-29T11:00:00Z"
  }
]
```

#### 取得特定清單

```http
GET /api/v1/lists/{list_id}
```

**路徑參數**：
* `list_id` (integer) - 清單 ID

**回應範例**：

```json
{
  "id": 1,
  "name": "我的待辦清單",
  "list_type": "TODO",
  "calendar_id": 1,
  "created_at": "2025-06-29T10:00:00Z"
}
```

#### 取得日曆的清單

```http
GET /api/v1/lists/calendar/{calendar_id}
```

**路徑參數**：
* `calendar_id` (integer) - 日曆 ID

#### 建立新清單

```http
POST /api/v1/lists/
```

**請求主體**：

```json
{
  "name": "新的清單",
  "list_type": "TODO",
  "calendar_id": 1
}
```

**回應**：

```json
{
  "id": 3,
  "name": "新的清單",
  "list_type": "TODO",
  "calendar_id": 1,
  "created_at": "2025-06-29T12:00:00Z"
}
```

#### 更新清單

```http
PUT /api/v1/lists/{list_id}
```

**路徑參數**：
* `list_id` (integer) - 清單 ID

**請求主體**：

```json
{
  "name": "更新後的清單名稱",
  "list_type": "PRIORITY"
}
```

#### 刪除清單

```http
DELETE /api/v1/lists/{list_id}
```

**回應**：`204 No Content`

### 清單類型

目前支援的清單類型：

* `TODO` - 一般待辦清單
* `PRIORITY` - 優先級投票清單

## 🔒 認證與授權

### 認證方式 (計劃中)

API 將使用 JWT Bearer Token 進行認證：

```http
Authorization: Bearer <your-jwt-token>
```

### 權限控制

* 使用者只能存取自己有權限的日曆
* 清單的建立、修改、刪除需要對應的日曆權限

## 📊 狀態碼

### 成功回應

* `200 OK` - 成功取得資料
* `201 Created` - 成功建立資源
* `204 No Content` - 成功刪除資源

### 錯誤回應

* `400 Bad Request` - 請求格式錯誤
* `401 Unauthorized` - 認證失敗
* `403 Forbidden` - 權限不足
* `404 Not Found` - 資源不存在
* `422 Unprocessable Entity` - 資料驗證失敗
* `500 Internal Server Error` - 伺服器內部錯誤

### 錯誤格式

```json
{
  "detail": "錯誤描述",
  "error_code": "VALIDATION_ERROR",
  "field_errors": {
    "name": ["此欄位為必填項目"]
  }
}
```

## 🔄 分頁

大量資料的端點支援分頁：

```http
GET /api/v1/lists/?page=1&size=20
```

**查詢參數**：
* `page` (integer) - 頁碼，預設為 1
* `size` (integer) - 每頁筆數，預設為 20，最大 100

**分頁回應格式**：

```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 20,
  "pages": 5
}
```

## 🔍 過濾與搜尋

### 過濾

```http
GET /api/v1/lists/?list_type=TODO&calendar_id=1
```

### 搜尋

```http
GET /api/v1/lists/?search=待辦
```

### 排序

```http
GET /api/v1/lists/?sort=created_at&order=desc
```

## 📱 API 使用範例

### JavaScript (Fetch API)

```javascript
// 建立新清單
async function createList(listData) {
  try {
    const response = await fetch('/api/v1/lists/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(listData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const newList = await response.json();
    return newList;
  } catch (error) {
    console.error('建立清單失敗:', error);
    throw error;
  }
}

// 取得清單
async function getLists() {
  try {
    const response = await fetch('/api/v1/lists/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    const lists = await response.json();
    return lists;
  } catch (error) {
    console.error('取得清單失敗:', error);
    throw error;
  }
}
```

### Python (requests)

```python
import requests

API_BASE_URL = "http://localhost:8000/api/v1"
TOKEN = "your-jwt-token"

def create_list(list_data):
    """建立新清單"""
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        f"{API_BASE_URL}/lists/",
        json=list_data,
        headers=headers
    )
    
    response.raise_for_status()
    return response.json()

def get_lists():
    """取得所有清單"""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    response = requests.get(
        f"{API_BASE_URL}/lists/",
        headers=headers
    )
    
    response.raise_for_status()
    return response.json()

# 使用範例
if __name__ == "__main__":
    # 建立清單
    new_list = create_list({
        "name": "我的待辦清單",
        "list_type": "TODO",
        "calendar_id": 1
    })
    print(f"建立清單: {new_list}")
    
    # 取得清單
    lists = get_lists()
    print(f"清單數量: {len(lists)}")
```

### cURL

```bash
# 建立清單
curl -X POST "http://localhost:8000/api/v1/lists/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "我的待辦清單",
    "list_type": "TODO",
    "calendar_id": 1
  }'

# 取得清單
curl -X GET "http://localhost:8000/api/v1/lists/" \
  -H "Authorization: Bearer $TOKEN"

# 更新清單
curl -X PUT "http://localhost:8000/api/v1/lists/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "更新後的清單名稱"
  }'

# 刪除清單
curl -X DELETE "http://localhost:8000/api/v1/lists/1" \
  -H "Authorization: Bearer $TOKEN"
```

## 🧪 測試 API

### 使用 Swagger UI

1. 啟動開發伺服器：
   ```bash
   cd backend
   uv run uvicorn app.main:app --reload
   ```

2. 開啟 Swagger UI：<http://localhost:8000/docs>

3. 在 Swagger UI 中測試各個端點

### 使用 Thunder Client (VS Code)

1. 安裝 Thunder Client 擴展
2. 建立新的 Collection
3. 添加各個 API 端點
4. 設定認證 Header

### 使用 Postman

1. 匯入 OpenAPI 規格：<http://localhost:8000/openapi.json>
2. 設定環境變數（base_url, token）
3. 測試各個端點

## 📚 相關文檔

* [OpenAPI 規格](http://localhost:8000/openapi.json)
* [Swagger UI](http://localhost:8000/docs)
* [ReDoc](http://localhost:8000/redoc)
* [API 使用範例](examples.md)
* [認證指南](../guides/authentication.md) (計劃中)
