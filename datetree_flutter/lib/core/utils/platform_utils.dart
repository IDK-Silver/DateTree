import 'package:flutter/foundation.dart';

class PlatformUtils {
  PlatformUtils._();

  static bool get isWeb => kIsWeb;
  static bool get isAndroid => !kIsWeb && defaultTargetPlatform == TargetPlatform.android;
  static bool get isIOS => !kIsWeb && defaultTargetPlatform == TargetPlatform.iOS;
  static bool get isMobile => isAndroid || isIOS;
  static bool get isDesktop => !kIsWeb && (
    defaultTargetPlatform == TargetPlatform.windows ||
    defaultTargetPlatform == TargetPlatform.linux ||
    defaultTargetPlatform == TargetPlatform.macOS
  );

  /// Returns optimized debounce duration for the current platform
  static Duration get validationDebounce {
    if (isWeb) {
      return const Duration(milliseconds: 500); // Longer delay for web to prevent freezing
    }
    return const Duration(milliseconds: 300);
  }

  /// Returns whether to use autovalidate mode for forms
  static bool get shouldUseAutovalidate {
    return !isWeb; // Disable auto-validation on web to prevent performance issues
  }
}