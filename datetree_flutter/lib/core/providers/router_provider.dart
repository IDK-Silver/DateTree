import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../features/auth/screens/login_screen.dart';
import '../../features/auth/screens/register_screen.dart';
import '../../features/calendar/screens/calendar_screen.dart';
import '../../features/profile/screens/profile_screen.dart';
import '../../features/todo/screens/todo_screen.dart';
import '../../features/vote/screens/vote_screen.dart';
import '../../shared/widgets/templates/main_layout.dart';
import 'auth_provider.dart';

final routerProvider = Provider<GoRouter>((ref) {
  print('🔄 Creating router...');
  final authState = ref.watch(authProvider);
  print('📱 Auth state: isAuthenticated=${authState.isAuthenticated}, isLoading=${authState.isLoading}');
  
  return GoRouter(
    initialLocation: authState.isAuthenticated ? '/todo' : '/login',
    redirect: (context, state) {
      final isAuthenticated = authState.isAuthenticated;
      final isLoading = authState.isLoading;
      
      // Don't redirect while loading
      if (isLoading) return null;
      
      final isOnAuthPage = state.uri.path == '/login' || state.uri.path == '/register';
      
      // Redirect to login if not authenticated and not on auth page
      if (!isAuthenticated && !isOnAuthPage) {
        return '/login';
      }
      
      // Redirect to main app if authenticated and on auth page
      if (isAuthenticated && isOnAuthPage) {
        return '/todo';
      }
      
      return null;
    },
    routes: [
      ShellRoute(
        builder: (context, state, child) => MainLayout(child: child),
        routes: [
          GoRoute(
            path: '/todo',
            name: 'todo',
            builder: (context, state) => const TodoScreen(),
          ),
          GoRoute(
            path: '/vote',
            name: 'vote',
            builder: (context, state) => const VoteScreen(),
          ),
          GoRoute(
            path: '/calendar',
            name: 'calendar',
            builder: (context, state) => const CalendarScreen(),
          ),
          GoRoute(
            path: '/profile',
            name: 'profile',
            builder: (context, state) => const ProfileScreen(),
          ),
        ],
      ),
      GoRoute(
        path: '/login',
        name: 'login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/register',
        name: 'register',
        builder: (context, state) => const RegisterScreen(),
      ),
    ],
    errorBuilder: (context, state) => Scaffold(
      body: Center(
        child: Text('Error: ${state.error}'),
      ),
    ),
  );
});