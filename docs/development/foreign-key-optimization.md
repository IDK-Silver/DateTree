# 外鍵效率優化建議

## 📈 立即改善方案

### 1. 新增外鍵索引

```python
# 在模型中新增索引
class List(Base):
    calendar_id = Column(Integer, ForeignKey("calendars.id"), nullable=False, index=True)

class ListItem(Base):
    list_id = Column(Integer, ForeignKey("lists.id"), nullable=False, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"), index=True)

class Vote(Base):
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    list_item_id = Column(Integer, ForeignKey("list_items.id"), nullable=False, index=True)

class Event(Base):
    calendar_id = Column(Integer, ForeignKey("calendars.id"), nullable=False, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"), index=True)
```

### 2. 創建複合索引

```python
# 投票去重索引
from sqlalchemy import Index

class Vote(Base):
    # ... 其他欄位
    
    __table_args__ = (
        Index('idx_vote_user_item', 'user_id', 'list_item_id', unique=True),
        Index('idx_vote_item', 'list_item_id'),  # 投票統計查詢
    )

class Event(Base):
    # ... 其他欄位
    
    __table_args__ = (
        Index('idx_event_calendar_time', 'calendar_id', 'start_time'),
    )
```

### 3. 優化查詢使用 eager loading

```python
# CRUD 層改善
def get_calendar_with_lists(self, db: Session, calendar_id: int):
    return (
        db.query(Calendar)
        .options(joinedload(Calendar.lists))  # 一次查詢載入
        .filter(Calendar.id == calendar_id)
        .first()
    )

def get_list_with_items_and_votes(self, db: Session, list_id: int):
    return (
        db.query(List)
        .options(
            joinedload(List.items).joinedload(ListItem.votes)
        )
        .filter(List.id == list_id)
        .first()
    )
```

## 📊 效能影響分析

### 改善前 vs 改善後

| 操作 | 改善前 | 改善後 | 改善比例 |
|------|--------|--------|----------|
| 獲取日曆清單 | 全表掃描 O(n) | 索引查找 O(log n) | 10-100x |
| 投票統計 | 多次JOIN無索引 | 索引JOIN | 5-20x |
| 權限檢查 | N+1查詢 | 單次JOIN查詢 | 2-10x |
| 事件查詢 | 全表掃描+排序 | 索引範圍查詢 | 20-100x |

### 記憶體使用

- **減少查詢次數**: 從 N+1 減少到 1-2 次查詢
- **減少網路延遲**: 批量載入相關數據
- **提高緩存效率**: 相關數據一起載入更容易緩存

## 🎯 實際應用場景

### 1. 日曆頁面載入
```python
# 改善前: 5-10 次查詢
calendar = get_calendar(1)
lists = get_lists_by_calendar(1)      # +1 查詢
for list_obj in lists:
    items = get_items_by_list(list_obj.id)  # +N 查詢

# 改善後: 1-2 次查詢
calendar = get_calendar_with_all_data(1)
```

### 2. 投票統計頁面
```python
# 改善前: 複雜的無索引JOIN
items_with_votes = slow_vote_count_query()  # 可能數秒

# 改善後: 索引優化JOIN
items_with_votes = fast_vote_count_query()  # 毫秒級
```

### 3. 權限檢查優化
```python
# 改善前: 每次API調用都檢查成員關係
def check_access():
    calendar = get_calendar()
    for member in calendar.members:  # 潛在的額外查詢
        if member.id == user_id:
            return True

# 改善後: 使用索引JOIN
def check_access():
    exists = db.query(calendar_user_association).filter(
        and_(calendar_id=cal_id, user_id=user_id)
    ).first()
    return exists is not None
```