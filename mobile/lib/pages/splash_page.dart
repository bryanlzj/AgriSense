import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';


class Splashpage extends StatelessWidget {
  const Splashpage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: Padding(
          padding: const EdgeInsets.only(bottom: 60),
          child: Column(            
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Image.asset(
                'assets/images/logo.png',
                width: 265,
                height: 265,
                ),
              Text(
                'AgriSense',
                style: GoogleFonts.quattrocento(
                  fontSize: 40,
                  color: Color(0xFF078456),
                  ), 
                )
            ],
          ),
        ),
      )
    );
  }
}