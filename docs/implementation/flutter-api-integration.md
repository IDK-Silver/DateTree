# Flutter API Integration Implementation

## Overview

This document details the Flutter frontend's integration with the DateTree backend API, focusing on the dynamic calendar management system and proper data model alignment.

## Architecture Changes

### From Hardcoded to Dynamic Calendar Management

**Previous Implementation:**
- Hardcoded calendar categories: `['Personal', 'Lover', 'Friends', 'Work']`
- Fixed TabController with 4 tabs
- Static UI components

**Current Implementation:**
- Dynamic calendar loading from backend API
- Variable TabController based on user's actual calendars
- Responsive UI that adapts to calendar count

### API Endpoint Corrections

The Flutter API client has been updated to match the backend implementation:

#### Lists API
```dart
// Before
@GET('/calendars/{calendarId}/lists')
@POST('/calendars/{calendarId}/lists')

// After
@GET('/lists/calendar/{calendarId}')
@POST('/lists/')
```

#### List Items API
```dart
// Before
@GET('/lists/{listId}/items')
@POST('/lists/{listId}/items')

// After
@GET('/list-items/list/{listId}')
@POST('/list-items/')
```

### Data Model Alignment

#### ListType Enum
```dart
enum ListType {
  @JsonValue('TODO')      // Matches backend 'TODO'
  todo,
  @JsonValue('PRIORITY')  // Matches backend 'PRIORITY'
  priority,
}
```

#### TodoList Model
```dart
class TodoList extends Equatable {
  final int id;
  final String name;
  final String? description;
  @JsonKey(name: 'list_type')  // Maps to backend field
  final ListType type;
  @JsonKey(name: 'calendar_id')
  final int calendarId;
  @JsonKey(name: 'created_at')
  final DateTime createdAt;
}
```

#### ListItem Model
```dart
class ListItem extends Equatable {
  final int id;
  final String content;           // Backend field name
  @JsonKey(name: 'is_completed')
  final bool isCompleted;
  @JsonKey(name: 'list_id')
  final int listId;
  @JsonKey(name: 'creator_id')
  final int? creatorId;
  @JsonKey(name: 'created_at')
  final DateTime createdAt;
  @JsonKey(name: 'vote_count')
  final int? voteCount;
}
```

## State Management

### Calendar Provider
- Automatically loads calendars when user authenticates
- Manages calendar CRUD operations
- Provides reactive state updates to UI components

### Todo Provider
- Per-calendar todo state management using `StateNotifierProvider.family`
- Optimistic updates with server synchronization
- Error handling and retry logic

### UI Components

#### TodoScreen
- Dynamic TabController management
- Handles empty state when no calendars exist
- Provides calendar creation functionality

#### TodoItemCard
- Simplified to display content and vote count
- Removed unsupported fields (description, dueDate)
- Shows voting indicators for PRIORITY lists

#### AddTodoDialog
- Streamlined to single content field
- Automatic list creation when needed
- Error handling with user feedback

## API Integration Patterns

### Error Handling
```dart
try {
  final result = await apiCall();
  // Update state optimistically
  state = state.copyWith(data: result);
} on DioException catch (e) {
  // Handle specific HTTP errors
  throw _handleError(e);
} catch (e) {
  // Handle unexpected errors
  state = state.copyWith(error: e.toString());
}
```

### State Synchronization
```dart
// Optimistic update followed by refresh
await createTodo(content: content);
// Callback triggers refresh to ensure consistency
onTodoAdded?.call();
```

## Configuration

### API Base URL
```dart
// Android emulator configuration
static const String apiBaseUrl = 'http://10.0.2.2:8000/api/v1';
```

### Android Manifest
```xml
<application
    android:enableOnBackInvokedCallback="true"
    ...>
```

## Testing Considerations

### API Endpoint Testing
- Verify correct endpoint paths match backend routes
- Test HTTP methods and request/response formats
- Validate JSON serialization/deserialization

### State Management Testing
- Test optimistic updates and rollback scenarios
- Verify error state handling
- Test reactive UI updates

### UI Component Testing
- Test empty states and loading states
- Verify dynamic TabController behavior
- Test error message display

## Performance Optimizations

### Efficient Data Loading
- Load calendars once on authentication
- Per-calendar todo loading with caching
- Lazy loading of calendar details

### UI Responsiveness
- Optimistic updates for immediate feedback
- Proper loading indicators
- Efficient widget rebuilding with Riverpod

## Future Enhancements

### Planned Features
- Calendar sharing and permissions
- Real-time collaboration with WebSockets
- Offline support with local caching
- Push notifications for todo updates

### Scalability Considerations
- Pagination for large todo lists
- Efficient calendar switching
- Memory management for multiple calendars

## Troubleshooting

### Common Issues

#### HTTP 307 Redirects
- Ensure POST endpoints have trailing slashes
- Match exact endpoint paths with backend

#### JSON Parsing Errors
- Verify @JsonKey annotations match backend field names
- Check enum values match backend exactly

#### State Not Updating
- Ensure providers are properly watched
- Check for proper state copying in notifiers
- Verify callback functions are called

### Debug Tools
- Use Dio interceptors for request/response logging
- Add debug prints in state notifiers
- Use Flutter Inspector for widget tree analysis

## Migration Notes

### Breaking Changes
- Calendar names are now dynamic (no more hardcoded categories)
- ListItem model fields changed (title → content)
- API endpoints updated to match backend

### Migration Steps
1. Update API client generated code
2. Modify existing UI components
3. Test all CRUD operations
4. Verify state management flows
5. Update any hardcoded references

This implementation provides a robust, scalable foundation for the DateTree Flutter frontend with proper backend API integration.