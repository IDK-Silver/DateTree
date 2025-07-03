import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/providers/todo_provider.dart';
import '../../../shared/models/calendar.dart';

class VoteScreen extends ConsumerStatefulWidget {
  const VoteScreen({super.key});

  @override
  ConsumerState<VoteScreen> createState() => _VoteScreenState();
}

class _VoteScreenState extends ConsumerState<VoteScreen>
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
        title: const Text('Vote'),
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
            onPressed: () {
              // TODO: Implement quick add vote item
            },
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
                        return _buildVoteList(calendar);
                      }).toList(),
                    ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // TODO: Implement add vote item
        },
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildVoteList(Calendar calendar) {
    return CustomScrollView(
      slivers: [
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '${calendar.name} Calendar',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      '0 active votes',
                      style: Theme.of(context).textTheme.bodySmall,
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
        const SliverToBoxAdapter(
          child: Padding(
            padding: EdgeInsets.symmetric(horizontal: 16.0),
            child: Text(
              'Active Votes',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
        ),
        SliverList(
          delegate: SliverChildListDelegate([
            const Center(
              child: Padding(
                padding: EdgeInsets.all(32.0),
                child: Text('No active votes'),
              ),
            ),
          ]),
        ),
        const SliverToBoxAdapter(
          child: Padding(
            padding: EdgeInsets.fromLTRB(16.0, 32.0, 16.0, 8.0),
            child: Text(
              'Completed Votes',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
        ),
        SliverList(
          delegate: SliverChildListDelegate([
            const Center(
              child: Padding(
                padding: EdgeInsets.all(32.0),
                child: Text('No completed votes'),
              ),
            ),
          ]),
        ),
      ],
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
              Icons.how_to_vote_outlined,
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
              'Create a calendar to start collaborative voting',
              style: Theme.of(context).textTheme.bodyMedium,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: () {
                // Navigate to Todo screen where calendar creation is available
                final scaffoldMessenger = ScaffoldMessenger.of(context);
                scaffoldMessenger.showSnackBar(
                  const SnackBar(
                    content: Text('Navigate to Todo tab to create a calendar'),
                  ),
                );
              },
              icon: const Icon(Icons.add),
              label: const Text('Create Calendar'),
            ),
          ],
        ),
      ),
    );
  }
}