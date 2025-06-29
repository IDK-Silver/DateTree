# 貢獻指南

歡迎參與 DateTree 專案的開發！本指南將幫助您了解如何有效地為專案做出貢獻。

## 🎯 開發流程

### 1. 準備開發環境

在開始貢獻之前，請確保您已經設定好開發環境：

1. **複製專案倉庫**：
   ```bash
   git clone https://github.com/your-org/DateTree.git
   cd DateTree
   ```

2. **設定開發環境**：
   參閱 [開發環境設定指南](development-setup.md) 進行完整設定。

3. **驗證環境**：
   ```bash
   cd backend
   uv run pytest  # 確保所有測試通過
   uv run uvicorn app.main:app --reload  # 確保服務器正常啟動
   ```

### 2. 選擇工作項目

* **新手貢獻者**：從 Issues 中尋找標記為 `good-first-issue` 的項目
* **資深開發者**：可以選擇 `help-wanted` 或自主提出新功能
* **文檔貢獻**：改進現有文檔或創建新的使用指南

### 3. 建立分支

```bash
# 從 main 分支建立新的功能分支
git checkout main
git pull origin main
git checkout -b feature/your-feature-name

# 例如：
git checkout -b feature/user-authentication
git checkout -b fix/database-connection-issue
git checkout -b docs/api-examples
```

## 📋 開發標準

### 程式碼風格

#### Python (後端)

* **遵循 PEP 8**：使用標準的 Python 程式碼風格
* **型別提示**：所有函式都應該包含型別提示
* **文檔字串**：重要函式需要包含 docstring

```python
from typing import Optional, List
from pydantic import BaseModel

def create_list(
    db: Session, 
    list_data: ListCreate, 
    current_user: User
) -> List:
    """
    創建新的清單
    
    Args:
        db: 資料庫會話
        list_data: 清單創建資料
        current_user: 當前使用者
        
    Returns:
        創建的清單物件
        
    Raises:
        HTTPException: 如果日曆不存在或無權限
    """
    # 實作內容...
```

* **錯誤處理**：適當處理異常並提供有意義的錯誤訊息
* **日誌記錄**：重要操作應該包含適當的日誌

#### 前端 (未來)

* 遵循 ESLint 和 Prettier 配置
* 使用 TypeScript 進行型別檢查
* 遵循 React/Vue.js 最佳實踐

### 測試要求

#### 新功能開發

所有新功能都必須包含對應的測試：

```python
# tests/test_new_feature.py
import pytest
from fastapi.testclient import TestClient

def test_create_list_success(client: TestClient, test_user, test_calendar):
    """測試成功創建清單"""
    response = client.post(
        "/api/v1/lists/",
        json={
            "name": "Test List",
            "list_type": "TODO",
            "calendar_id": test_calendar.id
        },
        headers={"Authorization": f"Bearer {test_user.token}"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test List"

def test_create_list_invalid_calendar(client: TestClient, test_user):
    """測試使用無效日曆ID創建清單"""
    response = client.post(
        "/api/v1/lists/",
        json={
            "name": "Test List",
            "list_type": "TODO", 
            "calendar_id": 99999  # 不存在的日曆
        },
        headers={"Authorization": f"Bearer {test_user.token}"}
    )
    assert response.status_code == 404
```

#### 測試分類

* **單元測試**：測試個別函式和方法
* **整合測試**：測試 API 端點和資料庫操作
* **功能測試**：測試完整的業務流程

#### 測試覆蓋率

* 目標覆蓋率：80% 以上
* 執行測試：`uv run pytest --cov=app tests/`
* 查看報告：`uv run pytest --cov=app --cov-report=html tests/`

### Git 提交規範

使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

```bash
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### 提交類型

* `feat`: 新功能
* `fix`: 錯誤修復
* `docs`: 文檔變更
* `style`: 程式碼格式變更（不影響功能）
* `refactor`: 程式碼重構
* `test`: 測試相關變更
* `chore`: 建置工具或輔助工具變更

#### 提交範例

```bash
# 新功能
git commit -m "feat(api): add user authentication endpoints"

