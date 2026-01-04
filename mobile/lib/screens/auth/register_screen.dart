import 'package:flutter/material.dart';

/// Register screen
/// 
/// TODO: Implement registration functionality
/// - Username, password, full name input fields
/// - Register button
/// - Navigate back to LoginScreen
/// - Call AuthService.register()
/// - Show success message
/// - Navigate to LoginScreen on success
class RegisterScreen extends StatelessWidget {
  const RegisterScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Register'),
      ),
      body: const Center(
        child: Text('TODO: Implement RegisterScreen'),
      ),
    );
  }
}
