import 'dart:convert';
import 'package:http/http.dart' as http;
import '../utils/constants.dart';
import '../utils/storage.dart';

/// Authentication service for API calls
class AuthService {
  /// Register new user
  /// 
  /// POST /api/v1/auth/register
  /// 
  /// TODO: Implement registration
  /// - Send username, password, full_name to backend
  /// - Return success/error message
  /// - Handle validation errors
  Future<Map<String, dynamic>> register({
    required String username,
    required String password,
    required String fullName,
  }) async {
    // TODO: Implement
    throw UnimplementedError('AuthService.register() not implemented');
  }

  /// Login user
  /// 
  /// POST /api/v1/auth/login
  /// 
  /// TODO: Implement login
  /// - Send username and password to backend
  /// - Receive JWT access token
  /// - Save token to StorageService
  /// - Return user data
  Future<Map<String, dynamic>> login({
    required String username,
    required String password,
  }) async {
    // TODO: Implement
    throw UnimplementedError('AuthService.login() not implemented');
  }

  /// Get current user
  /// 
  /// GET /api/v1/auth/me
  /// 
  /// TODO: Implement get current user
  /// - Get JWT token from StorageService
  /// - Send token in Authorization header
  /// - Return user data
  Future<Map<String, dynamic>> getCurrentUser() async {
    // TODO: Implement
    throw UnimplementedError('AuthService.getCurrentUser() not implemented');
  }

  /// Logout user
  /// 
  /// TODO: Implement logout
  /// - Clear JWT token from StorageService
  /// - Clear user data
  Future<void> logout() async {
    await StorageService.clearUserSession();
  }

  /// Check if user is logged in
  Future<bool> isLoggedIn() async {
    return await StorageService.isLoggedIn();
  }
}
