// Main test file that runs all test suites
//
// To run all tests:
//   flutter test
//
// To run specific test file:
//   flutter test test/unit/models_test.dart
//
// To run with coverage:
//   flutter test --coverage

import 'package:flutter_test/flutter_test.dart';

// Import test files
import 'unit/auth_provider_test.dart' as auth_provider_tests;
import 'unit/models_test.dart' as models_tests;
import 'unit/error_handler_test.dart' as error_handler_tests;
import 'widget/login_page_test.dart' as login_page_tests;

void main() {
  group('Unit Tests', () {
    auth_provider_tests.main();
    models_tests.main();
    error_handler_tests.main();
  });

  group('Widget Tests', () {
    login_page_tests.main();
  });
}
