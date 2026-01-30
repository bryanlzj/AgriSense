import 'package:fyp_prototype/models/alert.dart';
import 'package:fyp_prototype/models/risk_status.dart';
import 'package:fyp_prototype/models/weather_data.dart';

class HomePageData {
  final String userName;
  final String username;
  final String location;
  final String cropType;
  final WeatherData? weatherData;
  final List<Alert> activeAlerts;
  final int totalUnreadAlerts;
  final RiskStatus? riskStatus;

  HomePageData({
    required this.userName,
    required this.username,
    required this.location,
    required this.cropType,
    this.weatherData,
    required this.activeAlerts,
    required this.totalUnreadAlerts,
    this.riskStatus,
  });

  /// Creates HomePageData from backend /dashboard response.
  factory HomePageData.fromDashboardResponse(Map<String, dynamic> json) {
    // Parse user info
    final user = json['user'] as Map<String, dynamic>? ?? {};
    final userName = user['full_name'] as String? ?? user['username'] as String? ?? 'User';
    final username = user['username'] as String? ?? '';
    final location = user['farm_location'] as String? ?? '';
    final cropType = user['crop_type'] as String? ?? '';

    // Parse weather
    WeatherData? weatherData;
    final weatherJson = json['weather'] as Map<String, dynamic>?;
    if (weatherJson != null && !weatherJson.containsKey('error')) {
      weatherData = WeatherData.fromJson(weatherJson);
    }

    // Parse alerts
    final alertsJson = json['alerts'] as Map<String, dynamic>? ?? {};
    final totalUnread = alertsJson['total_unread'] as int? ?? 0;
    final recentAlerts = (alertsJson['recent'] as List<dynamic>? ?? [])
        .map((alert) => Alert.fromJson(alert as Map<String, dynamic>))
        .toList();

    // Parse pest risk
    RiskStatus? riskStatus;
    final pestRiskJson = json['pest_risk'] as Map<String, dynamic>?;
    if (pestRiskJson != null) {
      riskStatus = RiskStatus.fromJson(pestRiskJson);
    }

    return HomePageData(
      userName: userName,
      username: username,
      location: location,
      cropType: cropType,
      weatherData: weatherData,
      activeAlerts: recentAlerts,
      totalUnreadAlerts: totalUnread,
      riskStatus: riskStatus,
    );
  }

  /// Legacy fromJson for backwards compatibility.
  factory HomePageData.fromJson(Map<String, dynamic> json) {
    return HomePageData.fromDashboardResponse(json);
  }
}
