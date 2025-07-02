import 'package:json_annotation/json_annotation.dart';
import 'package:equatable/equatable.dart';

part 'todo.g.dart';

enum ListType {
  @JsonValue('todo')
  todo,
  @JsonValue('priority')
  priority,
  @JsonValue('checklist')
  checklist,
}

@JsonSerializable()
class TodoList extends Equatable {
  final int id;
  final String name;
  final String? description;
  final ListType type;
  @JsonKey(name: 'calendar_id')
  final int calendarId;
  @JsonKey(name: 'created_at')
  final DateTime createdAt;

  const TodoList({
    required this.id,
    required this.name,
    this.description,
    required this.type,
    required this.calendarId,
    required this.createdAt,
  });

  factory TodoList.fromJson(Map<String, dynamic> json) => _$TodoListFromJson(json);
  Map<String, dynamic> toJson() => _$TodoListToJson(this);

  @override
  List<Object?> get props => [id, name, description, type, calendarId, createdAt];
}

@JsonSerializable()
class TodoListCreate extends Equatable {
  final String name;
  final String? description;
  final ListType type;
  @JsonKey(name: 'calendar_id')
  final int calendarId;

  const TodoListCreate({
    required this.name,
    this.description,
    required this.type,
    required this.calendarId,
  });

  factory TodoListCreate.fromJson(Map<String, dynamic> json) => _$TodoListCreateFromJson(json);
  Map<String, dynamic> toJson() => _$TodoListCreateToJson(this);

  @override
  List<Object?> get props => [name, description, type, calendarId];
}

@JsonSerializable()
class ListItem extends Equatable {
  final int id;
  final String title;
  final String? description;
  @JsonKey(name: 'due_date')
  final DateTime? dueDate;
  @JsonKey(name: 'is_completed')
  final bool isCompleted;
  @JsonKey(name: 'list_id')
  final int listId;
  @JsonKey(name: 'created_at')
  final DateTime createdAt;
  @JsonKey(name: 'completed_at')
  final DateTime? completedAt;

  const ListItem({
    required this.id,
    required this.title,
    this.description,
    this.dueDate,
    required this.isCompleted,
    required this.listId,
    required this.createdAt,
    this.completedAt,
  });

  factory ListItem.fromJson(Map<String, dynamic> json) => _$ListItemFromJson(json);
  Map<String, dynamic> toJson() => _$ListItemToJson(this);

  ListItem copyWith({
    int? id,
    String? title,
    String? description,
    DateTime? dueDate,
    bool? isCompleted,
    int? listId,
    DateTime? createdAt,
    DateTime? completedAt,
  }) {
    return ListItem(
      id: id ?? this.id,
      title: title ?? this.title,
      description: description ?? this.description,
      dueDate: dueDate ?? this.dueDate,
      isCompleted: isCompleted ?? this.isCompleted,
      listId: listId ?? this.listId,
      createdAt: createdAt ?? this.createdAt,
      completedAt: completedAt ?? this.completedAt,
    );
  }

  @override
  List<Object?> get props => [id, title, description, dueDate, isCompleted, listId, createdAt, completedAt];
}

@JsonSerializable()
class ListItemCreate extends Equatable {
  final String title;
  final String? description;
  @JsonKey(name: 'due_date')
  final DateTime? dueDate;
  @JsonKey(name: 'list_id')
  final int listId;

  const ListItemCreate({
    required this.title,
    this.description,
    this.dueDate,
    required this.listId,
  });

  factory ListItemCreate.fromJson(Map<String, dynamic> json) => _$ListItemCreateFromJson(json);
  Map<String, dynamic> toJson() => _$ListItemCreateToJson(this);

  @override
  List<Object?> get props => [title, description, dueDate, listId];
}

@JsonSerializable()
class ListItemUpdate extends Equatable {
  final String? title;
  final String? description;
  @JsonKey(name: 'due_date')
  final DateTime? dueDate;
  @JsonKey(name: 'is_completed')
  final bool? isCompleted;

  const ListItemUpdate({
    this.title,
    this.description,
    this.dueDate,
    this.isCompleted,
  });

  factory ListItemUpdate.fromJson(Map<String, dynamic> json) => _$ListItemUpdateFromJson(json);
  Map<String, dynamic> toJson() => _$ListItemUpdateToJson(this);

  @override
  List<Object?> get props => [title, description, dueDate, isCompleted];
}