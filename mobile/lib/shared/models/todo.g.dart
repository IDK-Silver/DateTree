// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'todo.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

TodoList _$TodoListFromJson(Map<String, dynamic> json) => TodoList(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      description: json['description'] as String?,
      type: $enumDecode(_$ListTypeEnumMap, json['list_type']),
      calendarId: (json['calendar_id'] as num).toInt(),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$TodoListToJson(TodoList instance) => <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'description': instance.description,
      'list_type': _$ListTypeEnumMap[instance.type]!,
      'calendar_id': instance.calendarId,
      'created_at': instance.createdAt.toIso8601String(),
    };

const _$ListTypeEnumMap = {
  ListType.todo: 'TODO',
  ListType.priority: 'PRIORITY',
};

TodoListCreate _$TodoListCreateFromJson(Map<String, dynamic> json) =>
    TodoListCreate(
      name: json['name'] as String,
      description: json['description'] as String?,
      type: $enumDecode(_$ListTypeEnumMap, json['list_type']),
      calendarId: (json['calendar_id'] as num).toInt(),
    );

Map<String, dynamic> _$TodoListCreateToJson(TodoListCreate instance) =>
    <String, dynamic>{
      'name': instance.name,
      'description': instance.description,
      'list_type': _$ListTypeEnumMap[instance.type]!,
      'calendar_id': instance.calendarId,
    };

ListItem _$ListItemFromJson(Map<String, dynamic> json) => ListItem(
      id: (json['id'] as num).toInt(),
      content: json['content'] as String,
      isCompleted: json['is_completed'] as bool,
      listId: (json['list_id'] as num).toInt(),
      creatorId: (json['creator_id'] as num?)?.toInt(),
      createdAt: DateTime.parse(json['created_at'] as String),
      voteCount: (json['vote_count'] as num?)?.toInt(),
    );

Map<String, dynamic> _$ListItemToJson(ListItem instance) => <String, dynamic>{
      'id': instance.id,
      'content': instance.content,
      'is_completed': instance.isCompleted,
      'list_id': instance.listId,
      'creator_id': instance.creatorId,
      'created_at': instance.createdAt.toIso8601String(),
      'vote_count': instance.voteCount,
    };

ListItemCreate _$ListItemCreateFromJson(Map<String, dynamic> json) =>
    ListItemCreate(
      content: json['content'] as String,
      listId: (json['list_id'] as num).toInt(),
    );

Map<String, dynamic> _$ListItemCreateToJson(ListItemCreate instance) =>
    <String, dynamic>{
      'content': instance.content,
      'list_id': instance.listId,
    };

ListItemUpdate _$ListItemUpdateFromJson(Map<String, dynamic> json) =>
    ListItemUpdate(
      content: json['content'] as String?,
      isCompleted: json['is_completed'] as bool?,
    );

Map<String, dynamic> _$ListItemUpdateToJson(ListItemUpdate instance) =>
    <String, dynamic>{
      'content': instance.content,
      'is_completed': instance.isCompleted,
    };
