# AgriSense Backend-Mobile Integration Plan

> **Created:** 2026-01-19
> **Purpose:** Track the integration between FastAPI backend and Flutter mobile app
> **Status:** In Review

---

## Table of Contents
- [1. Backend API Summary](#1-backend-api-summary)
- [2. Mobile App Summary](#2-mobile-app-summary)
- [3. Backend ↔ Mobile Mapping](#3-backend--mobile-mapping)
- [4. Schema Comparison](#4-schema-comparison)
- [5. Gap Analysis](#5-gap-analysis)
- [6. Integration Roadmap](#6-integration-roadmap)
- [7. Progress Tracker](#7-progress-tracker)

---

## 1. Backend API Summary

### 1.1 Authentication (`/api/v1/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register` | Register new user with farm profile | No |
| POST | `/login` | Login & get JWT token (30-day expiry) | No |
| GET | `/me` | Get current user info | Yes |

**Notes:**
- JWT token returned on login: `{ "access_token": "...", "token_type": "bearer" }`
- All authenticated requests need header: `Authorization: Bearer <token>`

### 1.2 Sensor Data (`/api/v1/sensor`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/` | Create sensor reading | Yes |
| GET | `/` | List sensor readings (paginated, filterable) | Yes |
| GET | `/{sensor_data_id}` | Get specific reading | Yes |
| PUT | `/{sensor_data_id}` | Update reading | Yes |
| DELETE | `/{sensor_data_id}` | Delete reading | Yes |
| GET | `/stats/summary` | Get aggregated statistics | Yes |

**Query Parameters:**
- Pagination: `skip`, `limit` (max 1000)
- Filters: `start_date`, `end_date`, `min_temperature`, `max_temperature`
- Stats: `days` (1-365, default 7)

### 1.3 Pest Detection (`/api/v1/pest`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/upload` | Upload image only | Yes |
| POST | `/detect` | Upload & detect pests | Yes |
| POST | `/detect/enhanced` | Enhanced detection with confidence tiers | Yes |
| GET | `/` | List pest detections | Yes |
| GET | `/{detection_id}` | Get specific detection | Yes |
| DELETE | `/{detection_id}` | Delete detection | Yes |
| GET | `/stats/summary` | Get pest statistics | Yes |
| GET | `/risk` | Get pest risk assessment | Yes |
| GET | `/risk/summary` | Get simplified risk summary | Yes |
| POST | `/report` | Submit manual pest report | Yes |
| GET | `/reports` | List manual reports | Yes |
| GET | `/reports/{report_id}` | Get specific report | Yes |

**Notes:**
- Currently using **MOCK ML** - returns random pest detection results
- Confidence tiers: ≥70% detected, 50-69% partial, <50% unknown
- Images stored in `backend/uploads/`

### 1.4 Weather (`/api/v1/weather`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/current` | Current weather conditions | Yes |
| GET | `/forecast` | 5-day forecast (3-hour intervals) | Yes |
| GET | `/summary` | Current + forecast + alerts + recommendations | Yes |
| GET | `/test` | Test API configuration | Yes |

**Query Parameters:**
- `latitude` (-90 to 90)
- `longitude` (-180 to 180)
- `location_name` (optional)

**Data Source:** Open-Meteo API (free, no key required)

### 1.5 Alerts (`/api/v1/alert`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | List alerts (filterable) | Yes |
| GET | `/{alert_id}` | Get specific alert | Yes |
| PUT | `/{alert_id}` | Update alert (mark read/acknowledged) | Yes |
| DELETE | `/{alert_id}` | Delete alert | Yes |
| PUT | `/bulk` | Bulk update multiple alerts | Yes |
| DELETE | `/bulk` | Bulk delete multiple alerts | Yes |
| GET | `/stats/summary` | Get alert statistics | Yes |
| POST | `/check` | Manually trigger alert checks | Yes |

**Filter Parameters:**
- `type`: weather, pest, system, environmental
- `severity`: low, medium, high, critical
- `is_read`, `is_acknowledged`: true/false

### 1.6 Chat/Chatbot (`/api/v1/chat`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/message` | Send message to AI chatbot | Yes |
| POST | `/image` | Send image for AI guidance | Yes |
| GET | `/status` | Check chatbot service status | Yes |

**Features:**
- Uses OpenRouter API for AI responses (or mock if not configured)
- Auto-injects context: crop type, location, weather
- Session support for conversation continuity

### 1.7 Dashboard (`/api/v1/dashboard`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Full dashboard data | Yes |
| GET | `/quick` | Minimal dashboard (fast loading) | Yes |

**Returns:**
- User profile summary
- Current weather
- Alert count + recent alerts
- Recent pest detections
- Pest risk status

---

## 2. Mobile App Summary

### 2.1 Pages/Screens

| Page | File | Status | Description |
|------|------|--------|-------------|
| Splash | `splash_page.dart` | ✅ Done | Logo display on startup |
| Login | `login_page.dart` | 🟡 UI Only | Email/password form with validation |
| Sign Up | `sign_up_page.dart` | 🟡 UI Only | Registration form |
| Forgot Password | `forgot_password_page.dart` | 🟡 Skeleton | Email input |
| OTP | `otp_page.dart` | 🟡 Skeleton | OTP verification |
| Reset Password | `reset_password_page.dart` | 🟡 Skeleton | New password form |
| Success | `success_page.dart` | 🟡 Skeleton | Generic success screen |
| Main | `main_page.dart` | ✅ Done | Tab navigation container |
| Home | `home_page.dart` | 🟡 Mock Data | Dashboard with greeting, weather, alerts |
| Weather | `weather_page.dart` | 🟡 Mock Data | Weather per sector |
| Pests | `pests_page.dart` | 🔴 Skeleton | Just an add button |
| Settings | `settings_page.dart` | ✅ Done | Settings menu |
| Farm Management | `farm_management_page.dart` | 🟡 Mock Service | CRUD for sectors |
| Chatbot | `chatbot_page.dart` | 🔴 Skeleton | Slide-up chat interface |
| Notifications | `notification_page.dart` | ✅ Done | Toggle preferences (SharedPreferences) |
| Import Dataset | `import_dataset_page.dart` | 🔴 Skeleton | Placeholder |
| Help & Support | `help_support_page.dart` | 🔴 Skeleton | Placeholder |
| About | `about_agrisense_page.dart` | 🔴 Skeleton | Placeholder |

### 2.2 Models

| Model | File | Has fromJson | Has toJson | Notes |
|-------|------|--------------|------------|-------|
| HomePageData | `home_page_data.dart` | ✅ Yes | ❌ No | Main dashboard model |
| WeatherData | `weather_data.dart` | ✅ Yes | ❌ No | Weather conditions |
| Alert | `alert.dart` | ✅ Yes | ❌ No | Alert notifications |
| RiskStatus | `risk_status.dart` | ✅ Yes | ❌ No | Risk assessment |
| Sector | `farm_sector.dart` | ❌ No | ❌ No | Farm sector (needs update) |

### 2.3 Services

| Service | File | Type | Notes |
|---------|------|------|-------|
| MockSectorService | `mock_sector_service.dart` | Mock | In-memory sector CRUD |

**Missing Services:**
- AuthService
- DashboardService
- WeatherService
- PestService
- AlertService
- ChatService

### 2.4 Dependencies (pubspec.yaml)

| Package | Purpose | Status |
|---------|---------|--------|
| flutter | Core framework | ✅ Present |
| google_fonts | Typography | ✅ Present |
| shared_preferences | Local storage | ✅ Present |
| cupertino_icons | iOS icons | ✅ Present |
| flutter_native_splash | Splash screen | ✅ Present |
| **http** | API calls | ❌ **MISSING** |
| **provider** | State management | ❌ **MISSING** |
| **image_picker** | Camera/gallery | ❌ **MISSING** |

---

## 3. Backend ↔ Mobile Mapping

| Mobile Feature | Mobile Status | Backend Endpoint | Integration Status |
|----------------|---------------|------------------|-------------------|
| Login | UI only | `POST /auth/login` | 🔴 Not Connected |
| Sign Up | UI only | `POST /auth/register` | 🔴 Not Connected + Schema Mismatch |
| Forgot Password | UI only | ❌ N/A | ❌ Backend Missing |
| OTP Verification | UI only | ❌ N/A | ❌ Backend Missing |
| Password Reset | UI only | ❌ N/A | ❌ Backend Missing |
| Home Dashboard | Mock data | `GET /dashboard/quick` | 🔴 Not Connected |
| Weather Display | Mock data | `GET /weather/summary` | 🔴 Not Connected |
| Farm Sectors | MockSectorService | ❌ N/A | ❌ Backend Missing |
| Pest Detection | Skeleton | `POST /pest/detect` | 🔴 Not Connected |
| Pest History | Not built | `GET /pest` | 🔴 Not Connected |
| Alerts List | Not built | `GET /alert` | 🔴 Not Connected |
| Chatbot | Skeleton | `POST /chat/message` | 🔴 Not Connected |
| Notification Prefs | SharedPreferences | ❌ N/A | ⚠️ Local Only |
| Profile View | Not built | `GET /auth/me` | 🔴 Not Connected |
| Profile Edit | Not built | ❌ N/A | ❌ Backend Missing |

---

## 4. Schema Comparison

### 4.1 User Registration

**Mobile Sign Up Form Fields:**
```dart
- name (full name)
- email
- password
- confirm password
```

**Backend `UserRegister` Schema:**
```python
username: str              # ⚠️ Mobile uses "email" - need to decide
password: str              # ✅ Match
full_name: str             # ✅ Match (mobile calls it "name")
farm_location_name: str    # ❌ Missing in mobile
farm_location_lat: float   # ❌ Missing in mobile (default: 3.1390)
farm_location_lng: float   # ❌ Missing in mobile (default: 101.6869)
crop_type: str             # ❌ Missing in mobile
```

**Crop Type Options:** `rice`, `vegetables`, `corn`, `oil_palm`, `rubber`

**Decision Needed:**
- [ ] Use `username` OR change backend to accept `email`?
- [ ] Add farm location picker to sign up form?
- [ ] Add crop type dropdown to sign up form?
- [ ] Make farm fields optional with defaults?

### 4.2 Dashboard Data

**Mobile `HomePageData` Model:**
```dart
class HomePageData {
  final String userName;
  final String location;
  final WeatherData weatherData;
  final List<Alert> activeAlerts;
  final RiskStatus riskStatus;
}
```

**Backend `GET /dashboard/quick` Response:**
```json
{
  "user": {
    "id": 1,
    "username": "...",
    "full_name": "...",
    "farm_location_name": "...",
    "crop_type": "..."
  },
  "weather": {
    "temperature": 30.0,
    "humidity": 65,
    "condition": "Sunny",
    "icon": "01d"
  },
  "alerts": {
    "unread_count": 3,
    "recent": [...]
  },
  "pest_risk": {
    "level": "Medium",
    "summary": "..."
  }
}
```

**Mapping Required:**
- `userName` ← `user.full_name`
- `location` ← `user.farm_location_name`
- `weatherData` ← `weather` (need to map icon codes)
- `activeAlerts` ← `alerts.recent`
- `riskStatus` ← `pest_risk`

### 4.3 Alert Model

**Mobile `Alert` Model:**
```dart
class Alert {
  final String title;
  final String message;
  final String timeAgo;      // e.g., "2h ago"
  final String severity;     // "High", "Medium", "Low"
}
```

**Backend `AlertResponse` Schema:**
```python
id: int
alert_type: str            # weather, pest, system, environmental
severity: str              # low, medium, high, critical
title: str
message: str
recommendations: str
is_read: bool
is_acknowledged: bool
created_at: datetime
```

**Mapping Required:**
- Need to add `id` to mobile model
- Need to calculate `timeAgo` from `created_at`
- `severity` casing: backend lowercase, mobile capitalized

### 4.4 Sector/Farm Model

**Mobile `Sector` Model:**
```dart
class Sector {
  String name;
  String location;
  String area;
  String crop;
  String planted;    // Date string
}
```

**Backend:** ❌ No Sector model exists

**Decision Needed:**
- [ ] Create `Sector` model in backend?
- [ ] Create `/api/v1/sectors` endpoints?
- [ ] Link sectors to users (one-to-many)?

---

## 5. Gap Analysis

### 5.1 Backend Gaps (Missing Features)

| Feature | Priority | Description | Effort |
|---------|----------|-------------|--------|
| Password Reset Flow | Medium | `/auth/forgot-password`, `/auth/verify-otp`, `/auth/reset-password` | Medium |
| Farm Sectors CRUD | High | `GET/POST/PUT/DELETE /sectors` | Medium |
| User Profile Update | Low | `PUT /auth/me` or `/users/profile` | Low |
| Notification Preferences API | Low | `GET/PUT /notifications/preferences` | Low |
| Email as username option | Low | Allow email in username field or add email field | Low |

### 5.2 Mobile Gaps (Missing Features)

| Feature | Priority | Description | Effort |
|---------|----------|-------------|--------|
| HTTP Package | Critical | Add `http` package for API calls | Low |
| API Base URL Config | Critical | Create constants file with base URL | Low |
| AuthService | Critical | Login, register, token storage | Medium |
| JWT Token Management | Critical | Store/retrieve/include in headers | Medium |
| DashboardService | High | Fetch home page data | Low |
| WeatherService | High | Fetch weather data | Low |
| AlertService | High | Fetch and manage alerts | Medium |
| PestService | High | Image upload + detection | Medium |
| SectorService | High | Replace MockSectorService | Medium |
| ChatService | Medium | Chatbot API calls | Medium |
| Provider Setup | High | Global state management | Medium |
| Error Handling | High | API errors, loading states | Medium |
| Image Picker | Medium | Camera/gallery for pest detection | Low |
| Model Updates | Medium | Add `id` fields, `fromJson`/`toJson` | Low |

### 5.3 Schema Mismatches

| Issue | Mobile | Backend | Resolution |
|-------|--------|---------|------------|
| Username vs Email | Uses `email` | Expects `username` | TBD |
| Missing Sign Up Fields | Only name/email/password | Needs farm location + crop type | Add fields to form |
| Sector Model | No backend equivalent | N/A | Create backend model |
| Alert timeAgo | String like "2h ago" | DateTime `created_at` | Calculate in mobile |
| Weather Icon | Emoji string | API icon code | Map codes to emojis |

---

## 6. Integration Roadmap

### Phase 1: Foundation (Critical Path)

**Goal:** Get login working end-to-end

1. Add required packages to mobile
2. Create API configuration (base URL, endpoints)
3. Create AuthService with login/register
4. Implement JWT token storage
5. Update login page to call API
6. Test login flow

### Phase 2: Sign Up & Dashboard

**Goal:** Complete auth flow and show real dashboard data

7. Decide on username vs email
8. Update sign up form (add farm location, crop type)
9. Create DashboardService
10. Update HomePageData model to match backend
11. Connect home page to API
12. Add loading states

### Phase 3: Weather & Alerts

**Goal:** Display real weather and alerts

13. Create WeatherService
14. Update weather page to use real data
15. Create AlertService
16. Build alerts list UI
17. Connect notifications to alerts

### Phase 4: Farm Sectors

**Goal:** Real sector management

18. Create Sector model in backend
19. Create sector endpoints in backend
20. Create SectorService in mobile
21. Update Sector model in mobile (add id, fromJson)
22. Replace MockSectorService usage

### Phase 5: Pest Detection & Chat

**Goal:** Complete feature set

23. Add image_picker package
24. Create PestService
25. Build pest detection UI (camera/gallery)
26. Create ChatService
27. Connect chatbot page

### Phase 6: Polish

**Goal:** Production ready

28. Add Provider state management
29. Implement proper error handling
30. Add refresh tokens (if needed)
31. Test all flows
32. Handle edge cases

---

## 7. Progress Tracker

### Phase 1: Foundation
- [ ] Add `http` package to pubspec.yaml
- [ ] Add `provider` package to pubspec.yaml
- [ ] Create `lib/utils/api_constants.dart` with base URL
- [ ] Create `lib/services/api_client.dart` (base HTTP client)
- [ ] Create `lib/services/auth_service.dart`
- [ ] Create `lib/utils/token_storage.dart` (SharedPreferences)
- [ ] Update `login_page.dart` to call AuthService
- [ ] Test login with backend

### Phase 2: Sign Up & Dashboard
- [ ] Decide: username vs email (update this doc)
- [ ] Update `sign_up_page.dart` form fields
- [ ] Update AuthService.register()
- [ ] Create `lib/services/dashboard_service.dart`
- [ ] Update `HomePageData` model to match backend response
- [ ] Update `home_page.dart` to fetch real data
- [ ] Add loading spinner to home page
- [ ] Test sign up → login → dashboard flow

### Phase 3: Weather & Alerts
- [ ] Create `lib/services/weather_service.dart`
- [ ] Update `WeatherData` model if needed
- [ ] Update `weather_page.dart` to fetch real data
- [ ] Create `lib/services/alert_service.dart`
- [ ] Update `Alert` model (add id, handle timestamps)
- [ ] Build alerts list in UI
- [ ] Test weather and alerts display

### Phase 4: Farm Sectors
- [ ] Create `Sector` model in backend (`backend/models/sector.py`)
- [ ] Create Alembic migration for sectors table
- [ ] Create `backend/schemas/sector.py`
- [ ] Create `backend/routers/sector.py` with CRUD endpoints
- [ ] Register sector router in `main.py`
- [ ] Create `lib/services/sector_service.dart` in mobile
- [ ] Update mobile `Sector` model (add id, fromJson, toJson)
- [ ] Update `farm_management_page.dart` to use SectorService
- [ ] Test sector CRUD operations

### Phase 5: Pest Detection & Chat
- [ ] Add `image_picker` package to pubspec.yaml
- [ ] Create `lib/services/pest_service.dart`
- [ ] Build pest detection UI (capture/upload image)
- [ ] Display detection results
- [ ] Create `lib/services/chat_service.dart`
- [ ] Update `chatbot_page.dart` to send/receive messages
- [ ] Test pest detection flow
- [ ] Test chatbot flow

### Phase 6: Polish
- [ ] Set up Provider for global auth state
- [ ] Create AuthProvider with login/logout
- [ ] Add error handling (try-catch, error messages)
- [ ] Add loading states to all pages
- [ ] Handle token expiration
- [ ] Test all user flows end-to-end
- [ ] Fix any bugs discovered

---

## Notes & Decisions

### Pending Decisions

| Decision | Options | Chosen | Date |
|----------|---------|--------|------|
| Username vs Email for login | A) Keep username, B) Change to email, C) Support both | TBD | - |
| Farm location in sign up | A) Required fields, B) Optional with defaults, C) Separate onboarding | TBD | - |
| State management | A) Provider, B) Riverpod, C) GetX | TBD | - |
| Sector backend model | A) Create new model, B) Use existing sensor readings per location | TBD | - |

### Meeting Notes

_Add notes from discussions here_

---

## Appendix

### A. API Base URLs

| Environment | URL |
|-------------|-----|
| Android Emulator | `http://10.0.2.2:8000` |
| iOS Simulator | `http://localhost:8000` |
| Physical Device | `http://<your-ip>:8000` |
| Production | TBD |

### B. Backend Test Credentials

```
Username: testuser
Password: testpass123
```

_(Create via `/auth/register` if not exists)_

### C. Useful Commands

**Backend:**
```bash
cd backend
python run.py                    # Start server
pytest                           # Run tests
alembic upgrade head             # Apply migrations
alembic revision --autogenerate -m "msg"  # Create migration
```

**Mobile:**
```bash
cd mobile
flutter pub get                  # Install packages
flutter run                      # Run app
flutter build apk --release      # Build APK
```

### D. API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
