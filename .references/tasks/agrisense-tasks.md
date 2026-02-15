# AgriSense - Task List

**Generated from PRD:** `.references/prd/agrisense-prd-v2.md`
**Project:** AgriSense - IoT-Driven Early Warning System for Weather and Pest Risk Management
**Timeline:** 14 Weeks
**Last Updated:** February 2026

**DUAL CORE FEATURES (Equal Priority):**
1. **Weather Early Warning System** - Real-time forecasts, weather alerts
2. **Pest Risk Management System** - AI pest detection, weather-pest correlations, risk predictions

---

## Progress Overview

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 0: Setup & Planning | ✅ COMPLETE | Git, folder structure, backend env |
| Phase 1: Backend Foundation | ✅ COMPLETE | Auth, Sensor, Pest, Weather, Alerts, Dashboard, Chat, Sector |
| Phase 2: Mobile App (Flutter) | ✅ COMPLETE | All screens, API integration, Provider state management |
| Phase 3: Testing | ✅ COMPLETE | 139 backend tests, 29 mobile tests |
| Phase 4: Deployment | ✅ COMPLETE | CI/CD, PostgreSQL, Docker |
| Phase 5: AI Integration | ✅ COMPLETE | OpenRouter chatbot, pest detection |
| Phase 6: Polish | ✅ COMPLETE | Provider auth state, error handling, logout |
| **Phase 7: Enhancements** | 🔧 IN PROGRESS | Edit Profile, Weather Enhancements |

---

## Current Test Coverage

| Type | Count | Coverage | Status |
|------|-------|----------|--------|
| Backend (pytest) | 139 | 77% overall, 92-100% routers | ✅ All passing |
| Mobile (flutter test) | 29 | - | ✅ All passing |

**Backend Test Breakdown:**
| Test File | Tests | Description |
|-----------|-------|-------------|
| test_auth.py | 15 | Authentication endpoints |
| test_sensor.py | 13 | Sensor data CRUD |
| test_pest.py | 28 | Pest detection & reports |
| test_weather.py | 17 | Weather API endpoints |
| test_alert.py | 15 | Alert system |
| test_chat.py | 16 | Chatbot functionality |
| test_dashboard.py | 14 | Dashboard endpoints |
| test_sector.py | 21 | Sector CRUD |

---

## ✅ COMPLETE - Phase 0: Setup & Planning

- [x] 0.1: Project Initialization (Git, folder structure, README)
- [x] 0.2: Backend Environment Setup (FastAPI, SQLAlchemy, Alembic)
- [x] 0.3: Database Schema Implementation (User, SensorReading, PestDetection, Alert, Sector)
- [x] 0.4: Synthetic Data Generator (password utils, data simulator, seed script)
- [x] 0.5: API Router Structure (routers, CORS, health check)

---

## ✅ COMPLETE - Phase 1: Backend Foundation

### Task 1.1: Authentication System ✅
- [x] 1.1.1: Install authentication dependencies
- [x] 1.1.2: Create password hashing utilities
- [x] 1.1.3: Create JWT token utilities (30-day expiry)
- [x] 1.1.4: Create authentication dependency
- [x] 1.1.5: Create Pydantic schemas (UserRegister, UserLogin, Token)
- [x] 1.1.6: Implement registration endpoint (POST /auth/register)
- [x] 1.1.7: Implement login endpoint (POST /auth/login)
- [x] 1.1.8: Implement get current user endpoint (GET /auth/me)

### Task 1.2: Sensor Data Management ✅
- [x] 1.2.1: Create sensor data schemas
- [x] 1.2.2: Implement create sensor data endpoint
- [x] 1.2.3: Implement get sensor data endpoints (list, get by ID)
- [x] 1.2.4: Implement update and delete endpoints
- [x] 1.2.5: Implement sensor statistics endpoint

### Task 1.3: Pest Detection ✅
- [x] 1.3.1: Set up image storage (uploads folder, file_storage.py)
- [x] 1.3.2: Implement image validation (type, size, dimensions)
- [x] 1.3.3: Implement pest detection endpoints (upload, detect, list, delete)
- [x] 1.3.4: Create pest detection schemas
- [x] 1.3.5: Implement detection history endpoint
- [x] 1.3.6: Implement detection details endpoint
- [x] 1.3.7: Integrate AI service for pest recommendations

### Task 1.4: Weather System ✅
- [x] 1.4.1: Set up Open-Meteo API integration (free, no key required)
- [x] 1.4.2: Create weather service (current, forecast)
- [x] 1.4.3: Implement weather caching (30 min)
- [x] 1.4.4: Create weather schemas
- [x] 1.4.5: Implement weather endpoints (current, forecast, summary)

### Task 1.5: Alert System ✅
- [x] 1.5.1: Create alert generation service
- [x] 1.5.2: Implement weather-based alerts
- [x] 1.5.3: Implement pest risk alerts
- [x] 1.5.4: Create alert management system
- [x] 1.5.5: Create alert schemas
- [x] 1.5.6: Implement alert endpoints (list, mark read, delete)

