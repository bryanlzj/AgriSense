import 'package:flutter_test/flutter_test.dart';
import 'package:fyp_prototype/utils/error_handler.dart';

void main() {
  group('ErrorHandler', () {
    group('parseError', () {
      test('removes Exception: prefix', () {
        final result = ErrorHandler.parseError('Exception: Something went wrong');
        expect(result, 'Something went wrong');
      });

      test('converts SocketException to user-friendly message', () {
        final result = ErrorHandler.parseError('SocketException: Connection refused');
        expect(result, 'Unable to connect to server. Please check your internet connection.');
      });

      test('converts TimeoutException to user-friendly message', () {
        final result = ErrorHandler.parseError('TimeoutException after 30 seconds');
        expect(result, 'Request timed out. Please try again.');
      });

      test('converts 401 error to session expired message', () {
        final result = ErrorHandler.parseError('Error 401: Unauthorized');
        expect(result, 'Session expired. Please login again.');
      });

      test('converts 403 error to permission denied message', () {
        final result = ErrorHandler.parseError('Error 403: Forbidden');
        expect(result, 'You do not have permission to perform this action.');
      });

      test('converts 404 error to not found message', () {
        final result = ErrorHandler.parseError('Error 404: Not Found');
        expect(result, 'The requested resource was not found.');
      });

      test('converts 500 error to server error message', () {
        final result = ErrorHandler.parseError('Error 500: Internal Server Error');
        expect(result, 'Server error. Please try again later.');
      });

      test('returns original message for unknown errors', () {
        final result = ErrorHandler.parseError('Something unexpected happened');
        expect(result, 'Something unexpected happened');
      });
    });

    group('isAuthError', () {
      test('returns true for 401 errors', () {
        expect(ErrorHandler.isAuthError('Error 401'), isTrue);
      });

      test('returns true for Session expired errors', () {
        expect(ErrorHandler.isAuthError('Session expired'), isTrue);
      });

      test('returns true for Unauthorized errors', () {
        expect(ErrorHandler.isAuthError('Unauthorized access'), isTrue);
      });

      test('returns false for other errors', () {
        expect(ErrorHandler.isAuthError('Network error'), isFalse);
      });
    });

    group('isNetworkError', () {
      test('returns true for SocketException', () {
        expect(ErrorHandler.isNetworkError('SocketException'), isTrue);
      });

      test('returns true for Connection refused', () {
        expect(ErrorHandler.isNetworkError('Connection refused'), isTrue);
      });

      test('returns true for TimeoutException', () {
        expect(ErrorHandler.isNetworkError('TimeoutException'), isTrue);
      });

      test('returns true for Network is unreachable', () {
        expect(ErrorHandler.isNetworkError('Network is unreachable'), isTrue);
      });

      test('returns false for other errors', () {
        expect(ErrorHandler.isNetworkError('Invalid data'), isFalse);
      });
    });
  });
}
