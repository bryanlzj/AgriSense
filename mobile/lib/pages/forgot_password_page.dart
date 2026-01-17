import 'package:flutter/material.dart';
import 'package:fyp_prototype/utils/extensions.dart';
import 'package:fyp_prototype/widgets/custom_form_field.dart';
import 'package:google_fonts/google_fonts.dart';

class ForgotPasswordPage extends StatefulWidget {
  const ForgotPasswordPage({super.key});

  @override
  State<ForgotPasswordPage> createState() => _ForgotPasswordPageState();
}

class _ForgotPasswordPageState extends State<ForgotPasswordPage> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController emailController = TextEditingController();

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
                  Navigator.pop(context);
                },
              ),
              SizedBox(height: 30),
              Padding(
                padding: EdgeInsetsGeometry.symmetric(horizontal: 20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Forgot password',
                      style: GoogleFonts.poppins(
                        fontWeight: FontWeight.w500,
                        fontSize: 20,
                      ),
                    ),
                    SizedBox(height: 10),
                    Text(
                      'Please enter your email to reset the password',
                      style: TextStyle(color: Color(0xFF989898)),
                    ),
                    SizedBox(height: 40),
                    CustomFormField(
                      hintText: 'Enter your email',
                      validator: (val) {
                        if (!val!.isValidEmail) {
                          return 'Enter a valid email';
                        }
                        return null;
                      },
                      controller: emailController,
                    ),
                    SizedBox(height: 30),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: () {
                          if (_formKey.currentState!.validate()) {
                            //backend api
                            final email = emailController.text.trim();
                            _formKey.currentState!.save();
                            Navigator.pushNamed(
                              context,
                              '/otp',
                              arguments: email,
                            );
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
                          'Reset Password',
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
