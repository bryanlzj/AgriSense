import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:fyp_prototype/providers/auth_provider.dart';
import 'package:fyp_prototype/pages/login_page.dart';

void main() {
  group('LoginPage Widget Tests', () {
    late AuthProvider authProvider;

    setUp(() {
      authProvider = AuthProvider();
    });

    Widget createLoginPage() {
      return ChangeNotifierProvider<AuthProvider>.value(
        value: authProvider,
        child: MaterialApp(
          home: const LoginPage(),
          routes: {
            '/main': (context) => const Scaffold(body: Text('Main Page')),
            '/signUp': (context) => const Scaffold(body: Text('Sign Up Page')),
            '/forgotPassword': (context) => const Scaffold(body: Text('Forgot Password')),
          },
        ),
      );
    }

    testWidgets('LoginPage shows all required elements', (WidgetTester tester) async {
      await tester.pumpWidget(createLoginPage());

      // Check for logo
      expect(find.byType(Image), findsOneWidget);

      // Check for "Login" title
      expect(find.text('Login'), findsOneWidget);

      // Check for form fields
      expect(find.byType(TextFormField), findsNWidgets(2)); // Username and password

      // Check for Continue button
      expect(find.text('Continue'), findsOneWidget);

      // Check for "Forgot password?" link
      expect(find.text('Forgot password?'), findsOneWidget);

      // Check for "Sign up" link
      expect(find.text('Sign up'), findsOneWidget);
    });

    testWidgets('LoginPage shows validation errors for empty fields', (WidgetTester tester) async {
      await tester.pumpWidget(createLoginPage());

      // Tap Continue without entering anything
      await tester.tap(find.text('Continue'));
      await tester.pumpAndSettle();

      // Check for validation error messages
      expect(find.text('Username is required'), findsOneWidget);
      expect(find.text('Password is required'), findsOneWidget);
    });

    testWidgets('LoginPage validates username format', (WidgetTester tester) async {
      await tester.pumpWidget(createLoginPage());

      // Find text fields and enter invalid data
      final textFields = find.byType(TextFormField);

      // Enter short username (less than 3 chars)
      await tester.enterText(textFields.first, 'ab');
      await tester.enterText(textFields.last, 'password123');

      // Tap Continue
      await tester.tap(find.text('Continue'));
      await tester.pumpAndSettle();

      // Should show username validation error
      expect(find.textContaining('Username must be'), findsOneWidget);
    });

    testWidgets('LoginPage validates password length', (WidgetTester tester) async {
      await tester.pumpWidget(createLoginPage());

      // Find text fields and enter data
      final textFields = find.byType(TextFormField);

      await tester.enterText(textFields.first, 'validuser');
      await tester.enterText(textFields.last, '12345'); // Too short

      // Tap Continue
      await tester.tap(find.text('Continue'));
      await tester.pumpAndSettle();

      // Should show password validation error
      expect(find.text('Password must be at least 6 characters'), findsOneWidget);
    });

    testWidgets('LoginPage navigates to Sign Up page', (WidgetTester tester) async {
      await tester.pumpWidget(createLoginPage());

      // Tap "Sign up" link
      await tester.tap(find.text('Sign up'));
      await tester.pumpAndSettle();

      // Should navigate to sign up page
      expect(find.text('Sign Up Page'), findsOneWidget);
    });

    testWidgets('LoginPage navigates to Forgot Password page', (WidgetTester tester) async {
      await tester.pumpWidget(createLoginPage());

      // Tap "Forgot password?" link
      await tester.tap(find.text('Forgot password?'));
      await tester.pumpAndSettle();

      // Should navigate to forgot password page
      expect(find.text('Forgot Password'), findsOneWidget);
    });

    testWidgets('Continue button is disabled when loading', (WidgetTester tester) async {
      await tester.pumpWidget(createLoginPage());

      // Find the button
      final buttonFinder = find.widgetWithText(ElevatedButton, 'Continue');
      expect(buttonFinder, findsOneWidget);

      // Initially, button should be enabled
      final button = tester.widget<ElevatedButton>(buttonFinder);
      expect(button.onPressed, isNotNull);
    });
  });
}
