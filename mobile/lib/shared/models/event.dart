import 'package:json_annotation/json_annotation.dart';
import 'package:equatable/equatable.dart';

part 'event.g.dart';

@JsonSerializable()
class Event extends Equatable {
  final int id;
  final String title;
  final String? description;
  @JsonKey(name: 'start_time')
  final DateTime startTime;
  @JsonKey(name: 'end_time')
  final DateTime? endTime;
  @JsonKey(name: 'is_all_day')
  final bool isAllDay;
  @JsonKey(name: 'calendar_id')
  final int calendarId;
  @JsonKey(name: 'created_at')
  final DateTime createdAt;

  const Event({
    required this.id,
    required this.title,
    this.description,
    required this.startTime,
    this.endTime,
    required this.isAllDay,
    required this.calendarId,
    required this.createdAt,
  });

  factory Event.fromJson(Map<String, dynamic> json) => _$EventFromJson(json);
  Map<String, dynamic> toJson() => _$EventToJson(this);

  @override
  List<Object?> get props => [id, title, description, startTime, endTime, isAllDay, calendarId, createdAt];
}

@JsonSerializable()
class EventCreate extends Equatable {
  final String title;
  final String? description;
  @JsonKey(name: 'start_time')
  final DateTime startTime;
  @JsonKey(name: 'end_time')
  final DateTime? endTime;
  @JsonKey(name: 'is_all_day')
  final bool isAllDay;
  @JsonKey(name: 'calendar_id')
  final int calendarId;

  const EventCreate({
    required this.title,
    this.description,
    required this.startTime,
    this.endTime,
    required this.isAllDay,
    required this.calendarId,
  });

  factory EventCreate.fromJson(Map<String, dynamic> json) => _$EventCreateFromJson(json);
  Map<String, dynamic> toJson() => _$EventCreateToJson(this);

  @override
  List<Object?> get props => [title, description, startTime, endTime, isAllDay, calendarId];
}

@JsonSerializable()
class EventUpdate extends Equatable {
  final String? title;
  final String? description;
  @JsonKey(name: 'start_time')
  final DateTime? startTime;
  @JsonKey(name: 'end_time')
  final DateTime? endTime;
  @JsonKey(name: 'is_all_day')
  final bool? isAllDay;

  const EventUpdate({
    this.title,
    this.description,
    this.startTime,
    this.endTime,
    this.isAllDay,
  });

  factory EventUpdate.fromJson(Map<String, dynamic> json) => _$EventUpdateFromJson(json);
  Map<String, dynamic> toJson() => _$EventUpdateToJson(this);

  @override
  List<Object?> get props => [title, description, startTime, endTime, isAllDay];
}