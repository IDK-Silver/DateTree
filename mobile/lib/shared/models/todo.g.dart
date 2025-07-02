// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'todo.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

TodoList _$TodoListFromJson(Map<String, dynamic> json) => TodoList(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      description: json['description'] as String?,
      type: $enumDecode(_$ListTypeEnumMap, json['type']),
      calendarId: (json['calendar_id'] as num).toInt(),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$TodoListToJson(TodoList instance) => <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'description': instance.description,
      'type': _$ListTypeEnumMap[instance.type]!,
      'calendar_id': instance.calendarId,
      'created_at': instance.createdAt.toIso8601String(),
    };

const _$ListTypeEnumMap = {
  ListType.todo: 'todo',
  ListType.priority: 'priority',
  ListType.checklist: 'checklist',
};

TodoListCreate _$TodoListCreateFromJson(Map<String, dynamic> json) =>
    TodoListCreate(
      name: json['name'] as String,
      description: json['description'] as String?,
      type: $enumDecode(_$ListTypeEnumMap, json['type']),
      calendarId: (json['calendar_id'] as num).toInt(),
    );

Map<String, dynamic> _$TodoListCreateToJson(TodoListCreate instance) =>
    <String, dynamic>{
      'name': instance.name,
      'description': instance.description,
      'type': _$ListTypeEnumMap[instance.type]!,
      'calendar_id': instance.calendarId,
    };

ListItem _$ListItemFromJson(Map<String, dynamic> json) => ListItem(
      id: (json['id'] as num).toInt(),
      title: json['title'] as String,
      description: json['description'] as String?,
      dueDate: json['due_date'] == null
          ? null
          : DateTime.parse(json['due_date'] as String),
      isCompleted: json['is_completed'] as bool,
      listId: (json['list_id'] as num).toInt(),
      createdAt: DateTime.parse(json['created_at'] as String),
      completedAt: json['completed_at'] == null
          ? null
          : DateTime.parse(json['completed_at'] as String),
    );

Map<String, dynamic> _$ListItemToJson(ListItem instance) => <String, dynamic>{
      'id': instance.id,
      'title': instance.title,
      'description': instance.description,
      'due_date': instance.dueDate?.toIso8601String(),
      'is_completed': instance.isCompleted,
      'list_id': instance.listId,
      'created_at': instance.createdAt.toIso8601String(),
      'completed_at': instance.completedAt?.toIso8601String(),
    };

ListItemCreate _$ListItemCreateFromJson(Map<String, dynamic> json) =>
    ListItemCreate(
      title: json['title'] as String,
      description: json['description'] as String?,
      dueDate: json['due_date'] == null
          ? null
          : DateTime.parse(json['due_date'] as String),
      listId: (json['list_id'] as num).toInt(),
    );

Map<String, dynamic> _$ListItemCreateToJson(ListItemCreate instance) =>
    <String, dynamic>{
      'title': instance.title,
      'description': instance.description,
      'due_date': instance.dueDate?.toIso8601String(),
      'list_id': instance.listId,
    };

ListItemUpdate _$ListItemUpdateFromJson(Map<String, dynamic> json) =>
    ListItemUpdate(
      title: json['title'] as String?,
      description: json['description'] as String?,
      dueDate: json['due_date'] == null
          ? null
          : DateTime.parse(json['due_date'] as String),
      isCompleted: json['is_completed'] as bool?,
    );

Map<String, dynamic> _$ListItemUpdateToJson(ListItemUpdate instance) =>
    <String, dynamic>{
      'title': instance.title,
      'description': instance.description,
      'due_date': instance.dueDate?.toIso8601String(),
      'is_completed': instance.isCompleted,
    };
