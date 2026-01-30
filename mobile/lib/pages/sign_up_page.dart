import 'package:flutter/material.dart';
import 'package:fyp_prototype/utils/extensions.dart';
import 'package:fyp_prototype/widgets/custom_form_field.dart';
import 'package:fyp_prototype/services/auth_service.dart';
import 'package:google_fonts/google_fonts.dart';

class SignUpPage extends StatefulWidget {
  const SignUpPage({super.key});

  @override
  State<SignUpPage> createState() => _SignUpPageState();
}

class _SignUpPageState extends State<SignUpPage> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController nameController = TextEditingController();
  final TextEditingController usernameController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  final TextEditingController confirmPasswordController = TextEditingController();
  final TextEditingController farmLocationController = TextEditingController();

  String _selectedCropType = 'rice';
  bool _isLoading = false;
  String? _errorMessage;

  final List<Map<String, String>> _cropTypes = [
    {'value': 'rice', 'label': 'Rice'},
    {'value': 'vegetables', 'label': 'Vegetables'},
    {'value': 'corn', 'label': 'Corn'},
    {'value': 'oil_palm', 'label': 'Oil Palm'},
    {'value': 'rubber', 'label': 'Rubber'},
  ];

  Future<void> _handleSignUp() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      await AuthService.register(
        username: usernameController.text.trim(),
        password: passwordController.text,
        fullName: nameController.text.trim(),
        farmLocationName: farmLocationController.text.trim().isEmpty
            ? 'Kuala Lumpur'
            : farmLocationController.text.trim(),
        cropType: _selectedCropType,
      );

      if (!mounted) return;

      // Show success message and navigate to login
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Account created successfully! Please login.'),
          backgroundColor: Color(0xFF4BAE4F),
        ),
      );

      Navigator.pushReplacementNamed(context, '/login');
    } catch (e) {
      setState(() {
        _errorMessage = e.toString().replaceFirst('Exception: ', '');
      });
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  void dispose() {
    nameController.dispose();
    usernameController.dispose();
    passwordController.dispose();
    confirmPasswordController.dispose();
    farmLocationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        child: Padding(
          padding: EdgeInsetsGeometry.symmetric(horizontal: 40),
          child: Form(
            key: _formKey,
            child: Center(
              child: Column(
                children: [
                  SizedBox(height: 60),
                  Image.asset(
                    'assets/images/logo.png',
                    width: 100,
                    height: 100,
                  ),
                  SizedBox(height: 10),
                  Text(
                    'Sign up',
                    style: GoogleFonts.inter(
                      color: Color(0xFF2E7D32),
                      fontWeight: FontWeight.bold,
                      fontSize: 20,
                    ),
                  ),
                  SizedBox(height: 10),
                  Text(
                    'Sign up to streamline crop management and enhance field productivity.',
                    style: GoogleFonts.inter(
                      color: Color(0xFF2E7D32),
                      fontSize: 12,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 15),

                  // Error message
                  if (_errorMessage != null)
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(12),
                      margin: const EdgeInsets.only(bottom: 10),
                      decoration: BoxDecoration(
                        color: Colors.red.shade50,
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(color: Colors.red.shade200),
                      ),
                      child: Text(
                        _errorMessage!,
                        style: TextStyle(color: Colors.red.shade700, fontSize: 13),
                      ),
                    ),

                  // Full Name
                  CustomFormField(
                    controller: nameController,
                    hintText: 'Enter your full name',
                    validator: (val) {
                      if (val == null || val.isEmpty) {
                        return 'Please enter your name';
                      }
                      if (!val.isValidName) {
                        return 'Enter a valid name';
                      }
                      return null;
                    },
                  ),

                  // Username
                  CustomFormField(
                    controller: usernameController,
                    hintText: 'Enter your username',
                    validator: (val) {
                      if (val == null || val.isEmpty) {
                        return 'Please enter a username';
                      }
                      if (!val.isValidUsername) {
                        return 'Username must be 3-50 characters (letters, numbers, underscore)';
                      }
                      return null;
                    },
                  ),

                  // Farm Location
                  CustomFormField(
                    controller: farmLocationController,
                    hintText: 'Farm location (e.g., Kuala Lumpur)',
                    validator: (val) {
                      // Optional field - no validation required
                      return null;
                    },
                  ),

                  // Crop Type Dropdown
                  Padding(
                    padding: EdgeInsetsGeometry.symmetric(vertical: 10),
                    child: DropdownButtonFormField<String>(
                      value: _selectedCropType,
                      decoration: InputDecoration(
                        hintText: 'Select crop type',
                        contentPadding: EdgeInsets.symmetric(vertical: 10, horizontal: 16),
                        hintStyle: TextStyle(
                          color: Color(0xFF828282),
                          fontSize: 14,
                        ),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                        enabledBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(8),
                          borderSide: BorderSide(color: Color(0xFFE0E0E0)),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(8),
                          borderSide: BorderSide(color: Color(0xFF53AD64)),
                        ),
                      ),
                      items: _cropTypes.map((crop) {
                        return DropdownMenuItem<String>(
                          value: crop['value'],
                          child: Text(crop['label']!),
                        );
                      }).toList(),
                      onChanged: (value) {
                        setState(() {
                          _selectedCropType = value ?? 'rice';
                        });
                      },
                    ),
                  ),

                  // Password
                  CustomFormField(
                    controller: passwordController,
                    hintText: 'Enter your password',
                    isPassword: true,
                    validator: (val) {
                      if (val == null || val.isEmpty) {
                        return 'Please enter a password';
                      }
                      if (!val.isValidPassword) {
                        return 'Password must be 8+ chars, include upper, lower, number, special';
                      }
                      return null;
                    },
                  ),

                  // Confirm Password
                  CustomFormField(
                    controller: confirmPasswordController,
                    hintText: 'Confirm your password',
                    isPassword: true,
                    validator: (val) {
                      if (val == null || val.isEmpty) {
                        return 'Please confirm your password';
                      }
                      if (val != passwordController.text) {
                        return 'Passwords do not match';
                      }
                      return null;
                    },
                  ),

                  SizedBox(height: 20),

                  // Submit Button
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: _isLoading ? null : _handleSignUp,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Color(0xFF4BAE4F),
                        foregroundColor: Color(0xFFFFFFFF),
                        disabledBackgroundColor: Color(0xFF4BAE4F).withOpacity(0.6),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadiusGeometry.circular(8),
                        ),
                      ),
                      child: _isLoading
                          ? SizedBox(
                              height: 20,
                              width: 20,
                              child: CircularProgressIndicator(
                                strokeWidth: 2,
                                valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                              ),
                            )
                          : Text(
                              'Create account',
                              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                            ),
                    ),
                  ),

                  SizedBox(height: 10),

                  // Login link
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        'Already have an account?',
                        style: TextStyle(
                          fontSize: 12,
                          color: Color(0xFF828282),
                        ),
                      ),
                      TextButton(
                        onPressed: _isLoading
                            ? null
                            : () {
                                Navigator.pushReplacementNamed(context, '/login');
                              },
                        style: TextButton.styleFrom(
                          padding: EdgeInsets.zero,
                          minimumSize: Size.zero,
                        ),
                        child: Text(
                          'Login',
                          style: TextStyle(color: Color(0xFF2C7730)),
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: 20),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
