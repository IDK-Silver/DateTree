import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/providers/todo_provider.dart';
import '../../../shared/widgets/molecules/todo_item_card.dart';
import '../../../shared/widgets/molecules/calendar_info_card.dart';
import '../../../shared/models/calendar.dart';
import '../../../shared/models/todo.dart';
import '../widgets/add_todo_dialog.dart';

class TodoScreen extends ConsumerStatefulWidget {
  const TodoScreen({super.key});

  @override
  ConsumerState<TodoScreen> createState() => _TodoScreenState();
}

class _TodoScreenState extends ConsumerState<TodoScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;
  final List<String> _calendarNames = ['Personal', 'Lover', 'Friends', 'Work'];

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: _calendarNames.length, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final calendarState = ref.watch(calendarProvider);
    final calendars = calendarState.calendars;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Todo'),
        bottom: TabBar(
          controller: _tabController,
          isScrollable: true,
          tabs: _calendarNames.map((name) => Tab(text: name)).toList(),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: () => _showAddTodoDialog(context),
          ),
        ],
      ),
      body: calendarState.isLoading
          ? const Center(child: CircularProgressIndicator())
          : TabBarView(
              controller: _tabController,
              children: _calendarNames.map((name) {
                final calendar = calendars.where((c) => c.name.toLowerCase() == name.toLowerCase()).firstOrNull;
                return _buildTodoList(calendar, name);
              }).toList(),
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _showAddTodoDialog(context),
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildTodoList(Calendar? calendar, String categoryName) {
    if (calendar == null) {
      return _buildEmptyCalendar(categoryName);
    }

    final todoState = ref.watch(todoProvider(calendar.id));
    
    return RefreshIndicator(
      onRefresh: () async {
        await ref.read(todoProvider(calendar.id).notifier).loadTodos();
      },
      child: CustomScrollView(
        slivers: [
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: CalendarInfoCard(
                calendarName: categoryName,
                calendarColor: _getCalendarColor(categoryName),
                pendingTasks: todoState.pendingItems.length,
                completedTasks: todoState.completedItems.length,
                onTap: () {
                  // TODO: Navigate to calendar details
                },
              ),
            ),
          ),
          const SliverToBoxAdapter(
            child: Padding(
              padding: EdgeInsets.symmetric(horizontal: 16.0),
              child: Text(
                'Pending',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ),
          if (todoState.isLoading)
            const SliverToBoxAdapter(
              child: Center(
                child: Padding(
                  padding: EdgeInsets.all(32.0),
                  child: CircularProgressIndicator(),
                ),
              ),
            )
          else if (todoState.pendingItems.isEmpty)
            const SliverToBoxAdapter(
              child: Center(
                child: Padding(
                  padding: EdgeInsets.all(32.0),
                  child: Text('No pending tasks'),
                ),
              ),
            )
          else
            SliverList(
              delegate: SliverChildBuilderDelegate(
                (context, index) {
                  final item = todoState.pendingItems[index];
                  return TodoItemCard(
                    id: item.id.toString(),
                    title: item.title,
                    description: item.description,
                    dueDate: item.dueDate,
                    isCompleted: item.isCompleted,
                    onTap: () => _editTodo(item),
                    onComplete: () => _completeTodo(calendar.id, item.id),
                    onDelete: () => _deleteTodo(calendar.id, item.id),
                  );
                },
                childCount: todoState.pendingItems.length,
              ),
            ),
          const SliverToBoxAdapter(
            child: Padding(
              padding: EdgeInsets.fromLTRB(16.0, 32.0, 16.0, 8.0),
              child: Text(
                'Completed',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ),
          if (todoState.completedItems.isEmpty)
            const SliverToBoxAdapter(
              child: Center(
                child: Padding(
                  padding: EdgeInsets.all(32.0),
                  child: Text('No completed tasks'),
                ),
              ),
            )
          else
            SliverList(
              delegate: SliverChildBuilderDelegate(
                (context, index) {
                  final item = todoState.completedItems[index];
                  return TodoItemCard(
                    id: item.id.toString(),
                    title: item.title,
                    description: item.description,
                    dueDate: item.dueDate,
                    isCompleted: item.isCompleted,
                    onTap: () => _editTodo(item),
                    onDelete: () => _deleteTodo(calendar.id, item.id),
                  );
                },
                childCount: todoState.completedItems.length,
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildEmptyCalendar(String categoryName) {
    return CustomScrollView(
      slivers: [
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: CalendarInfoCard(
              calendarName: categoryName,
              calendarColor: _getCalendarColor(categoryName),
              pendingTasks: 0,
              completedTasks: 0,
              onTap: () => _createCalendar(categoryName),
            ),
          ),
        ),
        SliverToBoxAdapter(
          child: Center(
            child: Padding(
              padding: const EdgeInsets.all(32.0),
              child: Column(
                children: [
                  Icon(
                    Icons.calendar_today_outlined,
                    size: 64,
                    color: Colors.grey[400],
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'No $categoryName calendar found',
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  const SizedBox(height: 8),
                  ElevatedButton(
                    onPressed: () => _createCalendar(categoryName),
                    child: Text('Create $categoryName Calendar'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ],
    );
  }

  Color _getCalendarColor(String categoryName) {
    switch (categoryName.toLowerCase()) {
      case 'personal':
        return Colors.blue;
      case 'lover':
        return Colors.pink;
      case 'friends':
        return Colors.green;
      case 'work':
        return Colors.orange;
      default:
        return Colors.grey;
    }
  }

  void _showAddTodoDialog(BuildContext context) {
    final currentIndex = _tabController.index;
    final categoryName = _calendarNames[currentIndex];
    final calendars = ref.read(calendarProvider).calendars;
    final calendar = calendars.where((c) => c.name.toLowerCase() == categoryName.toLowerCase()).firstOrNull;

    if (calendar == null) {
      _createCalendar(categoryName);
      return;
    }

    showDialog(
      context: context,
      builder: (context) => AddTodoDialog(
        calendarId: calendar.id,
        onTodoAdded: () {
          ref.read(todoProvider(calendar.id).notifier).loadTodos();
        },
      ),
    );
  }

  void _createCalendar(String name) async {
    await ref.read(calendarProvider.notifier).createCalendar(name);
  }

  void _completeTodo(int calendarId, int todoId) async {
    await ref.read(todoProvider(calendarId).notifier).completeTodo(todoId);
  }

  void _deleteTodo(int calendarId, int todoId) async {
    await ref.read(todoProvider(calendarId).notifier).deleteTodo(todoId);
  }

  void _editTodo(ListItem item) {
    // TODO: Implement edit todo functionality
  }
}