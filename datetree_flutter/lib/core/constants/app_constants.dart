class AppConstants {
  AppConstants._();

  static const String appName = 'DateTree';
  static const String apiBaseUrl = 'http://127.0.0.1:8000/api/v1';
  
  static const int maxRetries = 3;
  static const Duration connectionTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
  
  static const int coldStartTargetMs = 3000;
  static const int responseTimeTargetMs = 200;
}