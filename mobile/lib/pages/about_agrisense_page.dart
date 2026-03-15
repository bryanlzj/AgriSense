import 'package:flutter/material.dart';
import 'package:fyp_prototype/widgets/custom_app_bar.dart';
import 'package:google_fonts/google_fonts.dart';

class AboutAgrisensePage extends StatelessWidget {
  const AboutAgrisensePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CustomAppBar(title: 'About AgriSense', subtitle: 'App information'),
      backgroundColor: Colors.white,
      body: Center(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 30),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Image.asset('assets/images/logo.png', width: 100, height: 100),
              const SizedBox(height: 20),
              Text(
                'AgriSense',
                style: GoogleFonts.scheherazadeNew(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: const Color(0xFF2E7D32),
                ),
              ),
              const SizedBox(height: 6),
              Text(
                'Version 1.0.0',
                style: GoogleFonts.inter(fontSize: 14, color: Colors.grey[600]),
              ),
              const SizedBox(height: 24),
              Text(
                'AgriSense is an IoT-driven agricultural monitoring system that helps farmers track environmental conditions, detect pests, and make data-driven decisions for their crops.',
                textAlign: TextAlign.center,
                style: GoogleFonts.inter(fontSize: 14, color: Colors.grey[700], height: 1.6),
              ),
              const SizedBox(height: 30),
              const Divider(),
              const SizedBox(height: 20),
              Text(
                'Built with Flutter & FastAPI',
                style: GoogleFonts.inter(fontSize: 12, color: Colors.grey[500]),
              ),
              const SizedBox(height: 6),
              Text(
                '\u00a9 2026 AgriSense Team',
                style: GoogleFonts.inter(fontSize: 12, color: Colors.grey[400]),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
