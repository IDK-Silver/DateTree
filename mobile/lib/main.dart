import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';

import 'core/constants/app_constants.dart';
import 'core/providers/router_provider.dart';
import 'core/theme/app_theme.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  print('🚀 DateTree App Starting...');
  
  // Initialize Hive for local storage (skip on web for now)
  try {
    if (!kIsWeb) {
      await Hive.initFlutter();
      print('✅ Hive initialized successfully');
    } else {
      print('⏭️ Skipping Hive initialization on web');
    }
  } catch (e) {
    print('❌ Hive initialization error: $e');
  }
  
  runApp(
    const ProviderScope(
      child: DateTreeApp(),
    ),
  );
  
  print('✅ DateTree App Started');
}

class DateTreeApp extends ConsumerWidget {
  const DateTreeApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    print('🔄 Building DateTreeApp...');
    
    try {
      final router = ref.watch(routerProvider);
      print('✅ Router initialized');
      
      return MaterialApp.router(
        title: AppConstants.appName,
        theme: AppTheme.lightTheme,
        darkTheme: AppTheme.darkTheme,
        themeMode: ThemeMode.system,
        routerConfig: router,
        debugShowCheckedModeBanner: false,
        builder: (context, child) {
          print('🏗️ Building app with child: ${child.runtimeType}');
          
          // Error widget builder for better error display
          ErrorWidget.builder = (FlutterErrorDetails details) {
            return Scaffold(
              body: Center(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(
                        Icons.error_outline,
                        color: Colors.red,
                        size: 60,
                      ),
                      const SizedBox(height: 16),
                      const Text(
                        'Oops! Something went wrong',
                        style: TextStyle(fontSize: 18),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        details.exception.toString(),
                        style: const TextStyle(color: Colors.grey),
                        textAlign: TextAlign.center,
                      ),
                    ],
                  ),
                ),
              ),
            );
          };
          
          return child ?? const SizedBox.shrink();
        },
      );
    } catch (e, stack) {
      print('❌ Error building app: $e');
      print('Stack trace: $stack');
      
      return MaterialApp(
        home: Scaffold(
          body: Center(
            child: Text('Error: $e'),
          ),
        ),
      );
    }
  }
}