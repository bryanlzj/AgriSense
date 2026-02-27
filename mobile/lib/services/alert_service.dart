import 'dart:convert';
import 'package:fyp_prototype/utils/api_constants.dart';
import 'package:fyp_prototype/utils/token_storage.dart';
import 'package:fyp_prototype/utils/http_client.dart';
import 'package:fyp_prototype/models/alert.dart';

/// Service for managing alerts from the API.
class AlertService {
  /// Fetch all alerts with optional filters.
  static Future<AlertListResponse> getAlerts({
    String? type,
    String? severity,
    bool? isRead,
    int skip = 0,
    int limit = 50,
  }) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final queryParams = <String, String>{
      'skip': skip.toString(),
      'limit': limit.toString(),
    };
    if (type != null) queryParams['type'] = type;
    if (severity != null) queryParams['severity'] = severity;
    if (isRead != null) queryParams['is_read'] = isRead.toString();

    final uri = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.alerts}')
        .replace(queryParameters: queryParams);

    final response = await appHttpClient.get(
      uri,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      // Backend returns a direct array, not paginated object
      if (data is List) {
        return AlertListResponse(
          alerts: data.map((a) => Alert.fromJson(a as Map<String, dynamic>)).toList(),
          total: data.length,
          skip: skip,
          limit: limit,
        );
      }
      return AlertListResponse.fromJson(data as Map<String, dynamic>);
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to fetch alerts');
    }
  }

  /// Get a single alert by ID.
  static Future<Alert> getAlert(int alertId) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final uri = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.alerts}/$alertId');

    final response = await appHttpClient.get(
      uri,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return Alert.fromJson(data);
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else if (response.statusCode == 404) {
      throw Exception('Alert not found');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to fetch alert');
    }
  }

  /// Mark an alert as read.
  static Future<Alert> markAsRead(int alertId) async {
    return updateAlert(alertId, isRead: true);
  }

  /// Mark an alert as acknowledged.
  static Future<Alert> acknowledge(int alertId) async {
    return updateAlert(alertId, isAcknowledged: true);
  }

  /// Update an alert (mark read, acknowledge, etc.).
  static Future<Alert> updateAlert(
    int alertId, {
    bool? isRead,
    bool? isAcknowledged,
  }) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final uri = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.alerts}/$alertId');

    final body = <String, dynamic>{};
    if (isRead != null) body['is_read'] = isRead;
    if (isAcknowledged != null) body['is_acknowledged'] = isAcknowledged;

    final response = await appHttpClient.put(
      uri,
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: json.encode(body),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return Alert.fromJson(data);
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else if (response.statusCode == 404) {
      throw Exception('Alert not found');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to update alert');
    }
  }

  /// Delete an alert.
  static Future<void> deleteAlert(int alertId) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final uri = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.alerts}/$alertId');

    final response = await appHttpClient.delete(
      uri,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200 || response.statusCode == 204) {
      return;
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else if (response.statusCode == 404) {
      throw Exception('Alert not found');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to delete alert');
    }
  }

  /// Bulk mark alerts as read.
  static Future<void> bulkMarkAsRead(List<int> alertIds) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final uri = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.alertsBulk}');

    final response = await appHttpClient.put(
      uri,
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: json.encode({
        'alert_ids': alertIds,
        'is_read': true,
      }),
    );

    if (response.statusCode == 200) {
      return;
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to update alerts');
    }
  }

  /// Get alert statistics.
  static Future<AlertStats> getStats() async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final uri = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.alertsStats}');

    final response = await appHttpClient.get(
      uri,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return AlertStats.fromJson(data);
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to fetch alert stats');
    }
  }
}

/// Response wrapper for alert list.
class AlertListResponse {
  final List<Alert> alerts;
  final int total;
  final int skip;
  final int limit;

  AlertListResponse({
    required this.alerts,
    required this.total,
    required this.skip,
    required this.limit,
  });

  factory AlertListResponse.fromJson(Map<String, dynamic> json) {
    // Handle both array response and paginated response
    if (json.containsKey('alerts')) {
      return AlertListResponse(
        alerts: (json['alerts'] as List<dynamic>)
            .map((a) => Alert.fromJson(a))
            .toList(),
        total: json['total'] as int? ?? 0,
        skip: json['skip'] as int? ?? 0,
        limit: json['limit'] as int? ?? 50,
      );
    } else if (json is List) {
      // Direct array response
      return AlertListResponse(
        alerts: (json as List<dynamic>)
            .map((a) => Alert.fromJson(a))
            .toList(),
        total: json.length,
        skip: 0,
        limit: json.length,
      );
    } else {
      return AlertListResponse(
        alerts: [],
        total: 0,
        skip: 0,
        limit: 50,
      );
    }
  }
}

/// Alert statistics.
class AlertStats {
  final int totalAlerts;
  final int unreadCount;
  final int weatherAlerts;
  final int pestAlerts;
  final int systemAlerts;
  final int environmentalAlerts;

  AlertStats({
    required this.totalAlerts,
    required this.unreadCount,
    required this.weatherAlerts,
    required this.pestAlerts,
    required this.systemAlerts,
    required this.environmentalAlerts,
  });

  factory AlertStats.fromJson(Map<String, dynamic> json) {
    return AlertStats(
      totalAlerts: json['total_alerts'] as int? ?? 0,
      unreadCount: json['unread_count'] as int? ?? 0,
      weatherAlerts: json['weather_alerts'] as int? ?? 0,
      pestAlerts: json['pest_alerts'] as int? ?? 0,
      systemAlerts: json['system_alerts'] as int? ?? 0,
      environmentalAlerts: json['environmental_alerts'] as int? ?? 0,
    );
  }
}