### Task 1.6: Dashboard ✅
- [x] 1.6.1: Implement GET /dashboard endpoint
- [x] 1.6.2: Aggregate weather summary, alert count, recent alerts
- [x] 1.6.3: Include recent detections and pest risk status

### Task 1.7: AI Chatbot ✅
- [x] 1.7.1: Create OpenRouter API client
- [x] 1.7.2: Create chat service with context injection
- [x] 1.7.3: Implement POST /chat/message endpoint
- [x] 1.7.4: Implement chat status endpoint

### Task 1.8: Farm Sectors ✅
- [x] 1.8.1: Create Sector model
- [x] 1.8.2: Create sector schemas
- [x] 1.8.3: Implement sector CRUD endpoints
- [x] 1.8.4: Implement sector statistics endpoint

---

## ✅ COMPLETE - Phase 2: Mobile App (Flutter)

### Task 2.1: Project Setup ✅
- [x] 2.1.1: Flutter project structure
- [x] 2.1.2: Install dependencies (http, provider, shared_preferences, image_picker)
- [x] 2.1.3: Configure API base URL
- [x] 2.1.4: Set up navigation

### Task 2.2: Authentication Screens ✅
- [x] 2.2.1: Login page with validation
- [x] 2.2.2: Sign up page with farm details
- [x] 2.2.3: JWT token storage (SharedPreferences)
- [x] 2.2.4: Auto-login check

### Task 2.3: Dashboard ✅
- [x] 2.3.1: Weather card (current conditions)
- [x] 2.3.2: Alert banner (unread count)
- [x] 2.3.3: Quick actions (Detect Pest, Chat)
- [x] 2.3.4: Pull-to-refresh

### Task 2.4: Weather Screen ✅
- [x] 2.4.1: Current weather display
- [x] 2.4.2: 5-day forecast list

### Task 2.5: Pest Detection ✅
- [x] 2.5.1: Image picker (camera/gallery)
- [x] 2.5.2: Detection results display
- [x] 2.5.3: AI recommendations display
- [x] 2.5.4: Confidence bar, danger level badge

### Task 2.6: Alerts Screen ✅
- [x] 2.6.1: Alerts list with severity badges
- [x] 2.6.2: Mark as read functionality
- [x] 2.6.3: Alert detail view

### Task 2.7: Chat Screen ✅
- [x] 2.7.1: Chat message list
- [x] 2.7.2: Text input + send button
- [x] 2.7.3: Image upload in chat
- [x] 2.7.4: AI responses display

### Task 2.8: Settings & Profile ✅
- [x] 2.8.1: Display user profile info
- [x] 2.8.2: Logout button with confirmation
- [x] 2.8.3: Settings navigation

### Task 2.9: Sectors Screen ✅
- [x] 2.9.1: Sector list view
- [x] 2.9.2: Add/Edit sector functionality
- [x] 2.9.3: Delete sector with confirmation
- [x] 2.9.4: Sector statistics display

---

## ✅ COMPLETE - Phase 3: Testing

### Task 3.1: Backend Tests ✅
- [x] 3.1.1: Set up pytest with fixtures (conftest.py)
- [x] 3.1.2: Authentication tests (15 tests)
- [x] 3.1.3: Sensor tests (13 tests)
- [x] 3.1.4: Pest detection tests (28 tests)
- [x] 3.1.5: Weather tests (17 tests)
- [x] 3.1.6: Alert tests (15 tests)
- [x] 3.1.7: Chat tests (16 tests)
- [x] 3.1.8: Dashboard tests (14 tests)
- [x] 3.1.9: Sector tests (21 tests)

### Task 3.2: Mobile Tests ✅
- [x] 3.2.1: Auth provider unit tests
- [x] 3.2.2: Model unit tests (User, Alert, PestDetection, Chat)
- [x] 3.2.3: Error handler unit tests
- [x] 3.2.4: Login page widget tests

---

## ✅ COMPLETE - Phase 4: Deployment

### Task 4.1: Backend Deployment ✅
- [x] 4.1.1: Docker configuration
- [x] 4.1.2: PostgreSQL database setup
- [x] 4.1.3: CI/CD via GitHub Actions
- [x] 4.1.4: Deploy to Oracle Cloud (agrisense.bryanlzj.work)
- [x] 4.1.5: SSL/HTTPS configuration

---

## ✅ COMPLETE - Phase 5: AI Integration

### Task 5.1: OpenRouter Integration ✅
- [x] 5.1.1: AI service setup
- [x] 5.1.2: Pest detection recommendations
- [x] 5.1.3: Chatbot responses with context
- [x] 5.1.4: Weather-based advice

---

## ✅ COMPLETE - Phase 6: Polish

