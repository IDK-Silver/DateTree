import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../shared/models/calendar.dart';
import '../../shared/models/todo.dart';
import 'api_client.dart';
import 'auth_service.dart';

class TodoService {
  final ApiClient _apiClient;

  TodoService(this._apiClient);

  // Calendar operations
  Future<List<Calendar>> getCalendars() async {
    try {
      return await _apiClient.getCalendars();
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Calendar> createCalendar(CalendarCreate calendar) async {
    try {
      return await _apiClient.createCalendar(calendar);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Calendar> updateCalendar(int id, CalendarCreate calendar) async {
    try {
      return await _apiClient.updateCalendar(id, calendar);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<void> deleteCalendar(int id) async {
    try {
      await _apiClient.deleteCalendar(id);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  // List operations
  Future<List<TodoList>> getLists(int calendarId) async {
    try {
      return await _apiClient.getLists(calendarId);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<TodoList> createList(int calendarId, TodoListCreate list) async {
    try {
      return await _apiClient.createList(calendarId, list);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<TodoList> updateList(int id, TodoListCreate list) async {
    try {
      return await _apiClient.updateList(id, list);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<void> deleteList(int id) async {
    try {
      await _apiClient.deleteList(id);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  // List item operations
  Future<List<ListItem>> getListItems(int listId) async {
    try {
      return await _apiClient.getListItems(listId);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<ListItem> createListItem(int listId, ListItemCreate item) async {
    try {
      return await _apiClient.createListItem(listId, item);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<ListItem> updateListItem(int id, ListItemUpdate item) async {
    try {
      return await _apiClient.updateListItem(id, item);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<void> deleteListItem(int id) async {
    try {
      await _apiClient.deleteListItem(id);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  // Helper method to get all todos for a calendar
  Future<List<ListItem>> getAllTodosForCalendar(int calendarId) async {
    try {
      final lists = await getLists(calendarId);
      final todoLists = lists.where((list) => list.type == ListType.todo).toList();
      
      final allTodos = <ListItem>[];
      for (final list in todoLists) {
        final todos = await getListItems(list.id);
        allTodos.addAll(todos);
      }
      
      return allTodos;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  // Helper method to get or create default todo list for a calendar
  Future<TodoList> getOrCreateDefaultTodoList(int calendarId, String calendarName) async {
    try {
      final lists = await getLists(calendarId);
      final todoLists = lists.where((list) => list.type == ListType.todo).toList();
      
      if (todoLists.isNotEmpty) {
        return todoLists.first;
      }
      
      // Create default todo list
      final defaultList = TodoListCreate(
        name: '$calendarName Tasks',
        description: 'Default todo list for $calendarName',
        type: ListType.todo,
        calendarId: calendarId,
      );
      
      return await createList(calendarId, defaultList);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  String _handleError(DioException e) {
    switch (e.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return 'Connection timeout. Please check your internet connection.';
      case DioExceptionType.badResponse:
        switch (e.response?.statusCode) {
          case 400:
            return 'Invalid request. Please check your input.';
          case 401:
            return 'Please log in again.';
          case 403:
            return 'You do not have permission to perform this action.';
          case 404:
            return 'Resource not found.';
          case 500:
            return 'Server error. Please try again later.';
          default:
            return 'Request failed with status ${e.response?.statusCode}';
        }
      case DioExceptionType.cancel:
        return 'Request was cancelled.';
      case DioExceptionType.unknown:
        return 'Network error. Please check your connection.';
      default:
        return 'An unexpected error occurred.';
    }
  }
}

// Provider
final todoServiceProvider = Provider<TodoService>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  return TodoService(apiClient);
});