# ADR-008: Flutter Frontend API Integration and Data Model Alignment

**Status**: ✅ Implemented
**Date**: 2025-07-03
**Decision Makers**: Development Team

## Context and Problem Statement

The initial Flutter frontend implementation used hardcoded calendar categories and had misaligned data models with the backend API. This caused several issues:

1. **Hardcoded Categories**: The frontend had fixed categories `['Personal', 'Lover', 'Friends', 'Work']` instead of dynamic calendar management
2. **API Endpoint Mismatches**: Flutter API client endpoints didn't match the backend implementation
3. **Data Model Inconsistencies**: Field names and types didn't align between Flutter models and backend schemas
4. **HTTP 307 Redirect Issues**: Missing trailing slashes on POST endpoints caused redirect errors

## Decision Drivers

* **API Compatibility**: Frontend must work seamlessly with backend API
* **Dynamic Architecture**: Support for user-created calendars instead of fixed categories
* **Data Integrity**: Ensure data models match exactly between frontend and backend
* **Scalability**: Architecture should support future feature additions
* **User Experience**: Smooth, error-free API interactions

## Considered Options

### Option 1: Patch Existing Implementation
- Pros: Minimal changes required
- Cons: Maintains architectural misalignment, technical debt

### Option 2: Complete API Integration Rewrite
- Pros: Perfect alignment, clean architecture
- Cons: Significant development effort

### Option 3: Incremental Alignment (Chosen)
- Pros: Systematic fixes, maintainable progress
- Cons: Requires careful coordination

## Decision Outcome

**Chosen Option**: Option 3 - Incremental Alignment

We decided to systematically align the Flutter frontend with the backend API through targeted fixes while maintaining working functionality.

## Implementation Details

### 1. Remove Hardcoded Calendar Categories

**Before:**
```dart
final List<String> _calendarNames = ['Personal', 'Lover', 'Friends', 'Work'];
```

**After:**
```dart
// Dynamic calendar loading from API
final calendars = ref.watch(calendarProvider).calendars;
```

### 2. Fix API Endpoint Paths

**Lists API Endpoints:**
```dart
// Before (incorrect)
@GET('/calendars/{calendarId}/lists')
@POST('/calendars/{calendarId}/lists')

// After (correct)
@GET('/lists/calendar/{calendarId}')
@POST('/lists/')
```

**List Items API Endpoints:**
```dart
// Before (incorrect)
@GET('/lists/{listId}/items')
@POST('/lists/{listId}/items')

// After (correct)
@GET('/list-items/list/{listId}')
@POST('/list-items/')
```

### 3. Align Data Models

**ListType Enum:**
```dart
enum ListType {
  @JsonValue('TODO')      // Match backend exactly
  todo,
  @JsonValue('PRIORITY')  // Match backend exactly
  priority,
}
```

**TodoList Model:**
```dart
class TodoList extends Equatable {
  final int id;
  final String name;
  final String? description;
  @JsonKey(name: 'list_type')  // Map to backend field
  final ListType type;
  @JsonKey(name: 'calendar_id')
  final int calendarId;
  @JsonKey(name: 'created_at')
  final DateTime createdAt;
}
```

**ListItem Model Overhaul:**
```dart
// Before (misaligned)
class ListItem {
  final String title;
  final String? description;
  final DateTime? dueDate;
  // ...
}

// After (aligned)
class ListItem {
  final String content;          // Backend field name
  @JsonKey(name: 'is_completed')
  final bool isCompleted;
  @JsonKey(name: 'list_id')
  final int listId;
  @JsonKey(name: 'creator_id')
  final int? creatorId;
  @JsonKey(name: 'vote_count')
  final int? voteCount;
  // ...
}
```

### 4. Update UI Components

**TodoItemCard Simplification:**
```dart
// Before (complex, unsupported fields)
TodoItemCard(
  title: item.title,
  description: item.description,
  dueDate: item.dueDate,
  // ...
)

// After (simplified, supported fields)
TodoItemCard(
  content: item.content,
  isCompleted: item.isCompleted,
  voteCount: item.voteCount,
  // ...
)
```

