/// Pest detection model
class PestDetection {
  final int id;
  final String imageUrl;
  final String pestType;
  final double confidence;
  final String recommendations;
  final DateTime detectedAt;
  final int userId;

  PestDetection({
    required this.id,
    required this.imageUrl,
    required this.pestType,
    required this.confidence,
    required this.recommendations,
    required this.detectedAt,
    required this.userId,
  });

  /// Create PestDetection from JSON
  factory PestDetection.fromJson(Map<String, dynamic> json) {
    return PestDetection(
      id: json['id'],
      imageUrl: json['image_url'],
      pestType: json['pest_type'],
      confidence: json['confidence'].toDouble(),
      recommendations: json['recommendations'],
      detectedAt: DateTime.parse(json['detected_at']),
      userId: json['user_id'],
    );
  }

  /// Convert PestDetection to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'image_url': imageUrl,
      'pest_type': pestType,
      'confidence': confidence,
      'recommendations': recommendations,
      'detected_at': detectedAt.toIso8601String(),
      'user_id': userId,
    };
  }
}
