class WeatherData {
  final double temperature;
  final String condition;
  final String icon;
  final double windSpeed;
  final double humidity;

  WeatherData({
    required this.temperature,
    required this.condition,
    required this.icon,
    required this.windSpeed,
    required this.humidity,
  });

  factory WeatherData.fromJson(Map<String, dynamic> json) {
    return WeatherData(
      temperature: json['temperature'],
      condition: json['condition'],
      icon: json['icon'],
      windSpeed: json['windSpeed'],
      humidity: json['humidity'],
    );
  }
}
