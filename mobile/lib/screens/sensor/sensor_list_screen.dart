import 'package:flutter/material.dart';

/// Sensor data list screen
/// 
/// TODO: Implement sensor list with:
/// - List of sensor readings (temperature, humidity, soil moisture, rainfall)
/// - Date and time for each reading
/// - Filter by date range
/// - Pull to refresh
/// - Floating action button to add new sensor reading
/// - Call SensorService.getSensorReadings()
/// - Navigate to AddSensorScreen
class SensorListScreen extends StatelessWidget {
  const SensorListScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Sensor Data'),
      ),
      body: const Center(
        child: Text('TODO: Implement SensorListScreen'),
      ),
    );
  }
}
