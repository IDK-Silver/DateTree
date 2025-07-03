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
  TabController? _tabController;
  List<Calendar> _calendars = [];

  @override
  void initState() {
    super.initState();
    // Tab controller will be initialized when calendars are loaded
  }

  @override
  void dispose() {
    _tabController?.dispose();
    super.dispose();
  }

  void _updateTabController(List<Calendar> calendars) {
    if (_calendars.length != calendars.length) {
      _tabController?.dispose();
      _tabController = TabController(length: calendars.length, vsync: this);
      _calendars = calendars;
    }
  }

  @override
  Widget build(BuildContext context) {
    final calendarState = ref.watch(calendarProvider);
    final calendars = calendarState.calendars;
    
    // Update tab controller when calendars change
    if (calendars.isNotEmpty) {
      _updateTabController(calendars);
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Todo'),
        bottom: calendars.isEmpty || _tabController == null
            ? null
            : TabBar(
                controller: _tabController!,
                isScrollable: true,
                tabs: calendars.map((calendar) => Tab(text: calendar.name)).toList(),
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
          : calendars.isEmpty
              ? _buildEmptyState()
              : _tabController == null
                  ? const Center(child: CircularProgressIndicator())
                  : TabBarView(
                      controller: _tabController!,
                      children: calendars.map((calendar) {
                        return _buildTodoList(calendar);
                      }).toList(),
                    ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _showAddTodoDialog(context),
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildTodoList(Calendar calendar) {

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
                calendarName: calendar.name,
                calendarColor: _getCalendarColor(calendar),
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
                    content: item.content,
                    isCompleted: item.isCompleted,
                    voteCount: item.voteCount,
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
                    content: item.content,
                    isCompleted: item.isCompleted,
                    voteCount: item.voteCount,
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

  Widget _buildEmptyState() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.calendar_today_outlined,
              size: 64,
              color: Colors.grey[400],
            ),
            const SizedBox(height: 16),
            Text(
              'No calendars found',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 8),
            Text(
              'Create a calendar to start organizing your tasks',
              style: Theme.of(context).textTheme.bodyMedium,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: () => _showCreateCalendarDialog(),
              icon: const Icon(Icons.add),
              label: const Text('Create Calendar'),
            ),
          ],
        ),
      ),
    );
  }

  Color _getCalendarColor(Calendar calendar) {
    // Use a color based on calendar ID for consistency
    final colors = [
      Colors.blue,
      Colors.green,
      Colors.orange,
      Colors.purple,
      Colors.teal,
      Colors.pink,
      Colors.indigo,
      Colors.amber,
    ];
    return colors[calendar.id % colors.length];
  }

  void _showAddTodoDialog(BuildContext context) {
    if (_tabController == null || _calendars.isEmpty) {
      _showCreateCalendarDialog();
      return;
    }
    
    final currentIndex = _tabController!.index;
    final calendar = _calendars[currentIndex];

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

  void _showCreateCalendarDialog() {
    showDialog(
      context: context,
      builder: (context) {
        final nameController = TextEditingController();
        final descriptionController = TextEditingController();
        
        return AlertDialog(
          title: const Text('Create New Calendar'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: nameController,
                decoration: const InputDecoration(
                  labelText: 'Calendar Name',
                  hintText: 'e.g., Work, Personal, Projects',
                ),
                autofocus: true,
              ),
              const SizedBox(height: 16),
              TextField(
                controller: descriptionController,
                decoration: const InputDecoration(
                  labelText: 'Description (optional)',
                  hintText: 'Brief description of this calendar',
                ),
                maxLines: 2,
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () async {
                final name = nameController.text.trim();
                if (name.isNotEmpty) {
                  await ref.read(calendarProvider.notifier).createCalendar(
                    name,
                    description: descriptionController.text.trim().isEmpty 
                        ? null 
                        : descriptionController.text.trim(),
                  );
                  if (context.mounted) {
                    Navigator.of(context).pop();
                  }
                }
              },
              child: const Text('Create'),
            ),
          ],
        );
      },
    );
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