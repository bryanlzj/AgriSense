# Mobile App Structure

Complete Flutter project scaffold for AgriSense mobile application.

## 📂 Project Structure

```
mobile/
├── lib/                                    # Dart source code
│   ├── main.dart                          # App entry point (✅ Basic scaffold)
│   │
│   ├── screens/                           # UI Screens (9 screens)
│   │   ├── auth/
│   │   │   ├── login_screen.dart         # TODO: Login UI
│   │   │   └── register_screen.dart      # TODO: Registration UI
│   │   ├── dashboard/
│   │   │   └── dashboard_screen.dart     # TODO: Home dashboard
│   │   ├── sensor/
│   │   │   ├── sensor_list_screen.dart   # TODO: Sensor readings list
│   │   │   └── add_sensor_screen.dart    # TODO: Add sensor reading
│   │   ├── pest/
│   │   │   ├── pest_detection_screen.dart # TODO: Pest detection
│   │   │   └── pest_history_screen.dart   # TODO: Detection history
│   │   ├── weather/
│   │   │   └── weather_screen.dart        # TODO: Weather forecast
│   │   └── alerts/
│   │       └── alerts_screen.dart         # TODO: Alerts list
│   │
│   ├── services/                          # API Services (5 services)
│   │   ├── auth_service.dart             # TODO: Auth API calls
│   │   ├── sensor_service.dart           # TODO: Sensor API calls
│   │   ├── pest_service.dart             # TODO: Pest API calls
│   │   ├── weather_service.dart          # TODO: Weather API calls
│   │   └── alert_service.dart            # TODO: Alert API calls
│   │
│   ├── models/                            # Data Models (5 models)
│   │   ├── user.dart                     # ✅ User model
│   │   ├── sensor_reading.dart           # ✅ Sensor reading model
│   │   ├── pest_detection.dart           # ✅ Pest detection model
│   │   ├── weather.dart                  # ✅ Weather model
│   │   └── alert.dart                    # ✅ Alert model
│   │
│   ├── widgets/                           # Reusable Widgets
│   │   └── README.md                     # TODO: Create custom widgets
│   │
│   └── utils/                             # Utilities
│       ├── constants.dart                # ✅ App constants & API endpoints
│       └── storage.dart                  # ✅ Local storage (JWT token)
│
├── android/                               # Android-specific files
│   └── app/src/main/
│       └── AndroidManifest.xml           # ✅ Permissions configured
│
├── ios/                                   # iOS-specific files
│   └── Runner/
│       └── Info.plist                    # ✅ Permissions configured
│
├── test/                                  # Unit tests
│   └── widget_test.dart                  # ✅ Basic test
│
├── assets/                                # Assets
│   └── images/
│       └── README.md                     # TODO: Add images
│
├── pubspec.yaml                          # ✅ Dependencies configured
├── README.md                             # ✅ Complete setup guide
├── .gitignore                            # ✅ Git ignore rules
└── STRUCTURE.md                          # This file
```

## ✅ What's Already Done

### **1. Project Structure** ✅
- Complete folder structure created
- All necessary directories in place

### **2. Configuration Files** ✅
- `pubspec.yaml` - All dependencies configured
- `AndroidManifest.xml` - Camera & internet permissions
- `Info.plist` - Camera & photo library permissions
- `.gitignore` - Proper ignore rules

### **3. Utilities** ✅
- `constants.dart` - API endpoints, error messages, app constants
- `storage.dart` - JWT token storage with SharedPreferences

### **4. Data Models** ✅
- `user.dart` - User model with JSON serialization
- `sensor_reading.dart` - Sensor reading model
- `pest_detection.dart` - Pest detection model
- `weather.dart` - Weather & forecast models
- `alert.dart` - Alert model

### **5. Main App** ✅
- `main.dart` - Basic app structure with placeholder screen
- Material Design theme configured
- Provider setup ready

### **6. Documentation** ✅
- `README.md` - Complete setup and usage guide
- `STRUCTURE.md` - This file
- Inline TODO comments in all files

## 🚧 What Member 3 Needs to Implement

### **Phase 2.1: Setup** (Week 1)
- [x] Create Flutter project structure ✅ DONE
- [x] Configure dependencies ✅ DONE
- [x] Set up utilities ✅ DONE
- [ ] Run `flutter pub get` to install dependencies
- [ ] Test app runs on emulator

