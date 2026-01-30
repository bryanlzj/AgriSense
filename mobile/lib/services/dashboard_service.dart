import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:fyp_prototype/utils/api_constants.dart';

/// Service for fetching dashboard data from the API.
class DashboardService {
  /// Fetch full dashboard data.
  /// Returns a Map with user, weather, alerts, detections, and pest_risk.
  /// Throws an exception on failure.
  static Future<Map<String, dynamic>> getDashboard(String token) async {
    final url = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.dashboard}');

    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      return json.decode(response.body) as Map<String, dynamic>;
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else {
      final data = json.decode(response.body);
      final detail = data['detail'] ?? 'Failed to fetch dashboard data';
      throw Exception(detail);
    }
  }

  /// Fetch quick dashboard data (minimal, for fast loading).
  /// Returns basic counts and user info.
  /// Throws an exception on failure.
  static Future<Map<String, dynamic>> getQuickDashboard(String token) async {
    final url = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.dashboardQuick}');

    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      return json.decode(response.body) as Map<String, dynamic>;
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else {
      final data = json.decode(response.body);
      final detail = data['detail'] ?? 'Failed to fetch dashboard data';
      throw Exception(detail);
    }
  }
}
