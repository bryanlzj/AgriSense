import 'package:flutter/material.dart';

/// Pest detection history screen
/// 
/// TODO: Implement pest history with:
/// - List of past pest detections
/// - Image thumbnail for each detection
/// - Pest type and confidence
/// - Date and time
/// - Tap to view details
/// - Filter by pest type
/// - Call PestService.getPestDetections()
class PestHistoryScreen extends StatelessWidget {
  const PestHistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Pest History'),
      ),
      body: const Center(
        child: Text('TODO: Implement PestHistoryScreen'),
      ),
    );
  }
}
