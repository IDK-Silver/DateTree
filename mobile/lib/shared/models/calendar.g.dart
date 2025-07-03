// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'calendar.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Calendar _$CalendarFromJson(Map<String, dynamic> json) => Calendar(
      id: (json['id'] as num).toInt(),
      name: json['name'] as String,
      description: json['description'] as String?,
      calendarType: $enumDecode(_$CalendarTypeEnumMap, json['calendar_type']),
      ownerId: (json['owner_id'] as num).toInt(),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$CalendarToJson(Calendar instance) => <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'description': instance.description,
      'calendar_type': _$CalendarTypeEnumMap[instance.calendarType]!,
      'owner_id': instance.ownerId,
      'created_at': instance.createdAt.toIso8601String(),
    };

const _$CalendarTypeEnumMap = {
  CalendarType.personal: 'PERSONAL',
  CalendarType.general: 'GENERAL',
};

CalendarCreate _$CalendarCreateFromJson(Map<String, dynamic> json) =>
    CalendarCreate(
      name: json['name'] as String,
      description: json['description'] as String?,
    );

Map<String, dynamic> _$CalendarCreateToJson(CalendarCreate instance) =>
    <String, dynamic>{
      'name': instance.name,
      'description': instance.description,
    };

UserCalendar _$UserCalendarFromJson(Map<String, dynamic> json) => UserCalendar(
      userId: (json['user_id'] as num).toInt(),
      calendarId: (json['calendar_id'] as num).toInt(),
      role: $enumDecode(_$UserRoleEnumMap, json['role']),
      joinedAt: DateTime.parse(json['joined_at'] as String),
    );

Map<String, dynamic> _$UserCalendarToJson(UserCalendar instance) =>
    <String, dynamic>{
      'user_id': instance.userId,
      'calendar_id': instance.calendarId,
      'role': _$UserRoleEnumMap[instance.role]!,
      'joined_at': instance.joinedAt.toIso8601String(),
    };

const _$UserRoleEnumMap = {
  UserRole.owner: 'owner',
  UserRole.editor: 'editor',
  UserRole.viewer: 'viewer',
};
