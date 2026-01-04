import 'package:flutter/material.dart';

/// Alerts screen
/// 
/// TODO: Implement alerts list with:
/// - List of alerts (weather, pest, sensor, system)
/// - Alert type icon and color
/// - Alert severity (info, warning, critical)
/// - Alert message
/// - Date and time
/// - Read/unread status
/// - Tap to mark as read
/// - Filter by type and severity
/// - Pull to refresh
/// - Call AlertService.getAlerts()
class AlertsScreen extends StatelessWidget {
  const AlertsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Alerts'),
      ),
      body: const Center(
        child: Text('TODO: Implement AlertsScreen'),
      ),
    );
  }
}
