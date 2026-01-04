/// Alert model
class Alert {
  final int id;
  final String type;
  final String severity;
  final String message;
  final bool isRead;
  final bool isAcknowledged;
  final DateTime createdAt;
  final int userId;

  Alert({
    required this.id,
    required this.type,
    required this.severity,
    required this.message,
    required this.isRead,
    required this.isAcknowledged,
    required this.createdAt,
    required this.userId,
  });

  /// Create Alert from JSON
  factory Alert.fromJson(Map<String, dynamic> json) {
    return Alert(
      id: json['id'],
      type: json['type'],
      severity: json['severity'],
      message: json['message'],
      isRead: json['is_read'],
      isAcknowledged: json['is_acknowledged'],
      createdAt: DateTime.parse(json['created_at']),
      userId: json['user_id'],
    );
  }

  /// Convert Alert to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'type': type,
      'severity': severity,
      'message': message,
      'is_read': isRead,
      'is_acknowledged': isAcknowledged,
      'created_at': createdAt.toIso8601String(),
      'user_id': userId,
    };
  }
}
