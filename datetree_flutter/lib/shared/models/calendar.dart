import 'package:json_annotation/json_annotation.dart';
import 'package:equatable/equatable.dart';

part 'calendar.g.dart';

@JsonSerializable()
class Calendar extends Equatable {
  final int id;
  final String name;
  final String? description;
  @JsonKey(name: 'owner_id')
  final int ownerId;
  @JsonKey(name: 'created_at')
  final DateTime createdAt;

  const Calendar({
    required this.id,
    required this.name,
    this.description,
    required this.ownerId,
    required this.createdAt,
  });

  factory Calendar.fromJson(Map<String, dynamic> json) => _$CalendarFromJson(json);
  Map<String, dynamic> toJson() => _$CalendarToJson(this);

  @override
  List<Object?> get props => [id, name, description, ownerId, createdAt];
}

@JsonSerializable()
class CalendarCreate extends Equatable {
  final String name;
  final String? description;

  const CalendarCreate({
    required this.name,
    this.description,
  });

  factory CalendarCreate.fromJson(Map<String, dynamic> json) => _$CalendarCreateFromJson(json);
  Map<String, dynamic> toJson() => _$CalendarCreateToJson(this);

  @override
  List<Object?> get props => [name, description];
}

enum UserRole {
  @JsonValue('owner')
  owner,
  @JsonValue('editor')
  editor,
  @JsonValue('viewer')
  viewer,
}

@JsonSerializable()
class UserCalendar extends Equatable {
  @JsonKey(name: 'user_id')
  final int userId;
  @JsonKey(name: 'calendar_id')
  final int calendarId;
  final UserRole role;
  @JsonKey(name: 'joined_at')
  final DateTime joinedAt;

  const UserCalendar({
    required this.userId,
    required this.calendarId,
    required this.role,
    required this.joinedAt,
  });

  factory UserCalendar.fromJson(Map<String, dynamic> json) => _$UserCalendarFromJson(json);
  Map<String, dynamic> toJson() => _$UserCalendarToJson(this);

  @override
  List<Object?> get props => [userId, calendarId, role, joinedAt];
}