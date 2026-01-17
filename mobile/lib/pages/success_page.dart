import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class SuccessPage extends StatelessWidget {
  const SuccessPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 40.0),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Container(
                height: 100,
                width: 100,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: Color(0x7060AC75),
                  border: Border.all(
                    color: Color(0xFF4BAE4F), // border color
                    width: 2,
                  ),
                ),
                child: Center(
                  child: Icon(
                    Icons.check,
                    color: Color(0xFF4BAE4F), // tick color (matches border)
                    size: 36,
                    semanticLabel: 'Success',
                  ),
                ),
              ),
              SizedBox(height: 20,),
              Text(
                'Successful',
                style: GoogleFonts.poppins(
                  fontWeight: FontWeight.w500,
                  fontSize: 20,
                ),
              ),
              SizedBox(height: 20,),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 30.0),
                child: Text(
                  'Congratulations! Your password has been changed. Click continue to login',
                  textAlign: TextAlign.center,
                  style: TextStyle(color: Color(0xFF989898)),
                ),
              ),
              SizedBox(height: 40,),
              SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: () {
                        Navigator.pushReplacementNamed(context, '/login');
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
                        style: TextStyle(fontSize: 16,fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
            ],
          ),
        ),
      ),
    );
  }
}
