import 'package:shared_preferences/shared_preferences.dart';
import 'constants.dart';

/// Local storage utility for storing JWT token and user data
class StorageService {
  static SharedPreferences? _prefs;

  /// Initialize SharedPreferences
  static Future<void> init() async {
    _prefs ??= await SharedPreferences.getInstance();
  }

  /// Ensure SharedPreferences is initialized
  static Future<SharedPreferences> _getPrefs() async {
    if (_prefs == null) {
      await init();
    }
    return _prefs!;
  }

  // ==========================================================================
  // Authentication
  // ==========================================================================

  /// Save JWT access token
  static Future<bool> saveAccessToken(String token) async {
    final prefs = await _getPrefs();
    return prefs.setString(StorageKeys.accessToken, token);
  }

  /// Get JWT access token
  static Future<String?> getAccessToken() async {
    final prefs = await _getPrefs();
    return prefs.getString(StorageKeys.accessToken);
  }

  /// Check if user is logged in (has valid token)
  static Future<bool> isLoggedIn() async {
    final token = await getAccessToken();
    return token != null && token.isNotEmpty;
  }

  /// Clear access token (logout)
  static Future<bool> clearAccessToken() async {
    final prefs = await _getPrefs();
    return prefs.remove(StorageKeys.accessToken);
  }

  // ==========================================================================
  // User Data
  // ==========================================================================

  /// Save user ID
  static Future<bool> saveUserId(int userId) async {
    final prefs = await _getPrefs();
    return prefs.setInt(StorageKeys.userId, userId);
  }

  /// Get user ID
  static Future<int?> getUserId() async {
    final prefs = await _getPrefs();
    return prefs.getInt(StorageKeys.userId);
  }

  /// Save username
  static Future<bool> saveUsername(String username) async {
    final prefs = await _getPrefs();
    return prefs.setString(StorageKeys.username, username);
  }

  /// Get username
  static Future<String?> getUsername() async {
    final prefs = await _getPrefs();
    return prefs.getString(StorageKeys.username);
  }

  /// Save full name
  static Future<bool> saveFullName(String fullName) async {
    final prefs = await _getPrefs();
    return prefs.setString(StorageKeys.fullName, fullName);
  }

  /// Get full name
  static Future<String?> getFullName() async {
    final prefs = await _getPrefs();
    return prefs.getString(StorageKeys.fullName);
  }

  // ==========================================================================
  // Complete User Session
  // ==========================================================================

  /// Save complete user session (token + user data)
  static Future<void> saveUserSession({
    required String token,
    required int userId,
    required String username,
    required String fullName,
  }) async {
    await saveAccessToken(token);
    await saveUserId(userId);
    await saveUsername(username);
    await saveFullName(fullName);
  }

  /// Clear all user data (complete logout)
  static Future<void> clearUserSession() async {
    final prefs = await _getPrefs();
    await prefs.remove(StorageKeys.accessToken);
    await prefs.remove(StorageKeys.userId);
    await prefs.remove(StorageKeys.username);
    await prefs.remove(StorageKeys.fullName);
  }

  // ==========================================================================
  // Generic Storage Methods
  // ==========================================================================

  /// Save string value
  static Future<bool> setString(String key, String value) async {
    final prefs = await _getPrefs();
    return prefs.setString(key, value);
  }

  /// Get string value
  static Future<String?> getString(String key) async {
    final prefs = await _getPrefs();
    return prefs.getString(key);
  }

  /// Save int value
  static Future<bool> setInt(String key, int value) async {
    final prefs = await _getPrefs();
    return prefs.setInt(key, value);
  }

  /// Get int value
  static Future<int?> getInt(String key) async {
    final prefs = await _getPrefs();
    return prefs.getInt(key);
  }

  /// Save bool value
  static Future<bool> setBool(String key, bool value) async {
    final prefs = await _getPrefs();
    return prefs.setBool(key, value);
  }

  /// Get bool value
  static Future<bool?> getBool(String key) async {
    final prefs = await _getPrefs();
    return prefs.getBool(key);
  }

  /// Remove value by key
  static Future<bool> remove(String key) async {
    final prefs = await _getPrefs();
    return prefs.remove(key);
  }

  /// Clear all stored data
  static Future<bool> clearAll() async {
    final prefs = await _getPrefs();
    return prefs.clear();
  }
}
