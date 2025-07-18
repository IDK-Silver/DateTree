### ADR 001: 採用共享日曆模型作為協作基礎

**文件狀態**: 已接受 (Accepted)
**決策日期**: 2025-06-28

#### 背景 (Context)

DateTree 的核心功能之一是支援多人協作，讓使用者可以共同規劃事件。我們需要選擇一種清晰、可擴展且符合產品「快速、方便」理念的協作模型。此決策將直接定義後端資料庫的核心結構，並影響未來所有與權限、分享相關的功能開發。

#### 決策驅動因素 (Decision Drivers)

* **使用者心智模型**: 選擇的方案應盡可能貼近使用者對「共享」的直覺理解，降低學習成本。
* **初始複雜度**: V1.0 的實現方式應相對簡單，避免過度設計，以便快速推出核心功能。
* **長期擴展性**: 方案應能支援未來更複雜的權限管理需求。
* **權限管理清晰度**: 權限邊界必須明確，易於在後端進行檢查，以確保資料安全。

#### 考量的選項 (Considered Options)

1. **共享單一事件 (Per-Event Sharing)**
    * **做法**: 每個事件預設為私有，使用者可以針對單一事件邀請協作者。
    * **優點**: 極度靈活，適合一次性的臨時共享。
    * **缺點**: 若需與同一群人共享大量事件，操作會非常繁瑣。權限管理的邏輯分散在每個事件上，較為複雜。

2. **群組/空間 (Groups/Spaces)**
    * **做法**: 使用者建立群組，在群組內建立的事件對所有成員可見。
    * **優點**: 適合目標導向的專案協作。
    * **缺點**: 對於非專案導向的簡單共享（如情侶共享日曆）來說，概念過重。

3. **共享日曆 (Shared Calendars) - (已選擇)**
    * **做法**: 事件歸屬於某個「日曆」。使用者可以建立不同的日曆，並將整個日曆分享給其他使用者。
    * **優點**:
        * **心智模型清晰**: 與 Google Calendar 等主流應用一致，使用者易於理解。
        * **權限集中**: 權限管理集中在「日曆」層級，後端邏輯清晰且安全。
        * **結構化**: 為事件提供了自然的分類容器。
        * **平衡性好**: 既能滿足個人私密需求（預設個人日曆），也能滿足團隊協作需求。
    * **缺點**: 相較於「共享單一事件」，在建立時多了一步「選擇日曆」的操作。但我們透過「快速新增預設歸屬個人日曆」的設計，彌補了這一點。

#### 決策 (Decision)

我們決定採用**「選項 3：共享日曆」**作為 DateTree 的核心協作模型。

每個使用者都會有一個預設的私有「個人日曆」。使用者可以建立新的日曆，並邀請其他成員加入，以此實現協作。每個事件都必須歸屬於一個日曆。

#### 後果 (Consequences)

* **正面**:
  * 我們的資料庫結構將非常清晰，易於理解和維護。
  * 權限檢查邏輯集中，可以建立一個可重複使用的、可靠的驗證層。
  * 為未來的功能擴展（如日曆顏色、進階權限等）打下了良好的基礎。

* **負面**:
  * 資料庫需要額外一個 `CalendarMembers` (或稱 `Shares`) 的關聯表來維護日曆與使用者之間的成員關係。

* **對開發的影響**:
  * 後端需要建立四個核心資料庫模型：`User`, `Calendar`, `Event`, 以及 `CalendarMember`。
  * 所有對 `Event` 的增、刪、改、查操作，都必須先驗證使用者對該 `Event` 所屬的 `Calendar` 是否擁有足夠的權限。

---

### 我的程式碼規劃

有了這份 ADR 作為指導，我對接下來的程式碼規劃如下：

1. **建立模型目錄**:
    * 我會在 `backend/app/` 下建立一個新的子資料夾 `models`。這個資料夾將專門用來存放我們所有的 SQLAlchemy 資料庫模型定義。
    * 這讓職責更加分離，`db` 資料夾負責資料庫連線與設定，`models` 資料夾負責資料表的結構定義。

2. **建立模型定義檔案**:
    * 在 `backend/app/models/` 資料夾中，我會建立一個 `__init__.py` 檔案。
    * 在專案初期，為了方便管理，我會將 `User`, `Calendar`, `Event`, `CalendarMember` 這四個核心模型類別 (Class) 全部定義在這個 `__init__.py` 檔案中。
    * 隨著專案變大，如果我們覺得有必要，未來可以輕易地將每個 Class 拆分到獨立的檔案中（如 `user.py`, `calendar.py` 等），再由 `__init__.py` 將它們匯入。

3. **模型程式碼的具體結構 (草圖)**:
    * **基礎引入**: 程式碼會先從 `..db.basic` 引入我們定義好的 `Base`。
    * **模型類別**:
        * **User**: 包含 `id`, `email`, `hashed_password` 等欄位。
        * **Calendar**: 包含 `id`, `name`, `owner_id` (外鍵關聯到 User) 等欄位。
        * **Event**: 包含 `id`, `title`, `content`, `start_time`, `end_time`, `status`, `calendar_id` (外鍵關聯到 Calendar) 等欄位。
        * **CalendarMember**: 這是一個「關聯表」，用來實現 `User` 和 `Calendar` 之間的多對多關係。它至少會包含 `user_id` 和 `calendar_id` 兩個外鍵，可能還有一個 `permission_level` 欄位。
    * **關聯性 (Relationships)**: 我會使用 SQLAlchemy 的 `relationship` 功能來定義模型之間的雙向關聯。例如，可以讓我們輕易地透過 `a_user.calendars` 來獲取某個使用者參與的所有日曆，或者透過 `a_calendar.events` 來獲取某個日曆下的所有事件。
