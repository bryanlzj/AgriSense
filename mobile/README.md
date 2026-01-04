# AgriSense Mobile App

Flutter mobile application for AgriSense - Agricultural Intelligence System.

## 📱 Features

- **Authentication**: User registration and login
- **Dashboard**: Overview of farm data and alerts
- **Sensor Data**: View and add sensor readings (temperature, humidity, soil moisture, rainfall)
- **Pest Detection**: Upload images and detect pests using AI
- **Weather Forecast**: 5-day weather forecast with agricultural recommendations
- **Alerts**: Real-time notifications for weather, pests, and sensor anomalies

## 🚀 Getting Started

### Prerequisites

- Flutter SDK (3.0.0 or higher)
- Dart SDK (3.0.0 or higher)
- Android Studio / Xcode
- Backend API running at `http://localhost:8000`

### Installation

1. **Install dependencies:**
   ```bash
   cd mobile
   flutter pub get
   ```

2. **Run on Android emulator:**
   ```bash
   flutter run
   ```

3. **Run on iOS simulator (Mac only):**
   ```bash
   flutter run
   ```

4. **Build APK (Android):**
   ```bash
   flutter build apk --release
   ```

5. **Build IPA (iOS, Mac only):**
   ```bash
   flutter build ios --release
   ```

## 📂 Project Structure

```
mobile/
├── lib/
│   ├── main.dart                      # App entry point
│   ├── screens/                       # UI screens
│   │   ├── auth/                      # Login, Register
│   │   ├── dashboard/                 # Home dashboard
│   │   ├── sensor/                    # Sensor data screens
│   │   ├── pest/                      # Pest detection screens
│   │   ├── weather/                   # Weather screens
│   │   └── alerts/                    # Alerts screens
│   ├── services/                      # API services
│   │   ├── auth_service.dart          # Authentication API
│   │   ├── sensor_service.dart        # Sensor data API
│   │   ├── pest_service.dart          # Pest detection API
│   │   ├── weather_service.dart       # Weather API
│   │   └── alert_service.dart         # Alert API
│   ├── models/                        # Data models
│   │   ├── user.dart
│   │   ├── sensor_reading.dart
│   │   ├── pest_detection.dart
│   │   ├── weather.dart
│   │   └── alert.dart
│   ├── widgets/                       # Reusable widgets
│   └── utils/                         # Utilities
│       ├── constants.dart             # App constants
│       └── storage.dart               # Local storage (JWT token)
├── android/                           # Android-specific files
├── ios/                               # iOS-specific files
├── test/                              # Unit tests
├── assets/                            # Images, fonts, etc.
└── pubspec.yaml                       # Dependencies
```

## 🔧 Configuration

### Backend API URL

Update the API base URL in `lib/utils/constants.dart`:

```dart
// For Android emulator
const String API_BASE_URL = 'http://10.0.2.2:8000/api/v1';

// For iOS simulator
const String API_BASE_URL = 'http://localhost:8000/api/v1';

// For physical device (replace with your computer's IP)
const String API_BASE_URL = 'http://192.168.1.100:8000/api/v1';
```

### Permissions

**Android** (`android/app/src/main/AndroidManifest.xml`):
- Camera permission (for pest detection)
- Internet permission (for API calls)
- Location permission (optional, for weather)

**iOS** (`ios/Runner/Info.plist`):
- Camera usage description
- Photo library usage description
- Location usage description (optional)

## 📦 Dependencies

Key packages used:
- `http` - HTTP requests to backend API
- `provider` - State management
- `shared_preferences` - Local storage for JWT token
- `image_picker` - Camera and gallery access
- `fl_chart` - Charts and graphs
- `intl` - Date formatting

## 🧪 Testing

Run unit tests:
```bash
flutter test
```

Run integration tests:
```bash
flutter test integration_test
```

## 📖 API Documentation

Backend API documentation: `http://localhost:8000/docs`

See `../backend/API_DOCUMENTATION.md` for complete API reference.

## 👥 Team

- **Member 3**: Flutter Developer (Mobile App)

## 📝 Tasks

See `.references/tasks/agrisense-tasks.md` for Phase 2 tasks (Mobile App Development).

## 🐛 Troubleshooting

### Common Issues

**1. Backend connection failed:**
- Ensure backend is running: `cd ../backend && python run.py`
- Check API URL in `lib/utils/constants.dart`
- For Android emulator, use `10.0.2.2` instead of `localhost`

**2. Camera not working:**
- Check permissions in AndroidManifest.xml / Info.plist
- Test on physical device (emulator camera is limited)

**3. Build failed:**
- Run `flutter clean`
- Run `flutter pub get`
- Restart IDE

**4. Hot reload not working:**
- Press `r` in terminal to hot reload
- Press `R` to hot restart
- Restart the app

## 📚 Resources

- [Flutter Documentation](https://docs.flutter.dev/)
- [Dart Documentation](https://dart.dev/guides)
- [Flutter Cookbook](https://docs.flutter.dev/cookbook)
- [Backend API Docs](../backend/API_DOCUMENTATION.md)

## 📄 License

This project is part of a university capstone project.
