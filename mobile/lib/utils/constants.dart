/// App-wide constants
library;

// ============================================================================
// API Configuration
// ============================================================================

/// Backend API base URL
/// 
/// IMPORTANT: Change this based on your environment:
/// 
/// - Android Emulator: Use 10.0.2.2 (emulator's special alias for host machine)
/// - iOS Simulator: Use localhost
/// - Physical Device: Use your computer's IP address (e.g., 192.168.1.100)
const String API_BASE_URL = 'http://10.0.2.2:8000/api/v1';

// Alternative URLs (uncomment the one you need):
// const String API_BASE_URL = 'http://localhost:8000/api/v1'; // iOS Simulator
// const String API_BASE_URL = 'http://192.168.1.100:8000/api/v1'; // Physical Device

/// API endpoints
class ApiEndpoints {
  // Authentication
  static const String register = '$API_BASE_URL/auth/register';
  static const String login = '$API_BASE_URL/auth/login';
  static const String me = '$API_BASE_URL/auth/me';

  // Sensor Data
  static const String sensors = '$API_BASE_URL/sensor';
  static const String sensorStats = '$API_BASE_URL/sensor/stats/summary';

  // Pest Detection
  static const String pestUpload = '$API_BASE_URL/pest/upload';
  static const String pestDetect = '$API_BASE_URL/pest/detect';
  static const String pests = '$API_BASE_URL/pest';
  static const String pestStats = '$API_BASE_URL/pest/stats/summary';

  // Weather
  static const String weatherCurrent = '$API_BASE_URL/weather/current';
  static const String weatherForecast = '$API_BASE_URL/weather/forecast';
  static const String weatherSummary = '$API_BASE_URL/weather/summary';

  // Alerts
  static const String alerts = '$API_BASE_URL/alert';
  static const String alertStats = '$API_BASE_URL/alert/stats/summary';
  static const String alertCheck = '$API_BASE_URL/alert/check';
}

// ============================================================================
// Storage Keys (for SharedPreferences)
// ============================================================================

class StorageKeys {
  static const String accessToken = 'access_token';
  static const String userId = 'user_id';
  static const String username = 'username';
  static const String fullName = 'full_name';
}

// ============================================================================
// App Constants
// ============================================================================

class AppConstants {
  // App Info
  static const String appName = 'AgriSense';
  static const String appVersion = '1.0.0';

  // Timeouts
  static const Duration apiTimeout = Duration(seconds: 30);
  static const Duration imageUploadTimeout = Duration(minutes: 2);

  // Image Constraints
  static const int maxImageSizeMB = 5;
  static const int imageQuality = 85; // 0-100

  // Pagination
  static const int defaultPageSize = 20;

  // Refresh Intervals
  static const Duration weatherRefreshInterval = Duration(minutes: 10);
  static const Duration alertRefreshInterval = Duration(minutes: 5);
  static const Duration sensorRefreshInterval = Duration(minutes: 1);
}

// ============================================================================
// Alert Types & Severity
// ============================================================================

enum AlertType {
  weather,
  pest,
  sensor,
  system,
}

enum AlertSeverity {
  info,
  warning,
  critical,
}

// ============================================================================
// Pest Types
// ============================================================================

class PestTypes {
  static const String fallArmyworm = 'Fall Armyworm';
  static const String aphids = 'Aphids';
  static const String whitefly = 'Whitefly';
  static const String leafMiner = 'Leaf Miner';
  static const String unknown = 'Unknown';

  static List<String> get all => [
        fallArmyworm,
        aphids,
        whitefly,
        leafMiner,
        unknown,
      ];
}

// ============================================================================
// Sensor Types
// ============================================================================

class SensorTypes {
  static const String temperature = 'Temperature';
  static const String humidity = 'Humidity';
  static const String soilMoisture = 'Soil Moisture';
  static const String rainfall = 'Rainfall';
}

// ============================================================================
// Error Messages
// ============================================================================

class ErrorMessages {
  static const String networkError = 'Network error. Please check your connection.';
  static const String serverError = 'Server error. Please try again later.';
  static const String authenticationError = 'Authentication failed. Please login again.';
  static const String invalidCredentials = 'Invalid username or password.';
  static const String unknownError = 'An unknown error occurred.';
  static const String imageUploadError = 'Failed to upload image. Please try again.';
  static const String cameraPermissionDenied = 'Camera permission denied.';
  static const String locationPermissionDenied = 'Location permission denied.';
}

// ============================================================================
// Success Messages
// ============================================================================

class SuccessMessages {
  static const String loginSuccess = 'Login successful!';
  static const String registerSuccess = 'Registration successful!';
  static const String sensorAdded = 'Sensor reading added successfully!';
  static const String pestDetected = 'Pest detection completed!';
  static const String alertMarkedRead = 'Alert marked as read.';
}
