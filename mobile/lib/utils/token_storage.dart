import 'package:shared_preferences/shared_preferences.dart';

/// Utility class for storing and retrieving JWT tokens.
class TokenStorage {
  static const String _tokenKey = 'auth_token';

  /// Save the JWT token to persistent storage.
  static Future<void> saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_tokenKey, token);
  }

  /// Retrieve the stored JWT token.
  /// Returns null if no token is stored.
  static Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_tokenKey);
  }

  /// Delete the stored token (used for logout).
  static Future<void> deleteToken() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_tokenKey);
  }

  /// Check if a token exists in storage.
  static Future<bool> hasToken() async {
    final token = await getToken();
    return token != null && token.isNotEmpty;
  }
}