### **Phase 2.2: Authentication** (Week 2-3)
- [ ] Implement `LoginScreen` UI
- [ ] Implement `RegisterScreen` UI
- [ ] Implement `AuthService` API calls
- [ ] Test authentication flow

### **Phase 2.3: Dashboard** (Week 4)
- [ ] Implement `DashboardScreen` UI
- [ ] Create overview cards
- [ ] Add navigation

### **Phase 2.4: Sensor Data** (Week 5)
- [ ] Implement `SensorListScreen` UI
- [ ] Implement `AddSensorScreen` UI
- [ ] Implement `SensorService` API calls
- [ ] Test sensor CRUD operations

### **Phase 2.5: Pest Detection** (Week 6-7)
- [ ] Implement `PestDetectionScreen` UI
- [ ] Implement `PestHistoryScreen` UI
- [ ] Implement `PestService` API calls
- [ ] Integrate camera/gallery
- [ ] Test image upload and detection

### **Phase 2.6: Weather** (Week 8)
- [ ] Implement `WeatherScreen` UI
- [ ] Implement `WeatherService` API calls
- [ ] Display forecast cards
- [ ] Test weather data display

### **Phase 2.7: Alerts** (Week 9)
- [ ] Implement `AlertsScreen` UI
- [ ] Implement `AlertService` API calls
- [ ] Add filtering
- [ ] Test alert management

### **Phase 2.8: Polish** (Week 10-12)
- [ ] Create reusable widgets
- [ ] Add loading states
- [ ] Add error handling
- [ ] Improve UI/UX
- [ ] Add animations
- [ ] Test on physical device

## 📦 Dependencies Configured

All dependencies are already in `pubspec.yaml`:

- `http` - HTTP requests to backend
- `provider` - State management
- `shared_preferences` - Local storage
- `image_picker` - Camera/gallery access
- `fl_chart` - Charts and graphs
- `intl` - Date formatting
- `flutter_spinkit` - Loading indicators

## 🔧 First Steps for Member 3

1. **Install dependencies:**
   ```bash
   cd mobile
   flutter pub get
   ```

2. **Run the app:**
   ```bash
   flutter run
   ```
   
   You should see a placeholder screen with "AgriSense Mobile"

3. **Start implementing:**
   - Begin with `LoginScreen` (Week 2)
   - Follow the TODO comments in each file
   - Test each feature before moving to next

4. **API Integration:**
   - All API endpoints are in `lib/utils/constants.dart`
   - Backend must be running at `http://localhost:8000`
   - For Android emulator, use `http://10.0.2.2:8000`

## 📚 Resources

- **Backend API:** `http://localhost:8000/docs` (Swagger UI)
- **API Documentation:** `../backend/API_DOCUMENTATION.md`
- **Task List:** `../.references/tasks/agrisense-tasks.md`
- **Flutter Docs:** https://docs.flutter.dev/

## 🎯 Key Points

1. **No actual implementation** - This is a scaffold/template
2. **All files have TODO comments** - Clear guidance on what to implement
3. **Models are complete** - JSON serialization ready
4. **Utilities are complete** - Storage and constants ready
5. **Permissions configured** - Camera and internet ready
6. **Dependencies configured** - Just run `flutter pub get`

## 💡 Tips for Member 3

1. **Start simple** - Build basic UI first, then add features
2. **Test frequently** - Run on emulator after each feature
3. **Use hot reload** - Press `r` in terminal for fast refresh
4. **Follow the models** - Use the provided data models for consistency
5. **Check backend docs** - Swagger UI shows exact API format
6. **Ask questions** - If stuck, check with team

## 🐛 Common Issues

**Issue:** `flutter: command not found`  
**Solution:** Install Flutter SDK from https://docs.flutter.dev/get-started/install

**Issue:** Dependencies not found  
**Solution:** Run `flutter pub get`

**Issue:** Backend connection failed  
**Solution:** 
- Ensure backend is running
- For Android emulator, use `10.0.2.2` instead of `localhost`
- Check `lib/utils/constants.dart` for API URL

**Issue:** Camera not working  
**Solution:** Test on physical device (emulator camera is limited)

---

**This scaffold provides a complete foundation for Member 3 to start building the AgriSense mobile app!** 🚀
