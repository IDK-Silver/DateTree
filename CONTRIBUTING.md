# Contributing to DateTree

我們非常歡迎您為 DateTree 做出貢獻！感謝您投入時間。

## 行為準則 (Code of Conduct)

為了建立一個友善且富有成效的社群，我們期望所有貢獻者都能遵守我們的行為準則。請尊重每一位參與者，並保持建設性的溝通。

## 如何貢獻 (How to Contribute)

* **回報問題 (Reporting Bugs)**: 如果您發現了程式碼中的問題，請清楚地描述問題和重現步驟。
* **提出功能建議 (Suggesting Enhancements)**: 歡迎提出新功能的想法，請詳細說明該功能要解決的問題和建議的實現方式。
* **提交程式碼 (Pull Requests)**:
  1. 確保您的程式碼遵循專案的架構指南 (詳見 `backend/CONTRIBUTING.md` 或 `frontend/CONTRIBUTING.md`)。
  2. 為您的變更新增適當的測試。
  3. 確保您的提交訊息清晰明瞭。

## 開發指南

### 架構概覽

DateTree 採用擴展式多清單模型，核心概念包括：

* **使用者 (User)** 可以擁有多個 **日曆 (Calendar)**
* **日曆** 包含不同類型的 **清單 (List)**（待辦清單、優先級清單等）
* **清單** 包含多個 **清單項目 (ListItem)**
* **清單項目** 可以接受 **投票 (Vote)** 來支援團隊決策
* **事件 (Event)** 是已排程的確定項目

詳細的架構決策請參閱 [ADR 002](docs/adr/002-adopt-extendable-multi-list-model.md)。

### 具體開發指南

* 後端開發指南請參閱 `backend/README.md` 和 `backend/CONTRIBUTING.md`。
* (未來) 前端開發指南請參閱 `frontend/README.md` 和 `frontend/CONTRIBUTING.md`。

### 資料庫遷移注意事項

* 在開發階段，重大模型變更可能需要重置遷移歷史
* 生產環境中應始終使用漸進式遷移
* 詳細的遷移指南請參閱後端開發文檔