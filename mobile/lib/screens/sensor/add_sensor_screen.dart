import 'package:flutter/material.dart';

/// Add sensor reading screen
/// 
/// TODO: Implement add sensor form with:
/// - Temperature input (°C)
/// - Humidity input (%)
/// - Soil moisture input (%)
/// - Rainfall input (mm)
/// - Location input (optional)
/// - Submit button
/// - Call SensorService.addSensorReading()
/// - Show success message
/// - Navigate back to SensorListScreen
class AddSensorScreen extends StatelessWidget {
  const AddSensorScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Add Sensor Reading'),
      ),
      body: const Center(
        child: Text('TODO: Implement AddSensorScreen'),
      ),
    );
  }
}
