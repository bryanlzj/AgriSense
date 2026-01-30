import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:fyp_prototype/models/user.dart';
import 'package:fyp_prototype/utils/api_constants.dart';

/// Service for handling authentication API calls.
class AuthService {
  /// Login with username and password.
  /// Returns the access token on success.
  /// Throws an exception with error message on failure.
  static Future<String> login(String username, String password) async {
    final url = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.login}');

    // OAuth2 password flow uses form-urlencoded format
    final response = await http.post(
      url,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: {
        'username': username,
        'password': password,
      },
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['access_token'] as String;
    } else if (response.statusCode == 401) {
      throw Exception('Invalid username or password');
    } else {
      final data = json.decode(response.body);
      final detail = data['detail'] ?? 'Login failed';
      throw Exception(detail);
    }
  }

  /// Register a new user.
  /// Returns the created User on success.
  /// Throws an exception with error message on failure.
  static Future<User> register({
    required String username,
    required String password,
    String? fullName,
    String farmLocationName = 'Kuala Lumpur',
    double farmLocationLat = 3.1390,
    double farmLocationLng = 101.6869,
    String cropType = 'rice',
  }) async {
    final url = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.register}');

    final body = {
      'username': username,
      'password': password,
      'farm_location_name': farmLocationName,
      'farm_location_lat': farmLocationLat,
      'farm_location_lng': farmLocationLng,
      'crop_type': cropType,
    };

    if (fullName != null) {
      body['full_name'] = fullName;
    }

    final response = await http.post(
      url,
      headers: {
        'Content-Type': 'application/json',
      },
      body: json.encode(body),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      final data = json.decode(response.body);
      return User.fromJson(data);
    } else if (response.statusCode == 400) {
      final data = json.decode(response.body);
      final detail = data['detail'] ?? 'Registration failed';
      throw Exception(detail);
    } else {
      final data = json.decode(response.body);
      final detail = data['detail'] ?? 'Registration failed';
      throw Exception(detail);
    }
  }

  /// Get the current authenticated user's profile.
  /// Requires a valid JWT token.
  /// Returns the User on success.
  /// Throws an exception on failure.
  static Future<User> getCurrentUser(String token) async {
    final url = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.me}');

    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return User.fromJson(data);
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else {
      throw Exception('Failed to get user profile');
    }
  }
}
