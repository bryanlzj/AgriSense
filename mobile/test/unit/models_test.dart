import 'package:flutter_test/flutter_test.dart';
import 'package:fyp_prototype/models/user.dart';
import 'package:fyp_prototype/models/alert.dart';
import 'package:fyp_prototype/models/pest_detection.dart';
import 'package:fyp_prototype/models/chat_message.dart';

void main() {
  group('User Model', () {
    test('fromJson creates User correctly', () {
      final json = {
        'id': 1,
        'username': 'testuser',
        'full_name': 'Test User',
        'farm_location_name': 'Kuala Lumpur',
        'farm_location_lat': 3.1390,
        'farm_location_lng': 101.6869,
        'crop_type': 'rice',
        'is_active': true,
        'created_at': '2024-01-01T00:00:00Z',
      };

      final user = User.fromJson(json);

      expect(user.id, 1);
      expect(user.username, 'testuser');
      expect(user.fullName, 'Test User');
      expect(user.farmLocationName, 'Kuala Lumpur');
      expect(user.farmLocationLat, 3.1390);
      expect(user.farmLocationLng, 101.6869);
      expect(user.cropType, 'rice');
      expect(user.isActive, true);
    });

    test('toJson creates correct map', () {
      final user = User(
        id: 1,
        username: 'testuser',
        fullName: 'Test User',
        farmLocationName: 'Kuala Lumpur',
        farmLocationLat: 3.1390,
        farmLocationLng: 101.6869,
        cropType: 'rice',
        isActive: true,
        createdAt: DateTime.parse('2024-01-01T00:00:00Z'),
      );

      final json = user.toJson();

      expect(json['id'], 1);
      expect(json['username'], 'testuser');
      expect(json['full_name'], 'Test User');
      expect(json['farm_location_name'], 'Kuala Lumpur');
      expect(json['crop_type'], 'rice');
    });
  });

  group('Alert Model', () {
    test('fromJson creates Alert correctly', () {
      final json = {
        'id': 1,
        'type': 'weather',
        'severity': 'high',
        'title': 'Heavy Rain Warning',
        'message': 'Heavy rain expected in your area',
        'is_read': false,
        'created_at': '2024-01-01T10:00:00Z',
      };

      final alert = Alert.fromJson(json);

      expect(alert.id, 1);
      expect(alert.type, 'weather');
      expect(alert.severity, 'high');
      expect(alert.title, 'Heavy Rain Warning');
      expect(alert.isRead, false);
    });

    test('timeAgo returns correct string', () {
      final now = DateTime.now();

      // Just now
      final justNow = Alert(
        id: 1,
        type: 'weather',
        severity: 'high',
        title: 'Test',
        message: 'Test',
        isRead: false,
        createdAt: now,
      );
      expect(justNow.timeAgo, 'Just now');
    });

    test('severityDisplay capitalizes severity', () {
      final alert = Alert(
        id: 1,
        type: 'weather',
        severity: 'high',
        title: 'Test',
        message: 'Test',
        isRead: false,
      );
      expect(alert.severityDisplay, 'High');
    });

    test('icon returns correct emoji for type', () {
      final weatherAlert = Alert(
        id: 1,
        type: 'weather',
        severity: 'high',
        title: 'Test',
        message: 'Test',
        isRead: false,
      );
      expect(weatherAlert.icon, '🌤️');

      final pestAlert = Alert(
        id: 2,
        type: 'pest',
        severity: 'high',
        title: 'Test',
        message: 'Test',
        isRead: false,
      );
      expect(pestAlert.icon, '🐛');
    });
  });

  group('PestDetection Model', () {
    test('fromJson creates PestDetection correctly', () {
      final json = {
        'id': 1,
        'user_id': 1,
        'pest_type': 'Rice Stem Borer',
        'confidence_score': 0.85,
        'image_url': 'https://example.com/image.jpg',
        'recommendations': 'Apply pesticide',
        'detected_at': '2024-01-01T12:00:00Z',
      };

      final detection = PestDetection.fromJson(json);

      expect(detection.id, 1);
      expect(detection.pestType, 'Rice Stem Borer');
      expect(detection.confidenceScore, 0.85);
      expect(detection.imageUrl, 'https://example.com/image.jpg');
    });
  });

  group('EnhancedPestDetection Model', () {
    test('fromJson creates EnhancedPestDetection correctly', () {
      final json = {
        'detection_id': 1,
        'image_url': 'https://example.com/image.jpg',
        'status': 'detected',
        'confidence': 0.85,
        'confidence_percent': 85,
        'pest_name': 'Rice Stem Borer',
        'scientific_name': 'Scirpophaga incertulas',
        'description': 'A major pest of rice',
        'danger_level': 'high',
        'recommendations': ['Apply pesticide', 'Monitor field'],
        'can_retry': false,
        'retry_tip': null,
        'offer_report': false,
        'analysis_timestamp': '2024-01-01T12:00:00Z',
      };

      final detection = EnhancedPestDetection.fromJson(json);

      expect(detection.status, 'detected');
      expect(detection.isDetected, true);
      expect(detection.isPartial, false);
      expect(detection.isUnknown, false);
      expect(detection.pestName, 'Rice Stem Borer');
      expect(detection.confidencePercent, 85);
      expect(detection.recommendations, isNotNull);
      expect(detection.recommendations!.length, 2);
    });

    test('status helpers work correctly', () {
      // Detected
      final detected = EnhancedPestDetection.fromJson({
        'status': 'detected',
        'image_url': '',
        'confidence': 0.8,
        'confidence_percent': 80,
        'can_retry': false,
        'offer_report': false,
        'analysis_timestamp': '2024-01-01T12:00:00Z',
      });
      expect(detected.isDetected, true);
      expect(detected.isPartial, false);
      expect(detected.isUnknown, false);

      // Partial
      final partial = EnhancedPestDetection.fromJson({
        'status': 'partial',
        'image_url': '',
        'confidence': 0.6,
        'confidence_percent': 60,
        'can_retry': true,
        'offer_report': false,
        'analysis_timestamp': '2024-01-01T12:00:00Z',
      });
      expect(partial.isDetected, false);
      expect(partial.isPartial, true);
      expect(partial.isUnknown, false);

      // Unknown
      final unknown = EnhancedPestDetection.fromJson({
        'status': 'unknown',
        'image_url': '',
        'confidence': 0.3,
        'confidence_percent': 30,
        'can_retry': true,
        'offer_report': true,
        'analysis_timestamp': '2024-01-01T12:00:00Z',
      });
      expect(unknown.isDetected, false);
      expect(unknown.isPartial, false);
      expect(unknown.isUnknown, true);
    });
  });

  group('ChatMessage Model', () {
    test('ChatResponse fromJson creates correctly', () {
      final json = {
        'message': 'Hello! How can I help you?',
        'session_id': 'abc123',
        'context_used': {
          'crop_type': 'rice',
          'location': 'Kuala Lumpur',
          'weather_available': true,
          'weather_summary': 'Sunny, 32°C',
        },
        'ai_available': true,
        'timestamp': '2024-01-01T12:00:00Z',
      };

      final response = ChatResponse.fromJson(json);

      expect(response.message, 'Hello! How can I help you?');
      expect(response.sessionId, 'abc123');
      expect(response.aiAvailable, true);
      expect(response.contextUsed.cropType, 'rice');
      expect(response.contextUsed.location, 'Kuala Lumpur');
      expect(response.contextUsed.weatherAvailable, true);
    });

    test('ChatStatus fromJson creates correctly', () {
      final json = {
        'status': 'online',
        'ai_service_available': true,
        'user_context': {
          'crop_type': 'rice',
          'location': 'Kuala Lumpur',
        },
        'capabilities': ['text', 'image'],
      };

      final status = ChatStatus.fromJson(json);

      expect(status.status, 'online');
      expect(status.aiServiceAvailable, true);
      expect(status.capabilities, contains('text'));
      expect(status.capabilities, contains('image'));
    });
  });
}
