/// Models for chatbot messages and responses.

class ChatMessage {
  final String content;
  final bool isUser;
  final DateTime timestamp;
  final ChatContextUsed? contextUsed;

  ChatMessage({
    required this.content,
    required this.isUser,
    required this.timestamp,
    this.contextUsed,
  });
}

class ChatContextUsed {
  final String? cropType;
  final String? location;
  final bool weatherAvailable;
  final String? weatherSummary;

  ChatContextUsed({
    this.cropType,
    this.location,
    required this.weatherAvailable,
    this.weatherSummary,
  });

  factory ChatContextUsed.fromJson(Map<String, dynamic> json) {
    return ChatContextUsed(
      cropType: json['crop_type'],
      location: json['location'],
      weatherAvailable: json['weather_available'] ?? false,
      weatherSummary: json['weather_summary'],
    );
  }
}

class ChatResponse {
  final String message;
  final String? sessionId;
  final ChatContextUsed contextUsed;
  final bool aiAvailable;
  final String timestamp;

  ChatResponse({
    required this.message,
    this.sessionId,
    required this.contextUsed,
    required this.aiAvailable,
    required this.timestamp,
  });

  factory ChatResponse.fromJson(Map<String, dynamic> json) {
    return ChatResponse(
      message: json['message'] ?? '',
      sessionId: json['session_id'],
      contextUsed: ChatContextUsed.fromJson(json['context_used'] ?? {}),
      aiAvailable: json['ai_available'] ?? false,
      timestamp: json['timestamp'] ?? DateTime.now().toIso8601String(),
    );
  }
}

class ChatStatus {
  final String status;
  final bool aiServiceAvailable;
  final Map<String, String?> userContext;
  final List<String> capabilities;

  ChatStatus({
    required this.status,
    required this.aiServiceAvailable,
    required this.userContext,
    required this.capabilities,
  });

  factory ChatStatus.fromJson(Map<String, dynamic> json) {
    return ChatStatus(
      status: json['status'] ?? 'unknown',
      aiServiceAvailable: json['ai_service_available'] ?? false,
      userContext: Map<String, String?>.from(json['user_context'] ?? {}),
      capabilities: List<String>.from(json['capabilities'] ?? []),
    );
  }
}
