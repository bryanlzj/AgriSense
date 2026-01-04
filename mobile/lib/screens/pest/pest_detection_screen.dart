import 'package:flutter/material.dart';

/// Pest detection screen
/// 
/// TODO: Implement pest detection with:
/// - Camera button to take photo
/// - Gallery button to select existing photo
/// - Image preview
/// - Detect button
/// - Loading indicator during detection
/// - Display detection results (pest type, confidence, recommendations)
/// - Call PestService.detectPest()
/// - Use image_picker package for camera/gallery
class PestDetectionScreen extends StatelessWidget {
  const PestDetectionScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Pest Detection'),
      ),
      body: const Center(
        child: Text('TODO: Implement PestDetectionScreen'),
      ),
    );
  }
}
