import 'package:fyp_prototype/models/alert.dart';
import 'package:fyp_prototype/models/risk_status.dart';
import 'package:fyp_prototype/models/weather_data.dart';

class HomePageData {
  final String userName;
  final String location;
  final WeatherData weatherData;
  final List<Alert> activeAlerts;
  final RiskStatus riskStatus;

  HomePageData({
    required this.userName,
    required this.location,
    required this.weatherData,
    required this.activeAlerts,
    required this.riskStatus,
  });

  factory HomePageData.fromJson(Map<String, dynamic> json) {
    return HomePageData(
      userName: json['userName'],
      location: json['location'],
      weatherData: WeatherData.fromJson(json['weatherData']),
      activeAlerts: (json['activeAlerts'] as List)
          .map((alert) => Alert.fromJson(alert))
          .toList(),
      riskStatus: RiskStatus.fromJson(json['riskStatus']),
    );
  }
}