# 錯誤修復
git commit -m "fix(database): resolve connection pool exhaustion"

# 文檔更新
git commit -m "docs(api): add authentication examples"

# 測試
git commit -m "test(lists): add comprehensive CRUD tests"

# 重構
git commit -m "refactor(models): extract common base model"
```

## 🔍 程式碼審查

### 提交 Pull Request

1. **確保測試通過**：
   ```bash
   uv run pytest
   ```

2. **檢查程式碼品質** (如果配置了)：
   ```bash
   uv run ruff check .
   uv run ruff format .
   ```

3. **建立 Pull Request**：
   * 使用清晰的標題描述變更
   * 在描述中說明變更的原因和影響
   * 連結到相關的 Issue

4. **Pull Request 模板**：
   ```markdown
   ## 變更描述
   
   簡要描述這個 PR 解決了什麼問題或新增了什麼功能。
   
   ## 變更類型
   
   - [ ] 錯誤修復 (非破壞性變更，修復了問題)
   - [ ] 新功能 (非破壞性變更，新增了功能)
   - [ ] 破壞性變更 (修復或功能會導致現有功能無法正常運作)
   - [ ] 文檔更新
   
   ## 測試
   
   - [ ] 已執行現有測試套件
   - [ ] 已新增新功能的測試
   - [ ] 所有測試都通過
   
   ## 檢查清單
   
   - [ ] 程式碼遵循專案的程式碼風格
   - [ ] 已進行自我審查
   - [ ] 程式碼有適當的註解
   - [ ] 相應的文檔已更新
   ```

### 審查標準

#### 功能性
* 程式碼是否正確實現了需求？
* 是否處理了邊界情況和錯誤情況？
* 性能是否可接受？

#### 程式碼品質
* 程式碼是否清晰易讀？
* 是否遵循了專案的程式碼風格？
* 是否有適當的註解和文檔？

#### 測試
* 是否包含了足夠的測試？
* 測試是否涵蓋了主要功能和邊界情況？
* 所有測試是否都通過？

## 🏗️ 架構貢獻

### 新功能設計

在實施重大新功能前，請考慮：

1. **創建 ADR (Architecture Decision Record)**：
   參考 `docs/adr/` 中的現有 ADR 格式

2. **討論設計**：
   在 GitHub Issues 或 Discussions 中提出設計方案

3. **考慮向後相容性**：
   確保變更不會破壞現有 API

### 資料庫變更

* **使用 Alembic 遷移**：所有資料庫變更都必須通過遷移腳本
* **測試遷移**：確保遷移可以正確執行和回滾
* **文檔化影響**：在 PR 中說明對現有資料的影響

```bash
# 創建新遷移
uv run alembic revision --autogenerate -m "add user preferences table"

# 測試遷移
uv run alembic upgrade head
uv run alembic downgrade -1
```

## 📚 文檔貢獻

### 文檔類型

* **API 文檔**：使用 FastAPI 自動生成的文檔
* **使用指南**：在 `docs/guides/` 中添加使用者指南
* **開發文檔**：在 `docs/development/` 中添加開發相關文檔
* **架構文檔**：在 `docs/architecture/` 中記錄系統設計

### 文檔標準

* 使用清晰、簡潔的語言
* 包含實際的程式碼範例
* 保持文檔與程式碼同步更新
* 使用適當的 Markdown 格式

## 🎉 認可與感謝

### 貢獻者認可

* 所有貢獻者都會在 README.md 中得到認可
* 重大貢獻會在 GitHub Releases 中特別提及
* 活躍貢獻者可能會被邀請成為專案維護者

### 社群參與

* 參與 GitHub Discussions 討論
* 幫助回答其他使用者的問題
* 分享使用經驗和最佳實踐

## 💬 獲得幫助

* **技術問題**：在 GitHub Issues 中提出
* **設計討論**：使用 GitHub Discussions
* **即時交流**：(未來可能建立 Discord 或 Slack)

感謝您對 DateTree 專案的貢獻！🚀
