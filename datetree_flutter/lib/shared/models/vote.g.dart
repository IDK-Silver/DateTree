// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'vote.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Vote _$VoteFromJson(Map<String, dynamic> json) => Vote(
      id: (json['id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      listItemId: (json['list_item_id'] as num).toInt(),
      value: (json['value'] as num).toInt(),
      createdAt: DateTime.parse(json['created_at'] as String),
    );

Map<String, dynamic> _$VoteToJson(Vote instance) => <String, dynamic>{
      'id': instance.id,
      'user_id': instance.userId,
      'list_item_id': instance.listItemId,
      'value': instance.value,
      'created_at': instance.createdAt.toIso8601String(),
    };

VoteCreate _$VoteCreateFromJson(Map<String, dynamic> json) => VoteCreate(
      listItemId: (json['list_item_id'] as num).toInt(),
      value: (json['value'] as num).toInt(),
    );

Map<String, dynamic> _$VoteCreateToJson(VoteCreate instance) =>
    <String, dynamic>{
      'list_item_id': instance.listItemId,
      'value': instance.value,
    };

VoteStats _$VoteStatsFromJson(Map<String, dynamic> json) => VoteStats(
      listItemId: (json['list_item_id'] as num).toInt(),
      totalVotes: (json['total_votes'] as num).toInt(),
      averageScore: (json['average_score'] as num).toDouble(),
      voteCount: (json['vote_count'] as num).toInt(),
    );

Map<String, dynamic> _$VoteStatsToJson(VoteStats instance) => <String, dynamic>{
      'list_item_id': instance.listItemId,
      'total_votes': instance.totalVotes,
      'average_score': instance.averageScore,
      'vote_count': instance.voteCount,
    };
