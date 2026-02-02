import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:fyp_prototype/utils/api_constants.dart';
import 'package:fyp_prototype/utils/token_storage.dart';
import 'package:fyp_prototype/models/pest_detection.dart';

/// Service for pest detection API calls.
class PestService {
  /// Upload an image and detect pests using enhanced detection.
  /// Returns EnhancedPestDetection with confidence tiering.
  static Future<EnhancedPestDetection> detectPest({
    required File imageFile,
    String? notes,
    int retryCount = 0,
  }) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final uri = Uri.parse(
      '${ApiConstants.baseUrl}${ApiConstants.pestDetectEnhanced}'
      '?retry_count=$retryCount${notes != null ? '&notes=${Uri.encodeComponent(notes)}' : ''}',
    );

    final request = http.MultipartRequest('POST', uri);
    request.headers['Authorization'] = 'Bearer $token';
    request.files.add(
      await http.MultipartFile.fromPath('file', imageFile.path),
    );

    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode == 201) {
      final data = json.decode(response.body);
      return EnhancedPestDetection.fromJson(data);
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else if (response.statusCode == 400) {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Invalid image file');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to detect pest');
    }
  }

  /// Get list of past pest detections.
  static Future<List<PestDetection>> getDetections({
    int skip = 0,
    int limit = 100,
    String? pestType,
    double? minConfidence,
  }) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final queryParams = <String, String>{
      'skip': skip.toString(),
      'limit': limit.toString(),
    };
    if (pestType != null) queryParams['pest_type'] = pestType;
    if (minConfidence != null) {
      queryParams['min_confidence'] = minConfidence.toString();
    }

    final uri = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.pestList}')
        .replace(queryParameters: queryParams);

    final response = await http.get(
      uri,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body) as List;
      return data.map((d) => PestDetection.fromJson(d)).toList();
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to fetch detections');
    }
  }

  /// Get a single pest detection by ID.
  static Future<PestDetection> getDetection(int detectionId) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final uri = Uri.parse(
      '${ApiConstants.baseUrl}${ApiConstants.pestList}$detectionId',
    );

    final response = await http.get(
      uri,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return PestDetection.fromJson(data);
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else if (response.statusCode == 404) {
      throw Exception('Detection not found');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to fetch detection');
    }
  }

  /// Delete a pest detection.
  static Future<void> deleteDetection(int detectionId) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final uri = Uri.parse(
      '${ApiConstants.baseUrl}${ApiConstants.pestList}$detectionId',
    );

    final response = await http.delete(
      uri,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 204) {
      return;
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else if (response.statusCode == 404) {
      throw Exception('Detection not found');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to delete detection');
    }
  }

  /// Get pest detection statistics.
  static Future<PestStatistics> getStatistics({int days = 30}) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final uri = Uri.parse(
      '${ApiConstants.baseUrl}${ApiConstants.pestStats}?days=$days',
    );

    final response = await http.get(
      uri,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return PestStatistics.fromJson(data);
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to fetch statistics');
    }
  }
}
