/// Weather model
class Weather {
  final double temperature;
  final double humidity;
  final double windSpeed;
  final String description;
  final String icon;
  final DateTime timestamp;

  Weather({
    required this.temperature,
    required this.humidity,
    required this.windSpeed,
    required this.description,
    required this.icon,
    required this.timestamp,
  });

  /// Create Weather from JSON
  factory Weather.fromJson(Map<String, dynamic> json) {
    return Weather(
      temperature: json['temperature'].toDouble(),
      humidity: json['humidity'].toDouble(),
      windSpeed: json['wind_speed'].toDouble(),
      description: json['description'],
      icon: json['icon'],
      timestamp: DateTime.parse(json['timestamp']),
    );
  }

  /// Convert Weather to JSON
  Map<String, dynamic> toJson() {
    return {
      'temperature': temperature,
      'humidity': humidity,
      'wind_speed': windSpeed,
      'description': description,
      'icon': icon,
      'timestamp': timestamp.toIso8601String(),
    };
  }
}

/// Weather forecast model
class WeatherForecast {
  final DateTime date;
  final double tempMin;
  final double tempMax;
  final String description;
  final String icon;

  WeatherForecast({
    required this.date,
    required this.tempMin,
    required this.tempMax,
    required this.description,
    required this.icon,
  });

  /// Create WeatherForecast from JSON
  factory WeatherForecast.fromJson(Map<String, dynamic> json) {
    return WeatherForecast(
      date: DateTime.parse(json['date']),
      tempMin: json['temp_min'].toDouble(),
      tempMax: json['temp_max'].toDouble(),
      description: json['description'],
      icon: json['icon'],
    );
  }

  /// Convert WeatherForecast to JSON
  Map<String, dynamic> toJson() {
    return {
      'date': date.toIso8601String(),
      'temp_min': tempMin,
      'temp_max': tempMax,
      'description': description,
      'icon': icon,
    };
  }
}
