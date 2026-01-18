class Alert {
  final String title;
  final String message;
  final String timeAgo;
  final String severity;

  Alert({
    required this.title,
    required this.message,
    required this.timeAgo,
    required this.severity,
  });

  factory Alert.fromJson(Map<String, dynamic> json) {
    return Alert(
      title: json['title'],
      message: json['message'],
      timeAgo: json['timeAgo'],
      severity: json['severity'],
    );
  }
}