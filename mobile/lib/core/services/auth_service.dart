import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../shared/models/user.dart';
import '../../shared/models/api_response.dart';
import 'api_client.dart';
import 'dio_client.dart';

class AuthService {
  final ApiClient _apiClient;
  final DioClient _dioClient;

  AuthService(this._apiClient, this._dioClient);

  Future<AuthResult> register({
    required String email,
    required String password,
    required String fullName,
  }) async {
    try {
      final userCreate = UserCreate(
        email: email,
        password: password,
        fullName: fullName,
      );

      final response = await _apiClient.register(userCreate);
      await _dioClient.setToken(response.accessToken);

      // Get user information after setting token
      final user = await _apiClient.getCurrentUser();

      return AuthResult.success(
        user: user,
        token: response.accessToken,
      );
    } on DioException catch (e) {
      return AuthResult.failure(_handleDioError(e));
    } catch (e) {
      return AuthResult.failure('Unexpected error occurred');
    }
  }

  Future<AuthResult> login({
    required String email,
    required String password,
  }) async {
    try {
      final response = await _apiClient.login(email, password);
      await _dioClient.setToken(response.accessToken);

      // Get user information after setting token
      final user = await _apiClient.getCurrentUser();

      return AuthResult.success(
        user: user,
        token: response.accessToken,
      );
    } on DioException catch (e) {
      return AuthResult.failure(_handleDioError(e));
    } catch (e) {
      return AuthResult.failure('Unexpected error occurred');
    }
  }

  Future<void> logout() async {
    try {
      await _apiClient.logout();
    } catch (e) {
      // Continue with logout even if API call fails
    } finally {
      await _dioClient.clearToken();
    }
  }

  Future<User?> getCurrentUser() async {
    try {
      final hasToken = await _dioClient.hasToken();
      if (!hasToken) return null;

      return await _apiClient.getCurrentUser();
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        await _dioClient.clearToken();
      }
      return null;
    } catch (e) {
      return null;
    }
  }

  Future<bool> isLoggedIn() async {
    return await _dioClient.hasToken();
  }

  String _handleDioError(DioException e) {
    if (e.response?.data != null) {
      try {
        final errorResponse = ErrorResponse.fromJson(e.response!.data);
        return errorResponse.detail;
      } catch (_) {
        // Fall through to default handling
      }
    }

    switch (e.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return 'Connection timeout. Please check your internet connection.';
      case DioExceptionType.badResponse:
        switch (e.response?.statusCode) {
          case 400:
            return 'Invalid request. Please check your input.';
          case 401:
            return 'Invalid email or password.';
          case 403:
            return 'Access denied.';
          case 404:
            return 'Service not found.';
          case 500:
            return 'Server error. Please try again later.';
          default:
            return 'Request failed with status ${e.response?.statusCode}';
        }
      case DioExceptionType.cancel:
        return 'Request was cancelled.';
      case DioExceptionType.unknown:
        return 'Network error. Please check your connection.';
      default:
        return 'An unexpected error occurred.';
    }
  }
}

class AuthResult {
  final bool isSuccess;
  final User? user;
  final String? token;
  final String? error;

  const AuthResult._({
    required this.isSuccess,
    this.user,
    this.token,
    this.error,
  });

  factory AuthResult.success({
    required User user,
    required String token,
  }) {
    return AuthResult._(
      isSuccess: true,
      user: user,
      token: token,
    );
  }

  factory AuthResult.failure(String error) {
    return AuthResult._(
      isSuccess: false,
      error: error,
    );
  }
}

// Providers
final dioClientProvider = Provider<DioClient>((ref) {
  return DioClient();
});

final apiClientProvider = Provider<ApiClient>((ref) {
  final dioClient = ref.watch(dioClientProvider);
  return ApiClient(dioClient.dio);
});

final authServiceProvider = Provider<AuthService>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  final dioClient = ref.watch(dioClientProvider);
  return AuthService(apiClient, dioClient);
});