import 'package:flutter/material.dart';

/// Utility class for consistent error handling across the app.
class ErrorHandler {
  /// Show a snackbar error message.
  static void showError(BuildContext context, String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            Icon(Icons.error_outline, color: Colors.white, size: 20),
            SizedBox(width: 8),
            Expanded(
              child: Text(
                _cleanErrorMessage(message),
                style: TextStyle(fontSize: 14),
              ),
            ),
          ],
        ),
        backgroundColor: Colors.red.shade600,
        behavior: SnackBarBehavior.floating,
        margin: EdgeInsets.all(16),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
        duration: Duration(seconds: 4),
      ),
    );
  }

  /// Show a success snackbar message.
  static void showSuccess(BuildContext context, String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            Icon(Icons.check_circle_outline, color: Colors.white, size: 20),
            SizedBox(width: 8),
            Expanded(
              child: Text(
                message,
                style: TextStyle(fontSize: 14),
              ),
            ),
          ],
        ),
        backgroundColor: Color(0xFF4BAE4F),
        behavior: SnackBarBehavior.floating,
        margin: EdgeInsets.all(16),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
        duration: Duration(seconds: 3),
      ),
    );
  }

  /// Show an info snackbar message.
  static void showInfo(BuildContext context, String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            Icon(Icons.info_outline, color: Colors.white, size: 20),
            SizedBox(width: 8),
            Expanded(
              child: Text(
                message,
                style: TextStyle(fontSize: 14),
              ),
            ),
          ],
        ),
        backgroundColor: Colors.blue.shade600,
        behavior: SnackBarBehavior.floating,
        margin: EdgeInsets.all(16),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
        duration: Duration(seconds: 3),
      ),
    );
  }

  /// Show a warning snackbar message.
  static void showWarning(BuildContext context, String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            Icon(Icons.warning_amber_outlined, color: Colors.white, size: 20),
            SizedBox(width: 8),
            Expanded(
              child: Text(
                message,
                style: TextStyle(fontSize: 14),
              ),
            ),
          ],
        ),
        backgroundColor: Colors.orange.shade600,
        behavior: SnackBarBehavior.floating,
        margin: EdgeInsets.all(16),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
        duration: Duration(seconds: 4),
      ),
    );
  }

  /// Clean up exception messages for display.
  static String _cleanErrorMessage(String message) {
    // Remove "Exception: " prefix
    String cleaned = message.replaceFirst('Exception: ', '');

    // Handle common error messages
    if (cleaned.contains('SocketException') || cleaned.contains('Connection refused')) {
      return 'Unable to connect to server. Please check your internet connection.';
    }
    if (cleaned.contains('TimeoutException')) {
      return 'Request timed out. Please try again.';
    }
    if (cleaned.contains('FormatException')) {
      return 'Invalid response from server. Please try again.';
    }
    if (cleaned.contains('401')) {
      return 'Session expired. Please login again.';
    }
    if (cleaned.contains('403')) {
      return 'You do not have permission to perform this action.';
    }
    if (cleaned.contains('404')) {
      return 'The requested resource was not found.';
    }
    if (cleaned.contains('500')) {
      return 'Server error. Please try again later.';
    }

    return cleaned;
  }

  /// Parse error from exception and return user-friendly message.
  static String parseError(dynamic error) {
    return _cleanErrorMessage(error.toString());
  }

  /// Check if error is an authentication error (401).
  static bool isAuthError(dynamic error) {
    final message = error.toString();
    return message.contains('401') ||
           message.contains('Session expired') ||
           message.contains('Unauthorized');
  }

  /// Check if error is a network error.
  static bool isNetworkError(dynamic error) {
    final message = error.toString();
    return message.contains('SocketException') ||
           message.contains('Connection refused') ||
           message.contains('TimeoutException') ||
           message.contains('Network is unreachable');
  }
}
