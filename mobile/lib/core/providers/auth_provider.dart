import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:equatable/equatable.dart';

import '../../shared/models/user.dart';
import '../services/auth_service.dart';

class AuthState extends Equatable {
  final User? user;
  final bool isLoading;
  final bool isAuthenticated;
  final String? error;

  const AuthState({
    this.user,
    this.isLoading = false,
    this.isAuthenticated = false,
    this.error,
  });

  AuthState copyWith({
    User? user,
    bool? isLoading,
    bool? isAuthenticated,
    String? error,
  }) {
    return AuthState(
      user: user ?? this.user,
      isLoading: isLoading ?? this.isLoading,
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      error: error,
    );
  }

  @override
  List<Object?> get props => [user, isLoading, isAuthenticated, error];
}

class AuthNotifier extends StateNotifier<AuthState> {
  final AuthService _authService;

  AuthNotifier(this._authService) : super(const AuthState()) {
    print('🔐 AuthNotifier created');
    // Delay initial auth check to avoid provider initialization issues
    Future.microtask(() => _checkAuthStatus());
  }

  Future<void> _checkAuthStatus() async {
    state = state.copyWith(isLoading: true);
    
    try {
      final user = await _authService.getCurrentUser();
      state = state.copyWith(
        user: user,
        isAuthenticated: user != null,
        isLoading: false,
        error: null,
      );
    } catch (e) {
      state = state.copyWith(
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      );
    }
  }

  Future<bool> login({
    required String email,
    required String password,
  }) async {
    state = state.copyWith(isLoading: true, error: null);

    try {
      final result = await _authService.login(
        email: email,
        password: password,
      );

      if (result.isSuccess) {
        state = state.copyWith(
          user: result.user,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        );
        return true;
      } else {
        state = state.copyWith(
          isLoading: false,
          error: result.error,
        );
        return false;
      }
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'An unexpected error occurred',
      );
      return false;
    }
  }

  Future<bool> register({
    required String email,
    required String password,
    required String fullName,
  }) async {
    state = state.copyWith(isLoading: true, error: null);

    try {
      final result = await _authService.register(
        email: email,
        password: password,
        fullName: fullName,
      );

      if (result.isSuccess) {
        state = state.copyWith(
          user: result.user,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        );
        return true;
      } else {
        state = state.copyWith(
          isLoading: false,
          error: result.error,
        );
        return false;
      }
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'An unexpected error occurred',
      );
      return false;
    }
  }

  Future<void> logout() async {
    state = state.copyWith(isLoading: true);
    
    try {
      await _authService.logout();
    } catch (e) {
      // Continue with logout even if API call fails
    }
    
    state = const AuthState(
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
    );
  }

  void clearError() {
    state = state.copyWith(error: null);
  }
}

final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  final authService = ref.watch(authServiceProvider);
  return AuthNotifier(authService);
});