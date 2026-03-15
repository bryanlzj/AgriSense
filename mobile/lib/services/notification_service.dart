import 'dart:async';
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
  static int _lastSeenAlertId = 0;
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
        // Notification tapped while app is open — no-op for now
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

    // Load last seen alert ID
    final prefs = await SharedPreferences.getInstance();
    _lastSeenAlertId = prefs.getInt('lastSeenAlertId') ?? 0;
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
      final droughtEnabled = prefs.getBool('droughtWarnings') ?? false;
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
  }

  /// Start polling for new alerts periodically.
  static void startPolling({Duration interval = const Duration(seconds: 30)}) {
    stopPolling();
    _pollTimer = Timer.periodic(interval, (_) => _checkForNewAlerts());
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
      if (token == null) return;

      final response = await AlertService.getAlerts(
        isRead: false,
        limit: 10,
      );

      for (final alert in response.alerts) {
        if (alert.id > _lastSeenAlertId) {
          await showAlertNotification(alert);
        }
      }

      // Update last seen ID
      if (response.alerts.isNotEmpty) {
        final maxId = response.alerts
            .map((a) => a.id)
            .reduce((a, b) => a > b ? a : b);
        if (maxId > _lastSeenAlertId) {
          _lastSeenAlertId = maxId;
          final prefs = await SharedPreferences.getInstance();
          await prefs.setInt('lastSeenAlertId', _lastSeenAlertId);
        }
      }
    } catch (_) {
      // Silently fail — polling should not crash the app
    }
  }
}
