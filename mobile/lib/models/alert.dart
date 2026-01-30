class Alert {
  final int id;
  final String type;
  final String severity;
  final String title;
  final String message;
  final bool isRead;
  final DateTime? createdAt;

  Alert({
    required this.id,
    required this.type,
    required this.severity,
    required this.title,
    required this.message,
    required this.isRead,
    this.createdAt,
  });

  /// Creates Alert from backend API response.
  factory Alert.fromJson(Map<String, dynamic> json) {
    return Alert(
      id: json['id'] as int? ?? 0,
      type: json['type'] as String? ?? 'system',
      severity: json['severity'] as String? ?? 'low',
      title: json['title'] as String? ?? '',
      message: json['message'] as String? ?? '',
      isRead: json['is_read'] as bool? ?? false,
      createdAt: json['created_at'] != null
          ? DateTime.tryParse(json['created_at'] as String)
          : null,
    );
  }

  /// Returns a human-readable time ago string.
  String get timeAgo {
    if (createdAt == null) return '';

    final now = DateTime.now();
    final difference = now.difference(createdAt!);

    if (difference.inDays > 7) {
      return '${(difference.inDays / 7).floor()}w ago';
    } else if (difference.inDays > 0) {
      return '${difference.inDays}d ago';
    } else if (difference.inHours > 0) {
      return '${difference.inHours}h ago';
    } else if (difference.inMinutes > 0) {
      return '${difference.inMinutes}m ago';
    } else {
      return 'Just now';
    }
  }

  /// Returns capitalized severity for display.
  String get severityDisplay {
    if (severity.isEmpty) return 'Low';
    return severity[0].toUpperCase() + severity.substring(1);
  }

  /// Returns an icon based on alert type.
  String get icon {
    switch (type.toLowerCase()) {
      case 'weather':
        return '🌤️';
      case 'pest':
        return '🐛';
      case 'environmental':
        return '🌱';
      case 'system':
      default:
        return '⚠️';
    }
  }
}
