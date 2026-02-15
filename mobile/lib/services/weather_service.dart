import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:fyp_prototype/utils/api_constants.dart';
import 'package:fyp_prototype/utils/token_storage.dart';

/// Service for fetching weather data from the API.
class WeatherService {
  /// Fetch current weather conditions.
  /// Returns weather data with alerts and recommendations.
  static Future<Map<String, dynamic>> getCurrentWeather({
    required double latitude,
    required double longitude,
    String? locationName,
  }) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final queryParams = {
      'latitude': latitude.toString(),
      'longitude': longitude.toString(),
      if (locationName != null) 'location_name': locationName,
    };

    final uri = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.weatherCurrent}')
        .replace(queryParameters: queryParams);

    final response = await http.get(
      uri,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      return json.decode(response.body) as Map<String, dynamic>;
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to fetch weather data');
    }
  }

  /// Fetch weather forecast (5 days).
  /// Returns forecast data with alerts and recommendations.
  static Future<Map<String, dynamic>> getForecast({
    required double latitude,
    required double longitude,
    String? locationName,
  }) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final queryParams = {
      'latitude': latitude.toString(),
      'longitude': longitude.toString(),
      if (locationName != null) 'location_name': locationName,
    };

    final uri = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.weatherForecast}')
        .replace(queryParameters: queryParams);

    final response = await http.get(
      uri,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      return json.decode(response.body) as Map<String, dynamic>;
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to fetch forecast data');
    }
  }

  /// Fetch weather summary (current + forecast + alerts + recommendations).
  /// This is the most comprehensive endpoint.
  static Future<WeatherSummaryData> getSummary({
    required double latitude,
    required double longitude,
    String? locationName,
  }) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final queryParams = {
      'latitude': latitude.toString(),
      'longitude': longitude.toString(),
      if (locationName != null) 'location_name': locationName,
    };

    final uri = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.weatherSummary}')
        .replace(queryParameters: queryParams);

    final response = await http.get(
      uri,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body) as Map<String, dynamic>;
      return WeatherSummaryData.fromJson(data);
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to fetch weather summary');
    }
  }
}

/// Model for weather summary response.
class WeatherSummaryData {
  final WeatherLocation location;
  final CurrentWeather current;
  final List<ForecastItem> forecast;
  final List<WeatherAlert> alerts;
  final List<WeatherRecommendation> recommendations;
  final DateTime updatedAt;

  WeatherSummaryData({
    required this.location,
    required this.current,
    required this.forecast,
    required this.alerts,
    required this.recommendations,
    required this.updatedAt,
  });

  factory WeatherSummaryData.fromJson(Map<String, dynamic> json) {
    return WeatherSummaryData(
      location: WeatherLocation.fromJson(json['location'] ?? {}),
      current: CurrentWeather.fromJson(json['current'] ?? {}),
      forecast: (json['forecast'] as List<dynamic>? ?? [])
          .map((f) => ForecastItem.fromJson(f))
          .toList(),
      alerts: (json['alerts'] as List<dynamic>? ?? [])
          .map((a) => WeatherAlert.fromJson(a))
          .toList(),
      recommendations: (json['recommendations'] as List<dynamic>? ?? [])
          .map((r) => WeatherRecommendation.fromJson(r))
          .toList(),
      updatedAt: DateTime.tryParse(json['updated_at'] ?? '') ?? DateTime.now(),
    );
  }
}

class WeatherLocation {
  final double latitude;
  final double longitude;
  final String? locationName;

  WeatherLocation({
    required this.latitude,
    required this.longitude,
    this.locationName,
  });

  factory WeatherLocation.fromJson(Map<String, dynamic> json) {
    return WeatherLocation(
      latitude: (json['latitude'] as num?)?.toDouble() ?? 0.0,
      longitude: (json['longitude'] as num?)?.toDouble() ?? 0.0,
      locationName: json['location_name'] as String?,
    );
  }
}

class CurrentWeather {
  final double temperature;
  final double feelsLike;
  final int humidity;
  final double pressure;
  final double windSpeed;
  final int windDirection;
  final int clouds;
  final int visibility;
  final String weatherMain;
  final String weatherDescription;
  final double? rain;

  CurrentWeather({
    required this.temperature,
    required this.feelsLike,
    required this.humidity,
    required this.pressure,
    required this.windSpeed,
    required this.windDirection,
    required this.clouds,
    required this.visibility,
    required this.weatherMain,
    required this.weatherDescription,
    this.rain,
  });

  factory CurrentWeather.fromJson(Map<String, dynamic> json) {
    return CurrentWeather(
      temperature: (json['temperature'] as num?)?.toDouble() ?? 0.0,
      feelsLike: (json['feels_like'] as num?)?.toDouble() ?? 0.0,
      humidity: (json['relative_humidity'] as num?)?.toInt() ?? 0,
      pressure: (json['pressure'] as num?)?.toDouble() ?? 0.0,
      windSpeed: (json['wind_speed'] as num?)?.toDouble() ?? 0.0,
      windDirection: (json['wind_direction'] as num?)?.toInt() ?? 0,
      clouds: (json['clouds'] as num?)?.toInt() ?? 0,
      visibility: (json['visibility'] as num?)?.toInt() ?? 10000,
      weatherMain: json['weather_main'] as String? ?? 'Unknown',
      weatherDescription: json['weather_description'] as String? ?? '',
      rain: (json['rain'] as num?)?.toDouble(),
    );
  }

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

