# Backend Blob Directory

這個目錄包含開發過程中產生的臨時檔案和建構產物。

## 目錄結構

```
blob/
└── pytest/           # pytest 相關檔案
    ├── test.db       # 測試資料庫 (SQLite)
    └── .pytest_cache/ # pytest 快取檔案
```

## 說明

### pytest/
- **test.db**: 執行測試時自動生成的 SQLite 測試資料庫
- **.pytest_cache/**: pytest 的快取目錄，包含測試發現和執行的快取資料

## 注意事項

- 這個目錄中的所有檔案都在 `.gitignore` 中被忽略
- 檔案會在測試執行時自動生成
- 可以安全地刪除整個 `blob/` 目錄，下次測試時會重新生成
- 此目錄的目的是將所有臨時檔案集中管理，保持專案根目錄的整潔

## 清理

如果需要清理測試檔案：

```bash
# 刪除測試資料庫
rm -f blob/pytest/test.db

# 刪除 pytest 快取
rm -rf blob/pytest/.pytest_cache

# 或者刪除整個 blob 目錄
rm -rf blob/
```

下次執行 `uv run pytest` 時會重新生成所需的檔案。
