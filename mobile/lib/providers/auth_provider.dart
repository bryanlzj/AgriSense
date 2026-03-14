import 'package:flutter/foundation.dart';
import 'package:fyp_prototype/models/user.dart';
import 'package:fyp_prototype/services/auth_service.dart';
import 'package:fyp_prototype/utils/token_storage.dart';

/// Authentication state for the app.
enum AuthStatus {
  initial,      // App just started, checking auth
  authenticated,
  unauthenticated,
}

/// Global authentication provider using ChangeNotifier.
/// Manages user session, login, logout, and token refresh.
class AuthProvider extends ChangeNotifier {
  AuthStatus _status = AuthStatus.initial;
  User? _user;
  String? _token;
  String? _errorMessage;
  bool _isLoading = false;

  // Getters
  AuthStatus get status => _status;
  User? get user => _user;
  String? get token => _token;
  String? get errorMessage => _errorMessage;
  bool get isLoading => _isLoading;
  bool get isAuthenticated => _status == AuthStatus.authenticated;

  /// Check if user is already logged in (on app startup).
  Future<void> checkAuthStatus() async {
    _isLoading = true;
    notifyListeners();

    try {
      final savedToken = await TokenStorage.getToken();

      if (savedToken == null) {
        _status = AuthStatus.unauthenticated;
        _isLoading = false;
        notifyListeners();
        return;
      }

      // Verify token is still valid by fetching user profile
      try {
        final user = await AuthService.getCurrentUser(savedToken);
        _token = savedToken;
        _user = user;
        _status = AuthStatus.authenticated;
      } catch (e) {
        // Token is invalid or expired
        await TokenStorage.deleteToken();
        _status = AuthStatus.unauthenticated;
      }
    } catch (e) {
      _status = AuthStatus.unauthenticated;
      _errorMessage = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Login with username and password.
  Future<bool> login(String username, String password) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final token = await AuthService.login(username, password);
      await TokenStorage.saveToken(token);

      // Fetch user profile
      final user = await AuthService.getCurrentUser(token);

      _token = token;
      _user = user;
      _status = AuthStatus.authenticated;
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString().replaceFirst('Exception: ', '');
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Register a new user.
  Future<bool> register({
    required String username,
    required String password,
    String? fullName,
    String? email,
    required String farmLocationName,
    required double farmLocationLat,
    required double farmLocationLng,
    required String cropType,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      await AuthService.register(
        username: username,
        password: password,
        fullName: fullName,
        email: email,
        farmLocationName: farmLocationName,
        farmLocationLat: farmLocationLat,
        farmLocationLng: farmLocationLng,
        cropType: cropType,
      );

      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString().replaceFirst('Exception: ', '');
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Update user profile.
  Future<bool> updateProfile({
    String? fullName,
    String? email,
    String? farmLocationName,
    double? farmLocationLat,
    double? farmLocationLng,
    String? cropType,
  }) async {
    if (_token == null) return false;

    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final updatedUser = await AuthService.updateProfile(
        token: _token!,
        fullName: fullName,
        email: email,
        farmLocationName: farmLocationName,
        farmLocationLat: farmLocationLat,
        farmLocationLng: farmLocationLng,
        cropType: cropType,
      );
      _user = updatedUser;
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString().replaceFirst('Exception: ', '');
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Change user password.
  Future<bool> changePassword({
    required String currentPassword,
    required String newPassword,
  }) async {
    if (_token == null) return false;

    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      await AuthService.changePassword(
        token: _token!,
        currentPassword: currentPassword,
        newPassword: newPassword,
      );
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString().replaceFirst('Exception: ', '');
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Logout and clear session.
  Future<void> logout() async {
    _isLoading = true;
    notifyListeners();

    await TokenStorage.deleteToken();

    _token = null;
    _user = null;
    _status = AuthStatus.unauthenticated;
    _errorMessage = null;
    _isLoading = false;
    notifyListeners();
  }

  /// Handle session expiration (called when API returns 401).
  Future<void> handleSessionExpired() async {
    await TokenStorage.deleteToken();
    _token = null;
    _user = null;
    _status = AuthStatus.unauthenticated;
    _errorMessage = 'Session expired. Please login again.';
    notifyListeners();
  }

  /// Clear error message.
  void clearError() {
    _errorMessage = null;
    notifyListeners();
  }

  /// Refresh user profile data.
  Future<void> refreshUser() async {
    if (_token == null) return;

    try {
      final user = await AuthService.getCurrentUser(_token!);
      _user = user;
      notifyListeners();
    } catch (e) {
      // If refresh fails due to auth error, handle session expiry
      if (e.toString().contains('401') || e.toString().contains('Session expired')) {
        await handleSessionExpired();
      }
    }
  }
}
