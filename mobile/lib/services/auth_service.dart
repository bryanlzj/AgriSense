import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:fyp_prototype/models/user.dart';
import 'package:fyp_prototype/utils/api_constants.dart';
import 'package:fyp_prototype/utils/http_client.dart';

/// Service for handling authentication API calls.
class AuthService {
  /// Login with username and password.
  /// Returns the access token on success.
  /// Throws an exception with error message on failure.
  static Future<String> login(String username, String password) async {
    final url = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.login}');
    debugPrint('[AUTH] Login attempt: url=$url, username=$username');

    try {
      // OAuth2 password flow uses form-urlencoded format
      final response = await appHttpClient.post(
        url,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: {
          'username': username,
          'password': password,
        },
      ).timeout(const Duration(seconds: 10));

      debugPrint('[AUTH] Login response: status=${response.statusCode}, body=${response.body}');

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
    } catch (e) {
      debugPrint('[AUTH] Login error: $e');
      rethrow;
    }
  }

  /// Register a new user.
  /// Returns the created User on success.
  /// Throws an exception with error message on failure.
  static Future<User> register({
    required String username,
    required String password,
    String? fullName,
    String? email,
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
    if (email != null) {
      body['email'] = email;
    }

    final response = await appHttpClient.post(
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

  /// Update the current user's profile.
  static Future<User> updateProfile({
    required String token,
    String? fullName,
    String? email,
    String? farmLocationName,
    double? farmLocationLat,
    double? farmLocationLng,
    String? cropType,
  }) async {
    final url = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.profileUpdate}');

    final body = <String, dynamic>{};
    if (fullName != null) body['full_name'] = fullName;
    if (email != null) body['email'] = email;
    if (farmLocationName != null) body['farm_location_name'] = farmLocationName;
    if (farmLocationLat != null) body['farm_location_lat'] = farmLocationLat;
    if (farmLocationLng != null) body['farm_location_lng'] = farmLocationLng;
    if (cropType != null) body['crop_type'] = cropType;

    final response = await appHttpClient.put(
      url,
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: json.encode(body),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return User.fromJson(data);
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else if (response.statusCode == 409) {
      throw Exception('Email already in use by another account');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to update profile');
    }
  }

  /// Change the current user's password.
  static Future<void> changePassword({
    required String token,
    required String currentPassword,
    required String newPassword,
  }) async {
    final url = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.changePassword}');

    final response = await appHttpClient.post(
      url,
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: json.encode({
        'current_password': currentPassword,
        'new_password': newPassword,
      }),
    );

    if (response.statusCode == 200) {
      return;
    } else if (response.statusCode == 400) {
      throw Exception('Current password is incorrect');
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to change password');
    }
  }

  /// Get the current authenticated user's profile.
  /// Requires a valid JWT token.
  /// Returns the User on success.
  /// Throws an exception on failure.
  static Future<User> getCurrentUser(String token) async {
    final url = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.me}');

    final response = await appHttpClient.get(
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
