import 'package:flutter/material.dart';
import 'package:fyp_prototype/utils/extensions.dart';
import 'package:fyp_prototype/widgets/custom_form_field.dart';
import 'package:google_fonts/google_fonts.dart';

class ResetPasswordPage extends StatefulWidget {
  const ResetPasswordPage({super.key});

  @override
  State<ResetPasswordPage> createState() => _ResetPasswordPageState();
}

class _ResetPasswordPageState extends State<ResetPasswordPage> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController passwordController = TextEditingController();
  final TextEditingController confirmPasswordController =
      TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Padding(
        padding: EdgeInsetsGeometry.symmetric(horizontal: 20),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              SizedBox(height: 40),
              BackButton(
                onPressed: () {
                  Navigator.pushReplacementNamed(context, '/login');
                },
              ),
              SizedBox(height: 30),
              Padding(
                padding: EdgeInsetsGeometry.symmetric(horizontal: 20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Set a new password',
                      style: GoogleFonts.poppins(
                        fontWeight: FontWeight.w500,
                        fontSize: 20,
                      ),
                    ),
                    SizedBox(height: 10),
                    Text(
                      'Create a new password. Ensure it differs from previous ones for security',
                      style: TextStyle(color: Color(0xFF989898)),
                    ),
                    SizedBox(height: 40),
                    CustomFormField(
                      controller: passwordController,
                      hintText: 'Enter your new password',
                      isPassword: true,
                      validator: (val) {
                        if (!val!.isValidPassword) {
                          return 'Password must be 8+ chars, include upper, lower, number, special';
                          //Password must be 8+ chars, include upper, lower, number, special
                        }
                        return null;
                      },
                    ),
                    CustomFormField(
                      controller: confirmPasswordController,
                      hintText: 'Confirm your new password',
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
                    SizedBox(height: 30),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: () {
                          if (_formKey.currentState!.validate()) {
                            _formKey.currentState!.save();
                            //backend function
                            Navigator.pushReplacementNamed(context, '/success');
                          }
                        },
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Color(0xFF4BAE4F),
                          foregroundColor: Color(0xFFFFFFFF),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadiusGeometry.circular(8),
                          ),
                        ),
                        child: Text(
                          'Continue',
                          style: TextStyle(
                            //fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
