import 'package:json_annotation/json_annotation.dart';
import 'package:equatable/equatable.dart';

part 'user.g.dart';

@JsonSerializable()
class User extends Equatable {
  final int id;
  final String email;
  @JsonKey(name: 'full_name')
  final String? fullName;
  @JsonKey(name: 'is_active')
  final bool isActive;
  @JsonKey(name: 'created_at')
  final DateTime? createdAt;

  const User({
    required this.id,
    required this.email,
    this.fullName,
    required this.isActive,
    this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);

  @override
  List<Object?> get props => [id, email, fullName, isActive, createdAt];
}

@JsonSerializable()
class UserCreate extends Equatable {
  final String email;
  final String password;
  @JsonKey(name: 'full_name')
  final String fullName;

  const UserCreate({
    required this.email,
    required this.password,
    required this.fullName,
  });

  factory UserCreate.fromJson(Map<String, dynamic> json) => _$UserCreateFromJson(json);
  Map<String, dynamic> toJson() => _$UserCreateToJson(this);

  @override
  List<Object?> get props => [email, password, fullName];
}

@JsonSerializable()
class UserLogin extends Equatable {
  final String email;
  final String password;

  const UserLogin({
    required this.email,
    required this.password,
  });

  factory UserLogin.fromJson(Map<String, dynamic> json) => _$UserLoginFromJson(json);
  Map<String, dynamic> toJson() => _$UserLoginToJson(this);

  @override
  List<Object?> get props => [email, password];
}