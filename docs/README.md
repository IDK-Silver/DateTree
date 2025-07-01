# DateTree 文檔中心

歡迎來到 DateTree 專案的文檔中心！這裡包含了專案的完整技術文檔。

## 📚 文檔結構

### 🏗️ 架構文檔 (`architecture/`)

- [資料模型架構](architecture/data-models.md) - 完整的資料庫模型說明
- [API 架構設計](architecture/api-design.md) - REST API 架構和設計原則

### 📋 架構決策記錄 (`adr/`)

- [ADR-001: 共享日曆協作模型](adr/001-shared-calendar-collaboration-model.md)
- [ADR-002: 採用擴展式多清單模型](adr/002-adopt-extendable-multi-list-model.md)
- [ADR-003: 資料庫遷移重置策略](adr/003-database-migration-reset-strategy.md)
- [ADR-004: 預設個人日曆設計](adr/004-default-personal-calendar.md)
- [ADR-005: 資料庫效能優化策略](adr/005-database-performance-optimization-strategy.md) ⭐ **New**

### 🔧 開發指南 (`guides/`)

- [開發環境設定](guides/development-setup.md) - 完整的開發環境設定指南
- [貢獻指南](guides/contributing.md) - 如何參與專案開發
- [資料庫管理](guides/database-management.md) - 資料庫操作和遷移指南

### 🧪 開發實務 (`development/`)

- [測試指南](development/testing-guide.md) - pytest 測試架構和最佳實踐
- [程式碼審查診斷](development/code-review-diagnosis.md) - 完整的程式碼品質分析報告
- [效能優化報告](development/performance-optimization-report.md) - 資料庫效能優化詳細分析
- [外鍵優化說明](development/foreign-key-optimization.md) - 外鍵索引問題與解決方案

### 🚀 功能實施 (`implementation/`)

- [List CRUD API](implementation/list-crud-api.md) - 清單 CRUD API 實施詳情

### 📖 API 參考 (`api/`)

- [REST API 規格](api/rest-api.md) - 完整的 API 端點參考
- [API 使用範例](api/examples.md) - 實際使用範例和最佳實踐

## 🎯 快速導航

### 新手開發者

1. 📖 [專案概覽](../README.md) - 了解專案願景和功能
2. 🔧 [開發環境設定](guides/development-setup.md) - 設定開發環境
3. 📋 [貢獻指南](guides/contributing.md) - 了解開發流程
4. 🧪 [測試指南](development/testing-guide.md) - 學習測試實踐

### 資深開發者

1. 🏗️ [架構文檔](architecture/) - 了解系統架構
2. 📋 [ADR 文檔](adr/) - 了解重要的架構決策
3. 🚀 [實施文檔](implementation/) - 查看功能實施細節
4. 📖 [API 參考](api/) - API 開發參考

### 專案管理者

1. 📊 [專案狀態](../README.md#7-專案開發狀態-development-status) - 查看最新進展
2. 🔄 [遷移指南](guides/database-management.md) - 了解資料庫變更影響
3. 📋 [架構決策](adr/) - 了解重要的技術決策

## 📝 文檔維護

- 📅 **更新頻率**: 每次功能發布後更新
- 👥 **維護責任**: 功能開發者負責相關文檔更新
- 🔄 **版本控制**: 所有文檔變更都需要通過 PR 審查

## 🚀 貢獻文檔

歡迎改進我們的文檔！請參閱 [貢獻指南](guides/contributing.md) 了解如何提交文檔改進。
