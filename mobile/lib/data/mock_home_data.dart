import 'package:fyp_prototype/models/alert.dart';
import 'package:fyp_prototype/models/home_page_data.dart';
import 'package:fyp_prototype/models/risk_status.dart';
import 'package:fyp_prototype/models/weather_data.dart';

final HomePageData mockData = HomePageData(
  userName: "Ahmad",
  location: "Selangor, Malaysia",
  weatherData: WeatherData(
    temperature: 30.0,
    condition: "Sunny",
    icon: "☀️",
    windSpeed: 5.0,
    humidity: 60.0,
  ),
  activeAlerts: [
    Alert(
      title: "Heavy Rain Warning",
      message: "Expected thunderstorms in the evening.",
      timeAgo: "2h ago",
      severity: "High",
    ),
  ],
  riskStatus: RiskStatus(
    weatherRisk: "Low",
    pestRisk: "Medium",
  ),
);