**Dynamic TabController Management:**
```dart
void _updateTabController(List<Calendar> calendars) {
  if (_calendars.length != calendars.length) {
    _tabController?.dispose();
    _tabController = TabController(length: calendars.length, vsync: this);
    _calendars = calendars;
  }
}
```

### 5. Configuration Updates

**Android Manifest:**
```xml
<application
    android:enableOnBackInvokedCallback="true"
    ...>
```

**API Base URL:**
```dart
// Android emulator configuration
static const String apiBaseUrl = 'http://10.0.2.2:8000/api/v1';
```

### 6. Personal Calendar Naming

**Backend Update:**
```python
# Before
personal_calendar_in = CalendarCreate(name=f"{db_obj.username}'s Personal Calendar")

# After
personal_calendar_in = CalendarCreate(name="Personal")
```

## Positive Consequences

* ✅ **Perfect API Alignment**: All endpoints now match backend implementation
* ✅ **Dynamic Calendar Support**: No more hardcoded categories limitation
* ✅ **Proper Data Models**: JSON serialization works flawlessly
* ✅ **Better UX**: Simplified, consistent user interface
* ✅ **Scalable Architecture**: Easy to add new features
* ✅ **Error Resolution**: Fixed HTTP 307 redirects and JSON parsing errors

## Negative Consequences

* ⚠️ **Breaking Changes**: Existing UI components required updates
* ⚠️ **Migration Effort**: Substantial code changes across multiple files
* ⚠️ **Testing Required**: All API integrations need re-validation

## Implementation Notes

### Files Modified

**Backend:**
- `app/crud/crud_user.py` - Personal calendar naming

**Frontend:**
- `lib/core/services/api_client.dart` - API endpoint corrections
- `lib/shared/models/todo.dart` - Data model alignment
- `lib/shared/models/calendar.dart` - Calendar type support
- `lib/features/todo/screens/todo_screen.dart` - Dynamic UI
- `lib/features/vote/screens/vote_screen.dart` - Dynamic UI
- `lib/features/calendar/screens/calendar_screen.dart` - Dynamic UI
- `lib/shared/widgets/molecules/todo_item_card.dart` - Simplified component
- `lib/features/todo/widgets/add_todo_dialog.dart` - Simplified dialog
- `android/app/src/main/AndroidManifest.xml` - Android configuration

### Testing Strategy

1. **API Endpoint Testing**: Verify all CRUD operations work
2. **JSON Serialization**: Test model parsing with real backend data
3. **UI Component Testing**: Ensure components handle dynamic data
4. **State Management Testing**: Verify Riverpod providers work correctly
5. **Integration Testing**: End-to-end user flows

### Migration Guide

For developers updating existing code:

1. **Update Dependencies**: Run `flutter packages pub run build_runner build --delete-conflicting-outputs`
2. **Model Updates**: Replace `title` with `content` in ListItem usage
3. **API Calls**: Remove hardcoded calendar references
4. **UI Components**: Update widget parameters to match new models
5. **State Management**: Verify provider dependencies

## Compliance

This decision aligns with:
- **ADR-002**: Extendable multi-list model architecture
- **ADR-006**: Flutter technology stack selection
- **ADR-007**: Flutter UI architecture design
- **Backend API specifications** defined in REST API documentation

## Related Documents

- [Flutter API Integration Implementation](../implementation/flutter-api-integration.md)
- [REST API Documentation](../api/rest-api.md)
- [Backend README](../../backend/README.md)
- [Mobile README](../../mobile/README.md)

## Future Considerations

1. **Real-time Updates**: WebSocket integration for live collaboration
2. **Offline Support**: Enhanced caching and sync mechanisms
3. **Performance Optimization**: Lazy loading and pagination
4. **Error Recovery**: Robust error handling and retry logic
5. **Testing Automation**: Comprehensive test coverage for API integration

This ADR represents a significant milestone in achieving seamless frontend-backend integration and establishing a solid foundation for future feature development.