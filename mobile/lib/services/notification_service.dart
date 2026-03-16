import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:fyp_prototype/models/alert.dart';
import 'package:fyp_prototype/services/alert_service.dart';
import 'package:fyp_prototype/utils/token_storage.dart';

/// Background notification tap handler (must be top-level function).
@pragma('vm:entry-point')
void _onBackgroundNotificationTap(NotificationResponse response) {
  // No-op: handled when app opens
}

/// Service for local push notifications and alert polling.
class NotificationService {
  static final FlutterLocalNotificationsPlugin _plugin =
      FlutterLocalNotificationsPlugin();

  static Timer? _pollTimer;
  static final Set<int> _notifiedAlertIds = {};
  static int _notificationIdCounter = 0;

  // Notification channel IDs
  static const String _criticalChannelId = 'agrisense_critical';
  static const String _alertChannelId = 'agrisense_alerts';

  /// Initialize the notification plugin and request permissions.
  static Future<void> initialize() async {
    const androidSettings = AndroidInitializationSettings('@mipmap/ic_launcher');
    const darwinSettings = DarwinInitializationSettings(
      requestAlertPermission: true,
      requestBadgePermission: true,
      requestSoundPermission: true,
    );

    const settings = InitializationSettings(
      android: androidSettings,
      iOS: darwinSettings,
      macOS: darwinSettings,
    );

    await _plugin.initialize(
      settings,
      onDidReceiveNotificationResponse: (NotificationResponse response) {
        // Notification tapped while app is open
      },
      onDidReceiveBackgroundNotificationResponse: _onBackgroundNotificationTap,
    );

    // Request permission on Android 13+
    await _plugin
        .resolvePlatformSpecificImplementation<
            AndroidFlutterLocalNotificationsPlugin>()
        ?.requestNotificationsPermission();

    // Create notification channels
    await _createChannels();

    // Load previously notified alert IDs
    final prefs = await SharedPreferences.getInstance();
    final savedIds = prefs.getStringList('notifiedAlertIds') ?? [];
    _notifiedAlertIds.addAll(savedIds.map((s) => int.tryParse(s) ?? 0));
  }

  /// Create Android notification channels.
  static Future<void> _createChannels() async {
    final androidPlugin = _plugin
        .resolvePlatformSpecificImplementation<
            AndroidFlutterLocalNotificationsPlugin>();

    await androidPlugin?.createNotificationChannel(
      const AndroidNotificationChannel(
        _criticalChannelId,
        'Critical Alerts',
        description: 'Urgent alerts requiring immediate attention',
        importance: Importance.high,
        playSound: true,
        enableVibration: true,
      ),
    );

    await androidPlugin?.createNotificationChannel(
      const AndroidNotificationChannel(
        _alertChannelId,
        'Alerts',
        description: 'General alert notifications',
        importance: Importance.defaultImportance,
        playSound: true,
      ),
    );
  }

  /// Show a notification for an alert.
  static Future<void> showAlertNotification(Alert alert) async {
    // Check user preferences
    final prefs = await SharedPreferences.getInstance();
    final enabled = prefs.getBool('pushNotificationsEnabled') ?? true;
    if (!enabled) return;

    // Check category-specific preferences
    final category = alert.category;
    if (category == 'weather') {
      final rainfallEnabled = prefs.getBool('rainfallWarnings') ?? true;
      if (!rainfallEnabled) return;
    } else if (category == 'pest') {
      final pestEnabled = prefs.getBool('pestDetection') ?? true;
      if (!pestEnabled) return;
    } else if (category == 'environmental') {
      final droughtEnabled = prefs.getBool('droughtWarnings') ?? true;
      if (!droughtEnabled) return;
    }

    // Pick channel based on severity
    final isCritical =
        alert.severity == 'critical' || alert.severity == 'high';
    final channelId = isCritical ? _criticalChannelId : _alertChannelId;
    final channelName = isCritical ? 'Critical Alerts' : 'Alerts';

    final androidDetails = AndroidNotificationDetails(
      channelId,
      channelName,
      channelDescription: isCritical
          ? 'Urgent alerts requiring immediate attention'
          : 'General alert notifications',
      importance: isCritical ? Importance.high : Importance.defaultImportance,
      priority: isCritical ? Priority.high : Priority.defaultPriority,
      ticker: alert.title,
    );

    const darwinDetails = DarwinNotificationDetails(
      presentAlert: true,
      presentBadge: true,
      presentSound: true,
    );

    final notificationDetails = NotificationDetails(
      android: androidDetails,
      iOS: darwinDetails,
    );

    _notificationIdCounter++;
    await _plugin.show(
      _notificationIdCounter,
      '${alert.icon} ${alert.title}',
      alert.message,
      notificationDetails,
      payload: 'alert_${alert.id}',
    );

    debugPrint('[NotificationService] Showed notification for alert ${alert.id}: ${alert.title}');
  }

  /// Start polling for new alerts periodically.
  static void startPolling({Duration interval = const Duration(seconds: 30)}) {
    stopPolling();
    // Run immediately on start, then every interval
    _checkForNewAlerts();
    _pollTimer = Timer.periodic(interval, (_) => _checkForNewAlerts());
    debugPrint('[NotificationService] Polling started (every ${interval.inSeconds}s)');
  }

  /// Stop polling.
  static void stopPolling() {
    _pollTimer?.cancel();
    _pollTimer = null;
  }

  /// Check for new alerts and show notifications.
  static Future<void> _checkForNewAlerts() async {
    try {
      final token = await TokenStorage.getToken();
      if (token == null) {
        debugPrint('[NotificationService] No token, skipping poll');
        return;
      }

      final response = await AlertService.getAlerts(
        isRead: false,
        limit: 20,
      );

      debugPrint('[NotificationService] Polled: ${response.alerts.length} unread alerts');

      int newCount = 0;
      for (final alert in response.alerts) {
        if (!_notifiedAlertIds.contains(alert.id)) {
          await showAlertNotification(alert);
          _notifiedAlertIds.add(alert.id);
          newCount++;
        }
      }

      // Persist notified IDs (keep only last 200 to avoid bloat)
      if (newCount > 0) {
        final idsToSave = _notifiedAlertIds.toList();
        if (idsToSave.length > 200) {
          idsToSave.sort();
          idsToSave.removeRange(0, idsToSave.length - 200);
          _notifiedAlertIds
            ..clear()
            ..addAll(idsToSave);
        }
        final prefs = await SharedPreferences.getInstance();
        await prefs.setStringList(
          'notifiedAlertIds',
          _notifiedAlertIds.map((id) => id.toString()).toList(),
        );
        debugPrint('[NotificationService] $newCount new notifications shown');
      }
    } catch (e) {
      debugPrint('[NotificationService] Poll error: $e');
    }
  }
}
