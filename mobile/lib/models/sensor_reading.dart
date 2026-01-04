/// Sensor reading model
class SensorReading {
  final int id;
  final double temperature;
  final double humidity;
  final double soilMoisture;
  final double rainfall;
  final String? location;
  final DateTime timestamp;
  final int userId;

  SensorReading({
    required this.id,
    required this.temperature,
    required this.humidity,
    required this.soilMoisture,
    required this.rainfall,
    this.location,
    required this.timestamp,
    required this.userId,
  });

  /// Create SensorReading from JSON
  factory SensorReading.fromJson(Map<String, dynamic> json) {
    return SensorReading(
      id: json['id'],
      temperature: json['temperature'].toDouble(),
      humidity: json['humidity'].toDouble(),
      soilMoisture: json['soil_moisture'].toDouble(),
      rainfall: json['rainfall'].toDouble(),
      location: json['location'],
      timestamp: DateTime.parse(json['timestamp']),
      userId: json['user_id'],
    );
  }

  /// Convert SensorReading to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'temperature': temperature,
      'humidity': humidity,
      'soil_moisture': soilMoisture,
      'rainfall': rainfall,
      'location': location,
      'timestamp': timestamp.toIso8601String(),
      'user_id': userId,
    };
  }
}
