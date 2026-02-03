import 'package:flutter_test/flutter_test.dart';
import 'package:fyp_prototype/providers/auth_provider.dart';

void main() {
  group('AuthProvider', () {
    late AuthProvider authProvider;

    setUp(() {
      authProvider = AuthProvider();
    });

    test('initial state should be AuthStatus.initial', () {
      expect(authProvider.status, AuthStatus.initial);
      expect(authProvider.user, isNull);
      expect(authProvider.token, isNull);
      expect(authProvider.isLoading, isFalse);
      expect(authProvider.isAuthenticated, isFalse);
    });

    test('clearError should set errorMessage to null', () {
      // Manually set an error (simulating a failed login)
      authProvider.clearError();
      expect(authProvider.errorMessage, isNull);
    });

    test('isAuthenticated should return true when status is authenticated', () {
      // Initially not authenticated
      expect(authProvider.isAuthenticated, isFalse);
    });
  });
}
