import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:equatable/equatable.dart';

import '../../shared/models/calendar.dart';
import '../../shared/models/todo.dart';
import '../services/todo_service.dart';
import 'auth_provider.dart';

// Calendar state
class CalendarState extends Equatable {
  final List<Calendar> calendars;
  final bool isLoading;
  final String? error;

  const CalendarState({
    this.calendars = const [],
    this.isLoading = false,
    this.error,
  });

  CalendarState copyWith({
    List<Calendar>? calendars,
    bool? isLoading,
    String? error,
  }) {
    return CalendarState(
      calendars: calendars ?? this.calendars,
      isLoading: isLoading ?? this.isLoading,
      error: error,
    );
  }

  @override
  List<Object?> get props => [calendars, isLoading, error];
}

class CalendarNotifier extends StateNotifier<CalendarState> {
  final TodoService _todoService;
  final Ref _ref;

  CalendarNotifier(this._todoService, this._ref) : super(const CalendarState()) {
    _init();
  }

  Future<void> _init() async {
    // Watch auth state and load calendars when authenticated
    _ref.listen<AuthState>(authProvider, (previous, next) {
      if (next.isAuthenticated && previous?.isAuthenticated != true) {
        loadCalendars();
      } else if (!next.isAuthenticated && previous?.isAuthenticated == true) {
        state = const CalendarState();
      }
    });

    // Load calendars if already authenticated
    final authState = _ref.read(authProvider);
    if (authState.isAuthenticated) {
      loadCalendars();
    }
  }

  Future<void> loadCalendars() async {
    state = state.copyWith(isLoading: true, error: null);

    try {
      final calendars = await _todoService.getCalendars();
      state = state.copyWith(
        calendars: calendars,
        isLoading: false,
        error: null,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
    }
  }

  Future<void> createCalendar(String name, {String? description}) async {
    try {
      final calendarCreate = CalendarCreate(name: name, description: description);
      final newCalendar = await _todoService.createCalendar(calendarCreate);
      
      state = state.copyWith(
        calendars: [...state.calendars, newCalendar],
        error: null,
      );
    } catch (e) {
      state = state.copyWith(error: e.toString());
    }
  }

  Future<void> updateCalendar(int id, String name, {String? description}) async {
    try {
      final calendarCreate = CalendarCreate(name: name, description: description);
      final updatedCalendar = await _todoService.updateCalendar(id, calendarCreate);
      
      final updatedCalendars = state.calendars.map((calendar) {
        return calendar.id == id ? updatedCalendar : calendar;
      }).toList();
      
      state = state.copyWith(
        calendars: updatedCalendars,
        error: null,
      );
    } catch (e) {
      state = state.copyWith(error: e.toString());
    }
  }

  Future<void> deleteCalendar(int id) async {
    try {
      await _todoService.deleteCalendar(id);
      
      final updatedCalendars = state.calendars.where((calendar) => calendar.id != id).toList();
      state = state.copyWith(
        calendars: updatedCalendars,
        error: null,
      );
    } catch (e) {
      state = state.copyWith(error: e.toString());
    }
  }

  void clearError() {
    state = state.copyWith(error: null);
  }
}

// Todo state for a specific calendar
class TodoState extends Equatable {
  final List<ListItem> items;
  final bool isLoading;
  final String? error;

  const TodoState({
    this.items = const [],
    this.isLoading = false,
    this.error,
  });

  TodoState copyWith({
    List<ListItem>? items,
    bool? isLoading,
    String? error,
  }) {
    return TodoState(
      items: items ?? this.items,
      isLoading: isLoading ?? this.isLoading,
      error: error,
    );
  }

  List<ListItem> get pendingItems => items.where((item) => !item.isCompleted).toList();
  List<ListItem> get completedItems => items.where((item) => item.isCompleted).toList();

  @override
  List<Object?> get props => [items, isLoading, error];
}

class TodoNotifier extends StateNotifier<TodoState> {
  final TodoService _todoService;
  final int calendarId;

  TodoNotifier(this._todoService, this.calendarId) : super(const TodoState()) {
    loadTodos();
  }

  Future<void> loadTodos() async {
    state = state.copyWith(isLoading: true, error: null);

    try {
      final todos = await _todoService.getAllTodosForCalendar(calendarId);
      state = state.copyWith(
        items: todos,
        isLoading: false,
        error: null,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
    }
  }

  Future<void> createTodo({
    required String title,
    String? description,
    DateTime? dueDate,
  }) async {
    try {
      // Get or create default todo list for this calendar
      final calendar = await _getCalendar();
      final todoList = await _todoService.getOrCreateDefaultTodoList(calendarId, calendar.name);
      
      final itemCreate = ListItemCreate(
        title: title,
        description: description,
        dueDate: dueDate,
        listId: todoList.id,
      );
      
      final newItem = await _todoService.createListItem(todoList.id, itemCreate);
      
      state = state.copyWith(
        items: [...state.items, newItem],
        error: null,
      );
    } catch (e) {
      state = state.copyWith(error: e.toString());
    }
  }

  Future<void> updateTodo(int id, {
    String? title,
    String? description,
    DateTime? dueDate,
    bool? isCompleted,
  }) async {
    try {
      final update = ListItemUpdate(
        title: title,
        description: description,
        dueDate: dueDate,
        isCompleted: isCompleted,
      );
      
      final updatedItem = await _todoService.updateListItem(id, update);
      
      final updatedItems = state.items.map((item) {
        return item.id == id ? updatedItem : item;
      }).toList();
      
      state = state.copyWith(
        items: updatedItems,
        error: null,
      );
    } catch (e) {
      state = state.copyWith(error: e.toString());
    }
  }

  Future<void> completeTodo(int id) async {
    await updateTodo(id, isCompleted: true);
  }

  Future<void> deleteTodo(int id) async {
    try {
      await _todoService.deleteListItem(id);
      
      final updatedItems = state.items.where((item) => item.id != id).toList();
      state = state.copyWith(
        items: updatedItems,
        error: null,
      );
    } catch (e) {
      state = state.copyWith(error: e.toString());
    }
  }

  Future<Calendar> _getCalendar() async {
    // This is a simple implementation - in a real app you might want to cache this
    final calendars = await _todoService.getCalendars();
    return calendars.firstWhere((calendar) => calendar.id == calendarId);
  }

  void clearError() {
    state = state.copyWith(error: null);
  }
}

// Providers
final calendarProvider = StateNotifierProvider<CalendarNotifier, CalendarState>((ref) {
  final todoService = ref.watch(todoServiceProvider);
  return CalendarNotifier(todoService, ref);
});

// Family provider for todos by calendar
final todoProvider = StateNotifierProvider.family<TodoNotifier, TodoState, int>((ref, calendarId) {
  final todoService = ref.watch(todoServiceProvider);
  return TodoNotifier(todoService, calendarId);
});

// Helper provider to get current user's calendars
final userCalendarsProvider = Provider<List<Calendar>>((ref) {
  final calendarState = ref.watch(calendarProvider);
  return calendarState.calendars;
});

// Helper provider to get a specific calendar by name
final calendarByNameProvider = Provider.family<Calendar?, String>((ref, name) {
  final calendars = ref.watch(userCalendarsProvider);
  try {
    return calendars.firstWhere((calendar) => calendar.name.toLowerCase() == name.toLowerCase());
  } catch (e) {
    return null;
  }
});