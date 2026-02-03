import 'package:flutter/material.dart';

class WeatherData {
  final double temperature;
  final int humidity;
  final String weatherMain;
  final String weatherDescription;
  final double feelsLike;
  final double windSpeed;
  final String location;

  WeatherData({
    required this.temperature,
    required this.humidity,
    required this.weatherMain,
    required this.weatherDescription,
    required this.feelsLike,
    required this.windSpeed,
    required this.location,
  });

  /// Creates WeatherData from backend API response.
  factory WeatherData.fromJson(Map<String, dynamic> json) {
    return WeatherData(
      temperature: (json['temperature'] as num?)?.toDouble() ?? 0.0,
      humidity: (json['humidity'] as num?)?.toInt() ?? 0,
      weatherMain: json['weather_main'] as String? ?? 'Unknown',
      weatherDescription: json['weather_description'] as String? ?? '',
      feelsLike: (json['feels_like'] as num?)?.toDouble() ?? 0.0,
      windSpeed: (json['wind_speed'] as num?)?.toDouble() ?? 0.0,
      location: json['location'] as String? ?? '',
    );
  }

  /// Returns an icon based on weather condition.
  IconData get iconData {
    switch (weatherMain.toLowerCase()) {
      case 'clear':
      case 'sunny':
        return Icons.wb_sunny;
      case 'clouds':
      case 'cloudy':
      case 'partly cloudy':
      case 'overcast':
        return Icons.cloud;
      case 'rain':
      case 'drizzle':
      case 'light rain':
      case 'moderate rain':
      case 'heavy rain':
        return Icons.water_drop;
      case 'thunderstorm':
        return Icons.thunderstorm;
      case 'snow':
        return Icons.ac_unit;
      case 'mist':
      case 'fog':
      case 'haze':
      case 'foggy':
        return Icons.foggy;
      default:
        return Icons.wb_cloudy;
    }
  }

  /// Returns a color for the weather icon.
  Color get iconColor {
    switch (weatherMain.toLowerCase()) {
      case 'clear':
      case 'sunny':
        return const Color(0xFFFFB300); // Amber/Yellow for sun
      case 'clouds':
      case 'cloudy':
      case 'partly cloudy':
      case 'overcast':
        return const Color(0xFF78909C); // Blue grey for clouds
      case 'rain':
      case 'drizzle':
      case 'light rain':
      case 'moderate rain':
      case 'heavy rain':
        return const Color(0xFF42A5F5); // Blue for rain
      case 'thunderstorm':
        return const Color(0xFF5C6BC0); // Indigo for storm
      case 'snow':
        return const Color(0xFF90CAF9); // Light blue for snow
      case 'mist':
      case 'fog':
      case 'haze':
      case 'foggy':
        return const Color(0xFFB0BEC5); // Light grey for fog
      default:
        return const Color(0xFF53AD64); // Green default
    }
  }

  /// Returns a formatted condition string.
  String get condition => weatherMain;
}