### Task 6.1: State Management ✅
- [x] 6.1.1: AuthProvider with ChangeNotifier
- [x] 6.1.2: Global auth state (login, logout, register)
- [x] 6.1.3: Auto-login on app startup
- [x] 6.1.4: Session expiration handling

### Task 6.2: Error Handling ✅
- [x] 6.2.1: ErrorHandler utility class
- [x] 6.2.2: Consistent snackbar messages
- [x] 6.2.3: Network error handling
- [x] 6.2.4: 401 auto-redirect to login

### Task 6.3: UI Polish ✅
- [x] 6.3.1: Settings page with real user data
- [x] 6.3.2: Logout with confirmation dialog

---

## 🔧 IN PROGRESS - Phase 7: Enhancements

### Priority 1: Edit Profile
- [ ] 7.1.1: Backend - Add PUT /api/v1/auth/me endpoint
- [ ] 7.1.2: Mobile - Create Edit Profile page
- [ ] 7.1.3: Fields to edit: full_name, farm_location_name, crop_type
- [ ] 7.1.4: Add tests for profile update

### Priority 2: Weather Enhancements (User Requested)

> **Note:** These features are marked "Out of Scope" in PRD but user indicates they are needed.

| Feature | Backend Changes | Mobile Changes |
|---------|-----------------|----------------|
| **Historical Weather Data** | Add `/weather/historical` endpoint | Add historical tab/view to weather page |
| **Weather by Farm Sector** | Add lat/lng to Sector model | Allow sector selection in weather page |
| **Sector Selection in Weather** | Support location parameter | Dropdown to select sector for weather |

**Implementation Tasks:**
- [ ] 7.2.1: Add latitude/longitude columns to Sector model
- [ ] 7.2.2: Create Alembic migration for sector coordinates
- [ ] 7.2.3: Update sector schemas and endpoints
- [ ] 7.2.4: Add /weather/historical endpoint
- [ ] 7.2.5: Mobile - Add sector selector to weather page
- [ ] 7.2.6: Mobile - Add historical weather view
- [ ] 7.2.7: Add tests for new endpoints

---

## Task Summary

| Category | Tasks | Status |
|----------|-------|--------|
| Phase 0-1: Backend Foundation | 44 subtasks | ✅ Complete |
| Phase 2: Mobile (Flutter) | 28 subtasks | ✅ Complete |
| Phase 3: Testing | 13 subtasks | ✅ Complete |
| Phase 4: Deployment | 5 subtasks | ✅ Complete |
| Phase 5: AI Integration | 4 subtasks | ✅ Complete |
| Phase 6: Polish | 9 subtasks | ✅ Complete |
| **Phase 7: Enhancements** | 11 subtasks | 🔧 Pending |
| **TOTAL** | **114 subtasks** | ~90% Complete |

---

## API Endpoints Summary

### Auth
| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/api/v1/auth/login` | Login | ✅ |
| POST | `/api/v1/auth/register` | Register | ✅ |
| GET | `/api/v1/auth/me` | Get current user | ✅ |
| PUT | `/api/v1/auth/me` | Update profile | ❌ NEEDED |

### Weather
| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/v1/weather/current` | Current weather | ✅ |
| GET | `/api/v1/weather/forecast` | 5-day forecast | ✅ |
| GET | `/api/v1/weather/summary` | Current + forecast | ✅ |
| GET | `/api/v1/weather/historical` | Historical data | ❌ NEEDED |

### Other Endpoints (All Working)
| Endpoint | Description | Status |
|----------|-------------|--------|
| `/api/v1/dashboard` | Dashboard data | ✅ |
| `/api/v1/alert/` | Alerts CRUD | ✅ |
| `/api/v1/sector/` | Sectors CRUD | ✅ |
| `/api/v1/pest/` | Pest detection | ✅ |
| `/api/v1/chat/` | Chatbot | ✅ |

---

## Infrastructure

- **Backend URL:** `https://agrisense.bryanlzj.work`
- **Database (Adminer):** `https://db.bryanlzj.work`
- **Server Location:** Oracle Cloud at `/opt/agrisense`
- **Deployment:** CI/CD via GitHub Actions (`.github/workflows/deploy.yml`)
- **Database:** PostgreSQL running in Docker on server

---

## How to Run

### Backend
```bash
cd backend
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run.py
```

### Mobile
```bash
cd mobile
flutter pub get
flutter run
```

### Run Tests
```bash
# Backend tests (139 tests)
cd backend
python -m pytest -v

# Backend tests with coverage
python -m pytest --cov=backend --cov-report=html

# Mobile tests (29 tests)
cd mobile
flutter test
```

---

## Notes

- **Mobile Framework:** Flutter (not React Native as originally planned)
- **JWT Expiry:** 30 days
- **AI Model:** Using OpenRouter API for chatbot and pest recommendations
- **ML Models:** Using mock services (teammate's models pending)
- **Database:** PostgreSQL for production
- **No Push Notifications:** In-app alerts only

---

**End of Task List**
