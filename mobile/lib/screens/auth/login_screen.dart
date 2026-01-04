import 'package:flutter/material.dart';

/// Login screen
/// 
/// TODO: Implement login functionality
/// - Username and password input fields
/// - Login button
/// - Navigate to RegisterScreen
/// - Call AuthService.login()
/// - Save JWT token to StorageService
/// - Navigate to DashboardScreen on success
class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Login'),
      ),
      body: const Center(
        child: Text('TODO: Implement LoginScreen'),
      ),
    );
  }
}
