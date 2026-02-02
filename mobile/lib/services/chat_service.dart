import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:fyp_prototype/utils/api_constants.dart';
import 'package:fyp_prototype/utils/token_storage.dart';
import 'package:fyp_prototype/models/chat_message.dart';

/// Service for chatbot API calls.
class ChatService {
  /// Send a message to the chatbot.
  static Future<ChatResponse> sendMessage({
    required String message,
    String? sessionId,
    bool includeWeather = true,
  }) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final uri = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.chatMessage}');

    final body = <String, dynamic>{
      'message': message,
      'include_weather': includeWeather,
    };
    if (sessionId != null) body['session_id'] = sessionId;

    final response = await http.post(
      uri,
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: json.encode(body),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return ChatResponse.fromJson(data);
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to send message');
    }
  }

  /// Send an image to the chatbot for guidance.
  static Future<Map<String, dynamic>> sendImage({
    required String imageUrl,
    String? message,
  }) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final uri = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.chatImage}');

    final body = <String, dynamic>{
      'image_url': imageUrl,
    };
    if (message != null) body['message'] = message;

    final response = await http.post(
      uri,
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: json.encode(body),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to send image');
    }
  }

  /// Get chatbot status.
  static Future<ChatStatus> getStatus() async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final uri = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.chatStatus}');

    final response = await http.get(
      uri,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return ChatStatus.fromJson(data);
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to get status');
    }
  }
}
