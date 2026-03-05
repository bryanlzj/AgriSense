/// API configuration constants for different environments.
class ApiConstants {
  // Base URL detection for different environments
  static const String androidEmulator = 'http://10.0.2.2:8000';
  static const String iosSimulator = 'http://localhost:8000';

  // Change this for physical device testing
  static const String physicalDevice = 'http://192.168.1.100:8000';

  // Production server
  static const String production = 'https://agrisense.bryanlzj.work';

  // Current active base URL (change as needed)
  static const String baseUrl = production;

  // API version prefix
  static const String apiPrefix = '/api/v1';

  // Auth endpoints
  static const String login = '$apiPrefix/auth/login';
  static const String register = '$apiPrefix/auth/register';
  static const String me = '$apiPrefix/auth/me';

  // Dashboard endpoints
  static const String dashboard = '$apiPrefix/dashboard';
  static const String dashboardQuick = '$apiPrefix/dashboard/quick';

  // Weather endpoints
  static const String weatherCurrent = '$apiPrefix/weather/current';
  static const String weatherForecast = '$apiPrefix/weather/forecast';
  static const String weatherSummary = '$apiPrefix/weather/summary';
  static const String weatherHistorical = '$apiPrefix/weather/historical';

  // Alert endpoints (note: trailing slash required for list endpoint)
  static const String alerts = '$apiPrefix/alert/';
  static const String alertsBulk = '$apiPrefix/alert/bulk';
  static const String alertsStats = '$apiPrefix/alert/stats/summary';

  // Sector endpoints
  static const String sectors = '$apiPrefix/sector/';
  static const String sectorStats = '$apiPrefix/sector/stats/summary';

  // Pest detection endpoints
  static const String pestDetect = '$apiPrefix/pest/detect';
  static const String pestDetectEnhanced = '$apiPrefix/pest/detect/enhanced';
  static const String pestList = '$apiPrefix/pest/';
  static const String pestStats = '$apiPrefix/pest/stats/summary';
  static const String pestRisk = '$apiPrefix/pest/risk';
  static const String pestRiskSummary = '$apiPrefix/pest/risk/summary';

  // Chat endpoints
  static const String chatMessage = '$apiPrefix/chat/message';
  static const String chatImage = '$apiPrefix/chat/image';
  static const String chatStatus = '$apiPrefix/chat/status';
}
