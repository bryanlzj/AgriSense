import 'package:flutter/material.dart';
import 'package:fyp_prototype/utils/extensions.dart';
import 'package:fyp_prototype/widgets/custom_form_field.dart';
import 'package:google_fonts/google_fonts.dart';

class SignUpPage extends StatefulWidget {
  const SignUpPage({super.key});

  @override
  State<SignUpPage> createState() => _SignUpPageState();
}

class _SignUpPageState extends State<SignUpPage> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController nameController = TextEditingController();
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  final TextEditingController confirmPasswordController = TextEditingController();

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
                  SizedBox(height: 80),
                  Image.asset(
                    'assets/images/logo.png',
                    width: 140,
                    height: 140,
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
                  SizedBox(height: 20),
                  CustomFormField(
                    controller: nameController,
                    hintText: 'Enter your name',
                    validator: (val) {
                      if (!val!.isValidName) {
                        return 'Enter a valid name';
                      }
                      return null;
                    },
                  ),
                  CustomFormField(
                    controller: emailController,
                    hintText: 'Enter your email',
                    validator: (val) {
                      if (!val!.isValidEmail) {
                        return 'Enter a valid email';
                      }
                      return null;
                    },
                  ),
                  CustomFormField(
                    controller: passwordController,
                    hintText: 'Enter your password',
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
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: () {
                        if (_formKey.currentState!.validate()) {
                          _formKey.currentState!.save();
                          Navigator.pushReplacementNamed(context, '/main');
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
                        'Create account',
                        style: TextStyle(fontSize: 16,fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
                  SizedBox(height: 10),
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
                        onPressed: () {
                          Navigator.pushReplacementNamed(context, '/login');
                        },
                        style: TextButton.styleFrom(
                          //side: BorderSide(color: Colors.black),
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
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
