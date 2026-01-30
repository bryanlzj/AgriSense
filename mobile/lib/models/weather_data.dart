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

  /// Returns an icon emoji based on weather condition.
  String get icon {
    switch (weatherMain.toLowerCase()) {
      case 'clear':
        return '☀️';
      case 'clouds':
        return '☁️';
      case 'rain':
      case 'drizzle':
        return '🌧️';
      case 'thunderstorm':
        return '⛈️';
      case 'snow':
        return '❄️';
      case 'mist':
      case 'fog':
      case 'haze':
        return '🌫️';
      default:
        return '🌤️';
    }
  }

  /// Returns a formatted condition string.
  String get condition => weatherMain;
}
