/// Models for sensor-based weather data with ML classification.

class SensorCurrentWeather {
  final String source;
  final String? weatherCondition;
  final double? confidence;
  final Map<String, double>? probabilities;
  final double temperature;
  final double relativeHumidity;
  final double rain;
  final double windSpeed;
  final double? soilTemperature;
  final double soilMoisture;
  final double? solarRadiation;
  final int? weatherCode;
  final DateTime timestamp;
  final bool modelLoaded;

  SensorCurrentWeather({
    required this.source,
    this.weatherCondition,
    this.confidence,
    this.probabilities,
    required this.temperature,
    required this.relativeHumidity,
    required this.rain,
    required this.windSpeed,
    this.soilTemperature,
    required this.soilMoisture,
    this.solarRadiation,
    this.weatherCode,
    required this.timestamp,
    required this.modelLoaded,
  });

  factory SensorCurrentWeather.fromJson(Map<String, dynamic> json) {
    return SensorCurrentWeather(
      source: json['source'] ?? 'sensor',
      weatherCondition: json['weather_condition'],
      confidence: json['confidence']?.toDouble(),
      probabilities: json['probabilities'] != null
          ? Map<String, double>.from(json['probabilities']
              .map((k, v) => MapEntry(k, (v as num).toDouble())))
          : null,
      temperature: (json['temperature'] ?? 0).toDouble(),
      relativeHumidity: (json['relative_humidity'] ?? 0).toDouble(),
      rain: (json['rain'] ?? 0).toDouble(),
      windSpeed: (json['wind_speed'] ?? 0).toDouble(),
      soilTemperature: json['soil_temperature']?.toDouble(),
      soilMoisture: (json['soil_moisture'] ?? 0).toDouble(),
      solarRadiation: json['solar_radiation']?.toDouble(),
      weatherCode: json['weather_code'],
      timestamp: DateTime.parse(json['timestamp']),
      modelLoaded: json['model_loaded'] ?? false,
    );
  }
}

class SensorWeatherReading {
  final DateTime timestamp;
  final double temperature;
  final double relativeHumidity;
  final double rain;
  final double windSpeed;
  final double? soilTemperature;
  final double soilMoisture;
  final double? solarRadiation;
  final int? weatherCode;
  final String? weatherCondition;

  SensorWeatherReading({
    required this.timestamp,
    required this.temperature,
    required this.relativeHumidity,
    required this.rain,
    required this.windSpeed,
    this.soilTemperature,
    required this.soilMoisture,
    this.solarRadiation,
    this.weatherCode,
    this.weatherCondition,
  });

  factory SensorWeatherReading.fromJson(Map<String, dynamic> json) {
    return SensorWeatherReading(
      timestamp: DateTime.parse(json['timestamp']),
      temperature: (json['temperature'] ?? 0).toDouble(),
      relativeHumidity: (json['relative_humidity'] ?? 0).toDouble(),
      rain: (json['rain'] ?? 0).toDouble(),
      windSpeed: (json['wind_speed'] ?? 0).toDouble(),
      soilTemperature: json['soil_temperature']?.toDouble(),
      soilMoisture: (json['soil_moisture'] ?? 0).toDouble(),
      solarRadiation: json['solar_radiation']?.toDouble(),
      weatherCode: json['weather_code'],
      weatherCondition: json['weather_condition'],
    );
  }
}

class HistoricalSummary {
  final double avgTemperature;
  final double maxTemperature;
  final double minTemperature;
  final double avgHumidity;
  final double totalRain;
  final String? dominantCondition;
  final Map<String, int> conditionBreakdown;

  HistoricalSummary({
    required this.avgTemperature,
    required this.maxTemperature,
    required this.minTemperature,
    required this.avgHumidity,
    required this.totalRain,
    this.dominantCondition,
    required this.conditionBreakdown,
  });

  factory HistoricalSummary.fromJson(Map<String, dynamic> json) {
    return HistoricalSummary(
      avgTemperature: (json['avg_temperature'] ?? 0).toDouble(),
      maxTemperature: (json['max_temperature'] ?? 0).toDouble(),
      minTemperature: (json['min_temperature'] ?? 0).toDouble(),
      avgHumidity: (json['avg_humidity'] ?? 0).toDouble(),
      totalRain: (json['total_rain'] ?? 0).toDouble(),
      dominantCondition: json['dominant_condition'],
      conditionBreakdown: json['condition_breakdown'] != null
          ? Map<String, int>.from(json['condition_breakdown']
              .map((k, v) => MapEntry(k, v as int)))
          : {},
    );
  }
}

class HistoricalWeatherData {
  final String period;
  final DateTime start;
  final DateTime end;
  final int readingsCount;
  final List<SensorWeatherReading> readings;
  final HistoricalSummary summary;

  HistoricalWeatherData({
    required this.period,
    required this.start,
    required this.end,
    required this.readingsCount,
    required this.readings,
    required this.summary,
  });

  factory HistoricalWeatherData.fromJson(Map<String, dynamic> json) {
    return HistoricalWeatherData(
      period: json['period'],
      start: DateTime.parse(json['start']),
      end: DateTime.parse(json['end']),
      readingsCount: json['readings_count'],
      readings: (json['readings'] as List)
          .map((r) => SensorWeatherReading.fromJson(r))
          .toList(),
      summary: HistoricalSummary.fromJson(json['summary']),
    );
  }
}
