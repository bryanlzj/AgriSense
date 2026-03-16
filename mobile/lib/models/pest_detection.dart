/// Model for pest detection results from the API.

class PestDetectionResult {
  final String pestType;
  final double confidence;
  final String description;

  PestDetectionResult({
    required this.pestType,
    required this.confidence,
    required this.description,
  });

  factory PestDetectionResult.fromJson(Map<String, dynamic> json) {
    return PestDetectionResult(
      pestType: json['pest_type'] ?? '',
      confidence: (json['confidence'] ?? 0).toDouble(),
      description: json['description'] ?? '',
    );
  }
}

class PestDetection {
  final int id;
  final int userId;
  final String pestType;
  final double confidenceScore;
  final String imageUrl;
  final String? recommendations;
  final DateTime detectedAt;
  final String? scientificName;
  final String? description;
  final String? dangerLevel;
  final List<String>? pestRecommendations;

  PestDetection({
    required this.id,
    required this.userId,
    required this.pestType,
    required this.confidenceScore,
    required this.imageUrl,
    this.recommendations,
    required this.detectedAt,
    this.scientificName,
    this.description,
    this.dangerLevel,
    this.pestRecommendations,
  });

  factory PestDetection.fromJson(Map<String, dynamic> json) {
    return PestDetection(
      id: json['id'],
      userId: json['user_id'],
      pestType: json['pest_type'] ?? '',
      confidenceScore: (json['confidence_score'] ?? 0).toDouble(),
      imageUrl: json['image_url'] ?? '',
      recommendations: json['recommendations'],
      detectedAt: DateTime.parse(json['detected_at']),
      scientificName: json['scientific_name'],
      description: json['description'],
      dangerLevel: json['danger_level'],
      pestRecommendations: json['pest_recommendations'] != null
          ? List<String>.from(json['pest_recommendations'])
          : null,
    );
  }
}

/// Enhanced pest detection response with confidence tiering.
class EnhancedPestDetection {
  final int? detectionId;
  final String imageUrl;
  final String status; // 'detected', 'partial', 'unknown'
  final double confidence;
  final int confidencePercent;
  final String? pestName;
  final String? scientificName;
  final String? description;
  final String? dangerLevel; // 'low', 'medium', 'high'
  final List<String>? recommendations;
  final bool canRetry;
  final String? retryTip;
  final bool offerReport;
  final DateTime analysisTimestamp;

  EnhancedPestDetection({
    this.detectionId,
    required this.imageUrl,
    required this.status,
    required this.confidence,
    required this.confidencePercent,
    this.pestName,
    this.scientificName,
    this.description,
    this.dangerLevel,
    this.recommendations,
    required this.canRetry,
    this.retryTip,
    required this.offerReport,
    required this.analysisTimestamp,
  });

  factory EnhancedPestDetection.fromJson(Map<String, dynamic> json) {
    return EnhancedPestDetection(
      detectionId: json['detection_id'],
      imageUrl: json['image_url'] ?? '',
      status: json['status'] ?? 'unknown',
      confidence: (json['confidence'] ?? 0).toDouble(),
      confidencePercent: json['confidence_percent'] ?? 0,
      pestName: json['pest_name'],
      scientificName: json['scientific_name'],
      description: json['description'],
      dangerLevel: json['danger_level'],
      recommendations: json['recommendations'] != null
          ? List<String>.from(json['recommendations'])
          : null,
      canRetry: json['can_retry'] ?? false,
      retryTip: json['retry_tip'],
      offerReport: json['offer_report'] ?? false,
      analysisTimestamp: DateTime.parse(
          json['analysis_timestamp'] ?? DateTime.now().toIso8601String()),
    );
  }

  bool get isDetected => status == 'detected';
  bool get isPartial => status == 'partial';
  bool get isUnknown => status == 'unknown';
}

/// Pest statistics summary.
class PestStatistics {
  final int totalDetections;
  final int uniquePests;
  final String? mostCommonPest;
  final double averageConfidence;
  final Map<String, int> detectionsByPest;

  PestStatistics({
    required this.totalDetections,
    required this.uniquePests,
    this.mostCommonPest,
    required this.averageConfidence,
    required this.detectionsByPest,
  });

  factory PestStatistics.fromJson(Map<String, dynamic> json) {
    return PestStatistics(
      totalDetections: json['total_detections'] ?? 0,
      uniquePests: json['unique_pests'] ?? 0,
      mostCommonPest: json['most_common_pest'],
      averageConfidence: (json['average_confidence'] ?? 0).toDouble(),
      detectionsByPest: Map<String, int>.from(json['detections_by_pest'] ?? {}),
    );
  }
}
