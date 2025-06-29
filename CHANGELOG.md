# DateTree 架構重構變更日志

**日期**: 2025-06-29  
**版本**: v1.1  
**類型**: 重大架構重構

## 變更概述

完成了從簡單的 Calendar-Event 架構到擴展式多清單模型（Calendar-List-ListItem-Vote-Event）的重大重構。

## 已完成的工作

### 1. 資料模型重構

**新增的模型文件**：
- `backend/app/models/base.py` - 基礎模型和共用功能
- `backend/app/models/user.py` - 使用者模型
- `backend/app/models/calendar.py` - 日曆模型和使用者關聯表
- `backend/app/models/list.py` - 清單模型和清單類型枚舉
- `backend/app/models/list_item.py` - 清單項目模型
- `backend/app/models/vote.py` - 投票模型（支援協作決策）
- `backend/app/models/event.py` - 重新設計的事件模型
- `backend/app/models/__init__.py` - 模型匯入配置

**移除的文件**：
- `backend/app/models/enums.py` - 舊的枚舉定義

### 2. 資料庫遷移重置

**執行的步驟**：
- 刪除所有舊的 Alembic 遷移檔案
- 更新 `backend/alembic/env.py` 以正確匯入新模型
- 產生新的初始遷移，完整反映新的資料結構
- 成功套用新遷移到資料庫

**建立的資料表**：
- `users` - 使用者基本資訊
- `calendars` - 日曆容器
- `calendar_user_association` - 使用者與日曆的多對多關聯
- `lists` - 各類型清單（待辦、優先級等）
- `list_items` - 清單中的具體項目
- `votes` - 投票記錄
- `events` - 已排程的確定事件

### 3. 開發環境修復

**修復的問題**：
- 修復損壞的 `uv.lock` 檔案
- 確保所有必要依賴正確安裝
- 修正 VS Code 除錯配置（`.vscode/launch.json`）
- 驗證 FastAPI 應用程式可正常啟動

### 4. 文檔全面更新

**更新的文檔**：

#### 後端文檔
- `backend/README.md`: 
  - 新增資料架構概覽
  - 詳細的遷移重置指南
  - 擴展的故障排除章節
- `backend/CONTRIBUTING.md`:
  - 模組化模型架構說明
  - 資料庫遷移最佳實踐
  - 模型變更檢查清單

#### 專案根目錄文檔
- `README.md`:
  - 更新核心功能說明，反映新的多清單架構
  - 修改使用者流程範例，展示協作投票功能
  - 新增技術架構中的資料模型說明
- `CONTRIBUTING.md`:
  - 新增架構概覽章節
  - 資料庫遷移注意事項

#### 架構決策記錄 (ADR)
- `docs/adr/002-adopt-extendable-multi-list-model.md`:
  - 更新狀態為「已實施」
  - 新增實際實施章節
  - 記錄遷移重置的決策過程
- `docs/adr/003-database-migration-reset-strategy.md` (新建):
  - 詳細記錄遷移重置的決策理由
  - 開發 vs 生產環境的不同策略
  - 未來的最佳實踐指導

## 新架構的核心特色

### 1. 擴展性
- 支援多種清單類型（待辦、優先級、未來可擴展更多）
- 模組化的模型設計，易於新增功能

### 2. 協作功能
- 多使用者日曆共享
- 投票機制支援團隊決策
- 清單項目到事件的轉換流程

### 3. 可維護性
- 每個模型都有獨立的檔案
- 清晰的職責分離
- 完整的文檔和指導

## 開發者行動項目

如果您是開發團隊的成員，請執行以下步驟來更新您的開發環境：

1. **拉取最新程式碼**：
   ```bash
   git pull origin main
   ```

2. **重建開發環境**：
   ```bash
   cd backend
   uv sync
   ```

3. **重置資料庫**：
   ```bash
   # 如果使用 Docker
   docker-compose down -v
   docker-compose up -d
   
   # 或直接重建資料庫
   dropdb your_database_name
   createdb your_database_name
   ```

4. **套用新遷移**：
   ```bash
   uv run alembic upgrade head
   ```

5. **驗證環境**：
   ```bash
   uv run uvicorn app.main:app --reload
   ```

## 影響分析

### 正面影響
- 🎯 **架構更清晰**：新模型更好地反映了業務需求
- 🔧 **更易維護**：模組化設計降低了維護成本
- 🚀 **支援擴展**：為未來功能奠定了堅實基礎
- 👥 **協作友善**：內建的投票和共享機制

### 注意事項
- ⚠️ **開發中斷**：需要所有開發者重建環境
- 📚 **學習成本**：開發團隊需要了解新的模型結構
- 🔄 **工作流程變化**：未來的資料庫變更需要遵循新的最佳實踐

## 後續計劃

1. **API 開發**：基於新模型實現 REST API 端點
2. **前端適配**：調整前端以支援新的資料結構
3. **測試編寫**：為新模型編寫完整的測試套件
4. **性能優化**：針對複雜查詢進行優化
5. **文檔完善**：繼續完善 API 文檔和使用指南
