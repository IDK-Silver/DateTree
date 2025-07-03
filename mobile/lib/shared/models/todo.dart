import 'package:json_annotation/json_annotation.dart';
import 'package:equatable/equatable.dart';

part 'todo.g.dart';

enum ListType {
  @JsonValue('TODO')
  todo,
  @JsonValue('PRIORITY')
  priority,
}

@JsonSerializable()
class TodoList extends Equatable {
  final int id;
  final String name;
  final String? description;
  @JsonKey(name: 'list_type')
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
  @JsonKey(name: 'list_type')
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
  final String content;
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

  const ListItem({
    required this.id,
    required this.content,
    required this.isCompleted,
    required this.listId,
    this.creatorId,
    required this.createdAt,
    this.voteCount,
  });

  factory ListItem.fromJson(Map<String, dynamic> json) => _$ListItemFromJson(json);
  Map<String, dynamic> toJson() => _$ListItemToJson(this);

  ListItem copyWith({
    int? id,
    String? content,
    bool? isCompleted,
    int? listId,
    int? creatorId,
    DateTime? createdAt,
    int? voteCount,
  }) {
    return ListItem(
      id: id ?? this.id,
      content: content ?? this.content,
      isCompleted: isCompleted ?? this.isCompleted,
      listId: listId ?? this.listId,
      creatorId: creatorId ?? this.creatorId,
      createdAt: createdAt ?? this.createdAt,
      voteCount: voteCount ?? this.voteCount,
    );
  }

  @override
  List<Object?> get props => [id, content, isCompleted, listId, creatorId, createdAt, voteCount];
}

@JsonSerializable()
class ListItemCreate extends Equatable {
  final String content;
  @JsonKey(name: 'list_id')
  final int listId;

  const ListItemCreate({
    required this.content,
    required this.listId,
  });

  factory ListItemCreate.fromJson(Map<String, dynamic> json) => _$ListItemCreateFromJson(json);
  Map<String, dynamic> toJson() => _$ListItemCreateToJson(this);

  @override
  List<Object?> get props => [content, listId];
}

@JsonSerializable()
class ListItemUpdate extends Equatable {
  final String? content;
  @JsonKey(name: 'is_completed')
  final bool? isCompleted;

  const ListItemUpdate({
    this.content,
    this.isCompleted,
  });

  factory ListItemUpdate.fromJson(Map<String, dynamic> json) => _$ListItemUpdateFromJson(json);
  Map<String, dynamic> toJson() => _$ListItemUpdateToJson(this);

  @override
  List<Object?> get props => [content, isCompleted];
}