  Color get iconColor {
    switch (weatherMain.toLowerCase()) {
      case 'clear':
      case 'sunny':
        return const Color(0xFFFFB300);
      case 'clouds':
      case 'cloudy':
      case 'partly cloudy':
      case 'overcast':
        return const Color(0xFF78909C);
      case 'rain':
      case 'drizzle':
      case 'light rain':
      case 'moderate rain':
      case 'heavy rain':
        return const Color(0xFF42A5F5);
      case 'thunderstorm':
        return const Color(0xFF5C6BC0);
      case 'snow':
        return const Color(0xFF90CAF9);
      case 'mist':
      case 'fog':
      case 'haze':
      case 'foggy':
        return const Color(0xFFB0BEC5);
      default:
        return const Color(0xFF53AD64);
    }
  }
}

class ForecastItem {
  final DateTime forecastTime;
  final double temperature;
  final double feelsLike;
  final int humidity;
  final double pressure;
  final double windSpeed;
  final int clouds;
  final String weatherMain;
  final String weatherDescription;
  final double rainProbability;
  final double? rainVolume;

  ForecastItem({
    required this.forecastTime,
    required this.temperature,
    required this.feelsLike,
    required this.humidity,
    required this.pressure,
    required this.windSpeed,
    required this.clouds,
    required this.weatherMain,
    required this.weatherDescription,
    required this.rainProbability,
    this.rainVolume,
  });

  factory ForecastItem.fromJson(Map<String, dynamic> json) {
    return ForecastItem(
      forecastTime: DateTime.tryParse(json['forecast_time'] ?? '') ?? DateTime.now(),
      temperature: (json['temperature'] as num?)?.toDouble() ?? 0.0,
      feelsLike: (json['feels_like'] as num?)?.toDouble() ?? 0.0,
      humidity: (json['humidity'] as num?)?.toInt() ?? 0,
      pressure: (json['pressure'] as num?)?.toDouble() ?? 0.0,
      windSpeed: (json['wind_speed'] as num?)?.toDouble() ?? 0.0,
      clouds: (json['clouds'] as num?)?.toInt() ?? 0,
      weatherMain: json['weather_main'] as String? ?? 'Unknown',
      weatherDescription: json['weather_description'] as String? ?? '',
      rainProbability: (json['rain_probability'] as num?)?.toDouble() ?? 0.0,
      rainVolume: (json['rain_volume'] as num?)?.toDouble(),
    );
  }

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

  Color get iconColor {
    switch (weatherMain.toLowerCase()) {
      case 'clear':
      case 'sunny':
        return const Color(0xFFFFB300);
      case 'clouds':
      case 'cloudy':
      case 'partly cloudy':
      case 'overcast':
        return const Color(0xFF78909C);
      case 'rain':
      case 'drizzle':
      case 'light rain':
      case 'moderate rain':
      case 'heavy rain':
        return const Color(0xFF42A5F5);
      case 'thunderstorm':
        return const Color(0xFF5C6BC0);
      case 'snow':
        return const Color(0xFF90CAF9);
      case 'mist':
      case 'fog':
      case 'haze':
      case 'foggy':
        return const Color(0xFFB0BEC5);
      default:
        return const Color(0xFF53AD64);
    }
  }
}

class WeatherAlert {
  final String alertType;
  final String severity;
  final String title;
  final String description;
  final DateTime? startTime;
  final DateTime? endTime;
  final List<String> recommendations;

  WeatherAlert({
    required this.alertType,
    required this.severity,
    required this.title,
    required this.description,
    this.startTime,
    this.endTime,
    required this.recommendations,
  });

  factory WeatherAlert.fromJson(Map<String, dynamic> json) {
    return WeatherAlert(
      alertType: json['alert_type'] as String? ?? '',
      severity: json['severity'] as String? ?? 'medium',
      title: json['title'] as String? ?? '',
      description: json['description'] as String? ?? '',
      startTime: json['start_time'] != null
          ? DateTime.tryParse(json['start_time'])
          : null,
      endTime: json['end_time'] != null
          ? DateTime.tryParse(json['end_time'])
          : null,
      recommendations: (json['recommendations'] as List<dynamic>? ?? [])
          .map((r) => r.toString())
          .toList(),
    );
  }

  String get icon {
    switch (alertType.toLowerCase()) {
      case 'heavy rain':
      case 'heavy rain forecast':
        return '🌧️';
      case 'strong wind':
        return '💨';
      case 'high temperature':
        return '🌡️';
      default:
        return '⚠️';
    }
  }
}

class WeatherRecommendation {
  final String category;
  final String priority;
  final String title;
  final String description;
  final String reason;
  final List<String> actions;

  WeatherRecommendation({
    required this.category,
    required this.priority,
    required this.title,
    required this.description,
    required this.reason,
    required this.actions,
  });

  factory WeatherRecommendation.fromJson(Map<String, dynamic> json) {
    return WeatherRecommendation(
      category: json['category'] as String? ?? '',
      priority: json['priority'] as String? ?? 'medium',
      title: json['title'] as String? ?? '',
      description: json['description'] as String? ?? '',
      reason: json['reason'] as String? ?? '',
      actions: (json['actions'] as List<dynamic>? ?? [])
          .map((a) => a.toString())
          .toList(),
    );
  }

  String get icon {
    switch (category.toLowerCase()) {
      case 'irrigation':
        return '💧';
      case 'pest_control':
        return '🐛';
      case 'spraying':
        return '🧴';
      case 'harvesting':
        return '🌾';
      default:
        return '📋';
    }
  }
}
