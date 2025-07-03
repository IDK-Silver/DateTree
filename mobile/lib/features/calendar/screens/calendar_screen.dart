import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:table_calendar/table_calendar.dart';

import '../../../core/providers/todo_provider.dart';

class CalendarScreen extends ConsumerStatefulWidget {
  const CalendarScreen({super.key});

  @override
  ConsumerState<CalendarScreen> createState() => _CalendarScreenState();
}

class _CalendarScreenState extends ConsumerState<CalendarScreen> {
  CalendarFormat _calendarFormat = CalendarFormat.month;
  DateTime _focusedDay = DateTime.now();
  DateTime? _selectedDay;
  Set<int> _selectedCalendarIds = {};

  @override
  void initState() {
    super.initState();
    _selectedDay = _focusedDay;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Calendar'),
        actions: [
          PopupMenuButton<CalendarFormat>(
            onSelected: (CalendarFormat format) {
              setState(() {
                _calendarFormat = format;
              });
            },
            itemBuilder: (BuildContext context) => [
              const PopupMenuItem(
                value: CalendarFormat.month,
                child: Text('Month'),
              ),
              const PopupMenuItem(
                value: CalendarFormat.twoWeeks,
                child: Text('2 weeks'),
              ),
              const PopupMenuItem(
                value: CalendarFormat.week,
                child: Text('Week'),
              ),
            ],
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: Row(
                children: [
                  Text(
                    _calendarFormat == CalendarFormat.month
                        ? 'Month'
                        : _calendarFormat == CalendarFormat.twoWeeks
                            ? '2 weeks'
                            : 'Week',
                    style: const TextStyle(fontSize: 16),
                  ),
                  const Icon(Icons.arrow_drop_down),
                ],
              ),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.filter_list),
            onPressed: () {
              _showFilterBottomSheet(context);
            },
          ),
        ],
      ),
      body: Column(
        children: [
          TableCalendar(
            firstDay: DateTime.utc(2020, 1, 1),
            lastDay: DateTime.utc(2030, 12, 31),
            focusedDay: _focusedDay,
            calendarFormat: _calendarFormat,
            selectedDayPredicate: (day) {
              return isSameDay(_selectedDay, day);
            },
            onDaySelected: (selectedDay, focusedDay) {
              if (!isSameDay(_selectedDay, selectedDay)) {
                setState(() {
                  _selectedDay = selectedDay;
                  _focusedDay = focusedDay;
                });
              }
            },
            onFormatChanged: (format) {
              if (_calendarFormat != format) {
                setState(() {
                  _calendarFormat = format;
                });
              }
            },
            onPageChanged: (focusedDay) {
              _focusedDay = focusedDay;
            },
            calendarStyle: CalendarStyle(
              outsideDaysVisible: false,
              weekendTextStyle: TextStyle(color: Theme.of(context).colorScheme.primary),
              selectedDecoration: BoxDecoration(
                color: Theme.of(context).colorScheme.primary,
                shape: BoxShape.circle,
              ),
              todayDecoration: BoxDecoration(
                color: Theme.of(context).colorScheme.secondary.withValues(alpha: 0.5),
                shape: BoxShape.circle,
              ),
            ),
            headerStyle: const HeaderStyle(
              formatButtonVisible: false,
              titleCentered: true,
            ),
          ),
          const Divider(height: 1),
          Expanded(
            child: ListView(
              padding: const EdgeInsets.all(16.0),
              children: [
                Text(
                  'Events for ${_selectedDay != null ? "${_selectedDay!.day}/${_selectedDay!.month}/${_selectedDay!.year}" : "Select a day"}',
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                const SizedBox(height: 16),
                const Center(
                  child: Text('No events for this day'),
                ),
              ],
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // TODO: Implement add event
        },
        child: const Icon(Icons.add),
      ),
    );
  }

  void _showFilterBottomSheet(BuildContext context) {
    final calendarState = ref.read(calendarProvider);
    final calendars = calendarState.calendars;
    
    // Initialize selected calendars if empty
    if (_selectedCalendarIds.isEmpty && calendars.isNotEmpty) {
      _selectedCalendarIds = calendars.map((c) => c.id).toSet();
    }
    
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (BuildContext context) {
        return StatefulBuilder(
          builder: (BuildContext context, StateSetter setModalState) {
            return Container(
              padding: const EdgeInsets.all(16.0),
              constraints: BoxConstraints(
                maxHeight: MediaQuery.of(context).size.height * 0.8,
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        'Filter Calendars',
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                      TextButton(
                        onPressed: () {
                          Navigator.pop(context);
                          setState(() {});
                        },
                        child: const Text('Done'),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  if (calendars.isEmpty)
                    const Padding(
                      padding: EdgeInsets.symmetric(vertical: 32.0),
                      child: Center(
                        child: Text('No calendars available'),
                      ),
                    )
                  else ...[                    
                    const Text(
                      'Calendars',
                      style: TextStyle(fontWeight: FontWeight.w600),
                    ),
                    const SizedBox(height: 8),
                    Flexible(
                      child: ListView.builder(
                        shrinkWrap: true,
                        itemCount: calendars.length,
                        itemBuilder: (context, index) {
                          final calendar = calendars[index];
                          return CheckboxListTile(
                            title: Text(calendar.name),
                            subtitle: calendar.description != null 
                                ? Text(calendar.description!) 
                                : null,
                            value: _selectedCalendarIds.contains(calendar.id),
                            onChanged: (bool? value) {
                              setModalState(() {
                                if (value == true) {
                                  _selectedCalendarIds.add(calendar.id);
                                } else {
                                  _selectedCalendarIds.remove(calendar.id);
                                }
                              });
                            },
                            controlAffinity: ListTileControlAffinity.leading,
                          );
                        },
                      ),
                    ),
                    const SizedBox(height: 16),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        TextButton(
                          onPressed: () {
                            setModalState(() {
                              _selectedCalendarIds.clear();
                            });
                          },
                          child: const Text('Clear All'),
                        ),
                        TextButton(
                          onPressed: () {
                            setModalState(() {
                              _selectedCalendarIds = calendars.map((c) => c.id).toSet();
                            });
                          },
                          child: const Text('Select All'),
                        ),
                      ],
                    ),
                  ],
                ],
              ),
            );
          },
        );
      },
    );
  }
}