import 'package:flutter/material.dart';

/// Dashboard screen (Home)
/// 
/// TODO: Implement dashboard with:
/// - Welcome message with user's name
/// - Overview cards (total sensors, active alerts, weather summary)
/// - Recent sensor readings
/// - Recent alerts
/// - Quick actions (Add Sensor, Detect Pest, View Weather)
/// - Bottom navigation bar (Dashboard, Sensors, Pest, Weather, Alerts)
class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard'),
      ),
      body: const Center(
        child: Text('TODO: Implement DashboardScreen'),
      ),
    );
  }
}
