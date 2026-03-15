import 'package:flutter/material.dart';
import 'package:fyp_prototype/widgets/custom_app_bar.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:url_launcher/url_launcher.dart';

class HelpSupportPage extends StatelessWidget {
  const HelpSupportPage({super.key});

  static const List<Map<String, String>> _faqs = [
    {
      'question': 'What is AgriSense?',
      'answer': 'AgriSense is an IoT-driven agricultural monitoring system that helps farmers track environmental conditions, detect pests using AI, and make data-driven decisions for their crops.',
    },
    {
      'question': 'How does pest detection work?',
      'answer': 'Upload a photo of your crop and our AI model will analyze it to identify pests. The system returns the pest type, confidence score, and recommended actions to take.',
    },
    {
      'question': 'How do I set up farm sectors?',
      'answer': 'Go to Settings > Farm Management. Tap "Add Sector" to create a new sector with crop type, area, and planting date. You can edit or delete sectors at any time.',
    },
    {
      'question': 'What environmental data is tracked?',
      'answer': 'AgriSense monitors temperature, relative humidity, soil moisture, rainfall, wind speed, and solar radiation. Data is updated regularly and displayed on your dashboard.',
    },
    {
      'question': 'How do I import historical data?',
      'answer': 'Go to Settings > Import Dataset. Select a CSV file with your sensor data. The system will validate the columns and import matching data into your account.',
    },
    {
      'question': 'How does weather forecasting work?',
      'answer': 'AgriSense uses the Open-Meteo API to provide a 5-day weather forecast for your farm location. Forecasts are updated every 10 minutes and include temperature, rainfall, and humidity predictions.',
    },
  ];

  Future<void> _launchUrl(String url) async {
    final uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    }
  }

  Future<void> _launchEmail(String email) async {
    final uri = Uri(scheme: 'mailto', path: email);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CustomAppBar(title: 'Help & Support', subtitle: 'FAQs and contact support'),
      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Frequently Asked Questions', style: GoogleFonts.scheherazadeNew(fontSize: 20, fontWeight: FontWeight.w500)),
            const SizedBox(height: 10),
            ..._faqs.map((faq) => ExpansionTile(
              tilePadding: const EdgeInsets.symmetric(horizontal: 0),
              title: Text(faq['question']!, style: GoogleFonts.inter(fontSize: 14, fontWeight: FontWeight.w600)),
              childrenPadding: const EdgeInsets.only(bottom: 12),
              children: [
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 0),
                  child: Text(faq['answer']!, style: GoogleFonts.inter(fontSize: 13, color: Colors.grey[700], height: 1.5)),
                ),
              ],
            )),

            const SizedBox(height: 30),
            const Divider(),
            const SizedBox(height: 20),

            Text('Contact Support', style: GoogleFonts.scheherazadeNew(fontSize: 20, fontWeight: FontWeight.w500)),
            const SizedBox(height: 15),
            ListTile(
              contentPadding: EdgeInsets.zero,
              leading: const Icon(Icons.email_outlined, color: Color(0xFF53AD64)),
              title: const Text('Email Support', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
              subtitle: const Text('support@agrisense.app', style: TextStyle(fontSize: 13, color: Color(0xFF53AD64))),
              onTap: () => _launchEmail('support@agrisense.app'),
            ),
            ListTile(
              contentPadding: EdgeInsets.zero,
              leading: const Icon(Icons.code, color: Color(0xFF53AD64)),
              title: const Text('GitHub Repository', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
              subtitle: const Text('Report issues or contribute', style: TextStyle(fontSize: 13, color: Colors.grey)),
              onTap: () => _launchUrl('https://github.com/bryanlzj/AgriSense'),
            ),
          ],
        ),
      ),
    );
  }
}
