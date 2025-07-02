// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'event.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Event _$EventFromJson(Map<String, dynamic> json) => Event(
      id: (json['id'] as num).toInt(),
      title: json['title'] as String,
      description: json['description'] as String?,
      startTime: DateTime.parse(json['start_time'] as String),
      endTime: json['end_time'] == null
          ? null
          : DateTime.parse(json['end_time'] as String),
      isAllDay: json['is_all_day'] as bool,
      calendarId: (json['calendar_id'] as num).toInt(),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$EventToJson(Event instance) => <String, dynamic>{
      'id': instance.id,
      'title': instance.title,
      'description': instance.description,
      'start_time': instance.startTime.toIso8601String(),
      'end_time': instance.endTime?.toIso8601String(),
      'is_all_day': instance.isAllDay,
      'calendar_id': instance.calendarId,
      'created_at': instance.createdAt.toIso8601String(),
    };

EventCreate _$EventCreateFromJson(Map<String, dynamic> json) => EventCreate(
      title: json['title'] as String,
      description: json['description'] as String?,
      startTime: DateTime.parse(json['start_time'] as String),
      endTime: json['end_time'] == null
          ? null
          : DateTime.parse(json['end_time'] as String),
      isAllDay: json['is_all_day'] as bool,
      calendarId: (json['calendar_id'] as num).toInt(),
    );

Map<String, dynamic> _$EventCreateToJson(EventCreate instance) =>
    <String, dynamic>{
      'title': instance.title,
      'description': instance.description,
      'start_time': instance.startTime.toIso8601String(),
      'end_time': instance.endTime?.toIso8601String(),
      'is_all_day': instance.isAllDay,
      'calendar_id': instance.calendarId,
    };

EventUpdate _$EventUpdateFromJson(Map<String, dynamic> json) => EventUpdate(
      title: json['title'] as String?,
      description: json['description'] as String?,
      startTime: json['start_time'] == null
          ? null
          : DateTime.parse(json['start_time'] as String),
      endTime: json['end_time'] == null
          ? null
          : DateTime.parse(json['end_time'] as String),
      isAllDay: json['is_all_day'] as bool?,
    );

Map<String, dynamic> _$EventUpdateToJson(EventUpdate instance) =>
    <String, dynamic>{
      'title': instance.title,
      'description': instance.description,
      'start_time': instance.startTime?.toIso8601String(),
      'end_time': instance.endTime?.toIso8601String(),
      'is_all_day': instance.isAllDay,
    };
