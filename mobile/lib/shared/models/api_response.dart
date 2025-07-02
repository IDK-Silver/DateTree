import 'package:json_annotation/json_annotation.dart';
import 'package:equatable/equatable.dart';

part 'api_response.g.dart';

@JsonSerializable(genericArgumentFactories: true)
class ApiResponse<T> extends Equatable {
  final bool success;
  final String? message;
  final T? data;
  final Map<String, dynamic>? errors;

  const ApiResponse({
    required this.success,
    this.message,
    this.data,
    this.errors,
  });

  factory ApiResponse.fromJson(
    Map<String, dynamic> json,
    T Function(Object? json) fromJsonT,
  ) =>
      _$ApiResponseFromJson(json, fromJsonT);

  Map<String, dynamic> toJson(Object? Function(T value) toJsonT) =>
      _$ApiResponseToJson(this, toJsonT);

  @override
  List<Object?> get props => [success, message, data, errors];
}

@JsonSerializable()
class AuthResponse extends Equatable {
  @JsonKey(name: 'access_token')
  final String accessToken;
  @JsonKey(name: 'token_type')
  final String tokenType;
  final Map<String, dynamic>? user;

  const AuthResponse({
    required this.accessToken,
    required this.tokenType,
    this.user,
  });

  factory AuthResponse.fromJson(Map<String, dynamic> json) => _$AuthResponseFromJson(json);
  Map<String, dynamic> toJson() => _$AuthResponseToJson(this);

  @override
  List<Object?> get props => [accessToken, tokenType, user];
}

@JsonSerializable()
class ErrorResponse extends Equatable {
  final String detail;
  final String? type;
  final Map<String, dynamic>? errors;

  const ErrorResponse({
    required this.detail,
    this.type,
    this.errors,
  });

  factory ErrorResponse.fromJson(Map<String, dynamic> json) => _$ErrorResponseFromJson(json);
  Map<String, dynamic> toJson() => _$ErrorResponseToJson(this);

  @override
  List<Object?> get props => [detail, type, errors];
}