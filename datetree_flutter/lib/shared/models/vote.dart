import 'package:json_annotation/json_annotation.dart';
import 'package:equatable/equatable.dart';

part 'vote.g.dart';

@JsonSerializable()
class Vote extends Equatable {
  final int id;
  @JsonKey(name: 'user_id')
  final int userId;
  @JsonKey(name: 'list_item_id')
  final int listItemId;
  final int value;
  @JsonKey(name: 'created_at')
  final DateTime createdAt;

  const Vote({
    required this.id,
    required this.userId,
    required this.listItemId,
    required this.value,
    required this.createdAt,
  });

  factory Vote.fromJson(Map<String, dynamic> json) => _$VoteFromJson(json);
  Map<String, dynamic> toJson() => _$VoteToJson(this);

  @override
  List<Object?> get props => [id, userId, listItemId, value, createdAt];
}

@JsonSerializable()
class VoteCreate extends Equatable {
  @JsonKey(name: 'list_item_id')
  final int listItemId;
  final int value;

  const VoteCreate({
    required this.listItemId,
    required this.value,
  });

  factory VoteCreate.fromJson(Map<String, dynamic> json) => _$VoteCreateFromJson(json);
  Map<String, dynamic> toJson() => _$VoteCreateToJson(this);

  @override
  List<Object?> get props => [listItemId, value];
}

@JsonSerializable()
class VoteStats extends Equatable {
  @JsonKey(name: 'list_item_id')
  final int listItemId;
  @JsonKey(name: 'total_votes')
  final int totalVotes;
  @JsonKey(name: 'average_score')
  final double averageScore;
  @JsonKey(name: 'vote_count')
  final int voteCount;

  const VoteStats({
    required this.listItemId,
    required this.totalVotes,
    required this.averageScore,
    required this.voteCount,
  });

  factory VoteStats.fromJson(Map<String, dynamic> json) => _$VoteStatsFromJson(json);
  Map<String, dynamic> toJson() => _$VoteStatsToJson(this);

  @override
  List<Object?> get props => [listItemId, totalVotes, averageScore, voteCount];
}