# AgriSense - Updated Task List (PRD v2)

**Generated from PRD:** `.references/prd/agrisense-prd-v2.md`
**Project:** AgriSense - IoT-Driven Early Warning System for Weather and Pest Risk Management
**Timeline:** 14 Weeks
**Last Updated:** January 2025

**DUAL CORE FEATURES (Equal Priority):**
1. **Weather Early Warning System** - Real-time forecasts, ML predictions, weather alerts
2. **Pest Risk Management System** - AI pest detection, weather-pest correlations, risk predictions

---

## Task Execution Rules

1. **Sequential Execution:** Tasks must be completed in order (top to bottom)
2. **One at a Time:** Only one subtask is worked on at a time
3. **Approval Required:** Wait for user approval before starting next subtask
4. **Atomic Tasks:** Each subtask is a complete, testable unit of work
5. **Mark Complete:** Update checkbox `[x]` after completion and review

---

## Progress Overview

| Phase | Status |
|-------|--------|
| Phase 0: Setup & Planning | ✅ COMPLETE |
| Phase 1: Backend Foundation | ✅ COMPLETE (Auth, Sensor, Pest, Weather, Alerts, Testing) |
| **Phase 1A: Infrastructure Setup** | 🔧 PENDING - **DO FIRST** |
| Phase 1B: Backend Modifications (PRD v2) | 🔧 PENDING |
| Phase 1C: New Backend Features (PRD v2) | 🆕 PENDING |
| Phase 2: Mobile App (React Native) | 🔄 PENDING (Fresh Start) |
| Phase 3: Testing & Deployment | ⏳ PENDING |

---

## ✅ DONE - Phase 0: Setup & Planning

> **Status:** All tasks completed successfully

- [x] 0.1: Project Initialization (Git, folder structure, README)
- [x] 0.2: Backend Environment Setup (FastAPI, SQLAlchemy, Alembic)
- [x] 0.3: Database Schema Implementation (User, SensorReading, PestDetection, Alert)
- [x] 0.4: Synthetic Data Generator (password utils, data simulator, seed script)
- [x] 0.5: API Router Structure (routers, CORS, health check)

---

## ✅ DONE - Phase 1: Backend Foundation

> **Status:** Core backend infrastructure complete

### Task 1.1: Authentication System - Models & Utils ✅
- [x] 1.1.1: Install authentication dependencies
- [x] 1.1.2: Create password hashing utilities
- [x] 1.1.3: Create JWT token utilities (30-day expiry)
- [x] 1.1.4: Create authentication dependency

### Task 1.2: Authentication System - API Endpoints ✅
- [x] 1.2.1: Create Pydantic schemas (UserRegister, UserLogin, Token)
- [x] 1.2.2: Implement registration endpoint (POST /auth/register)
- [x] 1.2.3: Implement login endpoint (POST /auth/login)
- [x] 1.2.4: Implement get current user endpoint (GET /auth/me)
- [x] 1.2.5: Test authentication flow

### Task 1.3: Sensor Data Management ✅
- [x] 1.3.1: Create sensor data schemas
- [x] 1.3.2: Implement create sensor data endpoint
- [x] 1.3.3: Implement get sensor data endpoints (list, get by ID)
- [x] 1.3.4: Implement update and delete endpoints
- [x] 1.3.5: Implement sensor statistics endpoint

### Task 1.4: Pest Detection - Image Upload ✅
- [x] 1.4.1: Set up image storage (uploads folder, file_storage.py)
- [x] 1.4.2: Implement image validation (type, size, dimensions)
- [x] 1.4.3: Implement pest detection endpoints (upload, detect, list, delete)

### Task 1.5: Pest Detection - Mock ML Service ✅
- [x] 1.5.1: Create mock ML service (random predictions)
- [x] 1.5.2: Define pest types and recommendations (10 Malaysian pests)
- [x] 1.5.3: Integrate mock service with upload endpoint

### Task 1.6: Pest Detection - History & Details ✅
- [x] 1.6.1: Create pest detection schemas
- [x] 1.6.2: Implement detection history endpoint
- [x] 1.6.3: Implement detection details endpoint
- [x] 1.6.4: Test pest detection flow

### Task 1.7: Weather Early Warning System ✅
- [x] 1.7.1: Set up OpenWeatherMap API
- [x] 1.7.2: Create weather service (current, forecast)
- [x] 1.7.3: Implement weather caching (30 min)
- [x] 1.7.4: Create weather schemas
- [x] 1.7.5: Implement weather endpoints
- [x] 1.7.6: Test weather endpoints

### Task 1.8: Alert System ✅
- [x] 1.8.1: Create alert generation service
- [x] 1.8.2: Implement weather-based alerts
- [x] 1.8.3: Implement pest risk alerts
- [x] 1.8.4: Create alert management system
- [x] 1.8.5: Create alert schemas
- [x] 1.8.6: Implement alert endpoints

### Task 1.10: Backend Testing & Documentation ✅
- [x] 1.10.1: Set up pytest
- [x] 1.10.2: Write authentication tests
- [x] 1.10.3: Write API endpoint tests
- [x] 1.10.4: Configure Swagger documentation
- [x] 1.10.5: Create API documentation

---

## 🔧 MODIFY - Phase 1A: Infrastructure & Database Setup

> **Goal:** Fix Docker Compose, environment files, and database initialization to match PRD v2
> **Run First:** This phase should be completed BEFORE any code changes

### Task 1A.1: Fix Docker Compose Configuration
**Files:** `docker-compose.yml` (root level)

- [ ] 1A.1.1: Fix port configuration
  - Change backend port from 5000 to 8000 (match CLAUDE.md docs)
  - Update healthcheck URL port

- [ ] 1A.1.2: Update environment variables
  - Change `ACCESS_TOKEN_EXPIRE_DAYS: 30` → `ACCESS_TOKEN_EXPIRE_DAYS: 7`
  - Add `OPENROUTER_API_KEY` for AI service
  - Add `OPENROUTER_BASE_URL: https://openrouter.ai/api/v1`

- [ ] 1A.1.3: Remove unused/incorrect variables
  - Remove sensor simulation variables (not needed per PRD v2)
  - Clean up Redis references if not using

- [ ] 1A.1.4: Verify service dependencies
  - Ensure postgres healthcheck works
  - Ensure backend waits for postgres

### Task 1A.2: Update Environment Files
**Files:** `.env` (root), `backend/.env`

- [ ] 1A.2.1: Update root `.env`
  - Add `OPENROUTER_API_KEY=your_openrouter_api_key_here`
  - Ensure PORT=8000 consistency
  - Add JWT_EXPIRY_DAYS=7

- [ ] 1A.2.2: Update `backend/.env`
  - Change `PORT=5000` → `PORT=8000`
  - Change `ACCESS_TOKEN_EXPIRE_DAYS=30` → `ACCESS_TOKEN_EXPIRE_DAYS=7`
  - Add `OPENROUTER_API_KEY=your_openrouter_api_key_here`
  - Add `OPENROUTER_BASE_URL=https://openrouter.ai/api/v1`
  - Remove unused sensor simulation variables

- [ ] 1A.2.3: Create `.env.example` templates
  - Update both root and backend .env.example files
  - Document all required variables with comments

### Task 1A.3: Update Database Initialization & Seed Data
**Files:** `backend/db_init.py` (contains `seed_test_data()` function)

- [ ] 1A.3.1: Update test users to match new User model
  - Remove old fields: `email`, `phone_number`, `farm_location`, `farm_size`, `crop_types`, `is_admin`
  - Add new fields: `full_name`, `farm_location_name`, `farm_location_lat`, `farm_location_lng`, `crop_type`
  - Use Malaysian locations with real coordinates

- [ ] 1A.3.2: Update seed users data
  ```python
  # New test users format
  users_data = [
      {
          "username": "admin",
          "password": "admin123",
          "full_name": "Admin User",
          "farm_location_name": "Kuala Lumpur",
          "farm_location_lat": 3.1390,
          "farm_location_lng": 101.6869,
          "crop_type": "rice"
      },
      {
          "username": "ahmad",
          "password": "password123",
          "full_name": "Ahmad bin Ibrahim",
          "farm_location_name": "Kedah",
          "farm_location_lat": 6.1184,
          "farm_location_lng": 100.3685,
          "crop_type": "rice"
      },
      # ... more test users
  ]
  ```

- [ ] 1A.3.3: Add pest_weather_correlations seed
  - Add import for PestWeatherCorrelation model
  - Seed 8 rice pest correlations from PRD v2 Section 7.4
  - Include: Rice Stem Borer, Rice Leaf Folder, Brown Planthopper, Rice Bug, Rice Blast, Bacterial Leaf Blight, Sheath Blight, Green Leafhopper

- [ ] 1A.3.4: Update pest detection seed data
  - Use correct field names matching updated PestDetection model
  - Include danger_level field

- [ ] 1A.3.5: Import and register new models
  - Add imports for new models (PestReport, PestWeatherCorrelation, WeatherCache)
  - Ensure all models are registered with Base.metadata

### Task 1A.4: Update Alembic Migration
**Files:** `backend/alembic/versions/`, `backend/alembic/env.py`

- [ ] 1A.4.1: Ensure env.py imports all models
  - Import new models: PestReport, PestWeatherCorrelation, WeatherCache

- [ ] 1A.4.2: Create migration for all schema changes
  - After all model changes are complete
  - Generate single migration with all table changes
  - Test migration up/down

---

## 🔧 MODIFY - Phase 1B: Backend Modifications (PRD v2)

> **Goal:** Modify existing code to match PRD v2 requirements

### Task 1B.1: User Model & Registration Updates
**Files:** `backend/models/user.py`, `backend/schemas/auth.py`, `backend/routers/auth.py`

- [ ] 1B.1.1: Add fields to User model
  - Add `full_name` VARCHAR(100)
  - Add `farm_location_name` VARCHAR(100) NOT NULL
  - Add `farm_location_lat` DECIMAL(10, 8) NOT NULL
  - Add `farm_location_lng` DECIMAL(11, 8) NOT NULL
  - Add `crop_type` VARCHAR(50) NOT NULL DEFAULT 'rice'

- [ ] 1B.1.2: Update auth schemas
  - Update `UserRegister` schema to require new fields
  - Add validation for Malaysian states/coordinates
  - Add crop_type enum validation (rice, vegetables, corn, oil_palm, rubber)
  - Update `UserResponse` to include new fields

- [ ] 1B.1.3: Update registration endpoint
  - Accept full_name, farm_location_name, lat/lng, crop_type
  - Validate location coordinates
  - Return user profile with all fields

- [ ] 1B.1.4: Create database migration
  - Generate Alembic migration for User table changes
  - Handle existing users (set defaults for new columns)
  - Test migration up/down

- [ ] 1B.1.5: Change JWT expiry to 7 days
  - Update `backend/utils/security.py` token expiration
  - Update config.py JWT_EXPIRY_DAYS

### Task 1B.2: Pest Detection Enhancements
**Files:** `backend/models/pest_detection.py`, `backend/schemas/pest.py`, `backend/routers/pest.py`

- [ ] 1B.2.1: Add confidence tiering logic
  - Implement 3-tier response based on confidence:
    - ≥70%: Successful detection (show pest info + AI recommendations)
    - 50-69%: Partial match (show possible pest + retry option)
    - <50%: Unknown (prompt retry with tips)

- [ ] 1B.2.2: Add retry tracking
  - Add `retry_count` field to detection tracking (session-based)
  - After 3 failed attempts: offer manual report option
  - Implement retry tips messages

- [ ] 1B.2.3: Update detection response schema
  - Add `status` field: "detected" | "partial" | "unknown"
  - Add `can_retry` boolean
  - Add `retry_count` integer
  - Add `tips` array for retry guidance
  - Add `offer_report` boolean

- [ ] 1B.2.4: Add danger_level assessment
  - Ensure danger_level is returned as "low" | "medium" | "high"
  - Map from existing severity_level

### Task 1B.3: Alert System Updates
**Files:** `backend/models/alert.py`, `backend/schemas/alert.py`

- [ ] 1B.3.1: Add pest_risk_warning alert type
  - Add PEST_RISK_WARNING to AlertType enum
  - Differentiate from PEST_DETECTION (detected) vs PEST_RISK_WARNING (predicted)

- [ ] 1B.3.2: Update alert response format
  - Ensure recommendations field is included in responses
  - Add source_data field for trigger information

---

## 🆕 NEW - Phase 1C: New Backend Features (PRD v2)

> **Goal:** Add new features required by PRD v2

### Task 1C.1: Pest Reports Table & Endpoints
**New Files:** `backend/models/pest_report.py`, `backend/schemas/pest_report.py`

- [ ] 1C.1.1: Create PestReport model
  ```python
  # Fields: id, user_id, image_url, description, observed_severity,
  #         ai_response (JSONB), status, reported_at
  ```

- [ ] 1C.1.2: Create pest report schemas
  - `PestReportCreate`: image_url, description (optional), observed_severity
  - `PestReportResponse`: all fields + ai_response

- [ ] 1C.1.3: Implement POST /pests/report endpoint
  - Accept image from failed detection attempts
  - Accept description and observed_severity
  - Call AI service for best-guess analysis
  - Store report in database

- [ ] 1C.1.4: Create database migration
  - Generate migration for pest_reports table

### Task 1C.2: Pest-Weather Correlations Table & Seed Data
**New Files:** `backend/models/pest_weather_correlation.py`

- [ ] 1C.2.1: Create PestWeatherCorrelation model
  ```python
  # Fields: id, pest_name, scientific_name, affected_crops (JSONB),
  #         risk_conditions (JSONB), risk_level, risk_message,
  #         prevention_tips (JSONB), data_source, created_at
  ```

- [ ] 1C.2.2: Create database migration

- [ ] 1C.2.3: Create seed script with 8 rice pest correlations
  - Rice Stem Borer
  - Rice Leaf Folder
  - Brown Planthopper
  - Rice Bug
  - Rice Blast (fungal)
  - Bacterial Leaf Blight
  - Sheath Blight
  - Green Leafhopper

### Task 1C.3: Weather Cache Table
**New Files:** `backend/models/weather_cache.py`

- [ ] 1C.3.1: Create WeatherCache model
  ```python
  # Fields: id, location_key (unique), location_name,
  #         current_conditions (JSONB), forecast_data (JSONB),
  #         ml_predictions (JSONB), fetched_at
  ```

- [ ] 1C.3.2: Update weather service to use database cache
  - Replace in-memory cache with database cache
  - Cache expiry: 30 minutes

- [ ] 1C.3.3: Create database migration

### Task 1C.4: Pest Risk Prediction Service & Endpoint
**New Files:** `backend/services/pest_risk_service.py`

- [ ] 1C.4.1: Create pest risk service
  - Load correlations for user's crop type
  - Check current weather against risk conditions
  - Generate risk assessment with risk factors

- [ ] 1C.4.2: Implement GET /pests/risk endpoint
  - Return current pest risk assessment
  - Include weather_summary, risks array, overall_risk

- [ ] 1C.4.3: Implement pest risk alert generation
  - Create alerts when conditions match risk patterns
  - Include prevention_tips in recommendations

### Task 1C.5: AI Service (OpenRouter Integration)
**New Files:** `backend/services/ai_service.py`

- [ ] 1C.5.1: Create OpenRouter API client
  - Configure API key from environment
  - Implement async HTTP client
  - Handle rate limiting and errors

- [ ] 1C.5.2: Implement recommendation generation
  - `get_pest_recommendations(pest_name, confidence, crop_type, weather)`
  - `get_weather_recommendations(alert_type, crop_type, conditions)`
  - Parse AI responses into structured format

- [ ] 1C.5.3: Integrate with pest detection
  - Call AI service when pest detected (≥70% confidence)
  - Store AI recommendations in detection record

- [ ] 1C.5.4: Integrate with alert generation
  - Call AI service when creating weather alerts
  - Include AI recommendations in alert

### Task 1C.6: Chatbot Endpoints
**New Files:** `backend/routers/chat.py`, `backend/services/chat_service.py`

- [ ] 1C.6.1: Create chat service
  - Build context from user profile (location, crop, weather)
  - Construct system prompt with context injection
  - Call OpenRouter API for responses

- [ ] 1C.6.2: Implement POST /chat/message endpoint
  - Accept message and optional session_id
  - Return AI response with context_used

- [ ] 1C.6.3: Implement POST /chat/image endpoint
  - Accept image + optional message
  - Route to pest detection flow
  - Return detection results in chat format

### Task 1C.7: Enhanced Dashboard Endpoint
**New Files:** `backend/routers/dashboard.py`

- [ ] 1C.7.1: Implement GET /dashboard endpoint
  - Aggregate: weather summary, alert count, recent alerts (top 3)
  - Include: recent detections (top 3), pest_risk_status
  - Return unified dashboard data

### Task 1C.8: Background Jobs Setup
**New Files:** `backend/jobs/scheduler.py`

- [ ] 1C.8.1: Set up APScheduler or similar
  - Configure 30-minute interval jobs

- [ ] 1C.8.2: Implement weather check job
  - Fetch weather for all user locations
  - Update weather cache
  - Check alert thresholds

- [ ] 1C.8.3: Implement pest risk check job
  - Check weather against pest correlations
  - Generate pest risk alerts

---

## 🔄 REPLACE - Phase 2: Mobile App (React Native + Expo)

> **Goal:** Fresh start with React Native + Expo (replacing Flutter)

### Task 2.1: React Native Project Setup
- [ ] 2.1.1: Initialize Expo project
  - Run `npx create-expo-app agrisense-mobile`
  - Configure app.json (name, slug, version)

- [ ] 2.1.2: Install dependencies
  - `axios` for API calls
  - `@react-native-async-storage/async-storage` for JWT storage
  - `expo-image-picker` for camera/gallery
  - `react-navigation` for navigation
  - `react-native-paper` for UI components (optional)

- [ ] 2.1.3: Configure project structure
  ```
  src/
  ├── screens/
  ├── components/
  ├── services/
  ├── context/
  ├── utils/
  └── constants/
  ```

- [ ] 2.1.4: Set up navigation
  - Auth stack (Login, Register)
  - Main stack (Dashboard, Weather, Detection, Alerts, Chat)
  - Bottom tab navigator

### Task 2.2: API Service Layer
- [ ] 2.2.1: Create API configuration
  - Base URL (dev/prod)
  - Axios instance with JWT interceptor

- [ ] 2.2.2: Create auth service
  - register(), login(), logout(), getCurrentUser()
  - Token storage with AsyncStorage

- [ ] 2.2.3: Create data services
  - weatherService (current, forecast)
  - pestService (detect, history, risk, report)
  - alertService (list, markRead)
  - chatService (message, image)
  - dashboardService (getDashboard)

### Task 2.3: Authentication Screens
- [ ] 2.3.1: Create Login screen
  - Username/password inputs
  - Login button, loading state
  - Navigate to Register link

- [ ] 2.3.2: Create Register screen
  - All required fields (username, password, full_name)
  - Farm location dropdown (Malaysian states)
  - Crop type dropdown
  - Coordinates auto-filled from state selection

- [ ] 2.3.3: Create Auth context
  - Store user and token state
  - Auto-login on app launch

### Task 2.4: Dashboard Screen
- [ ] 2.4.1: Create Dashboard layout
  - Weather card (current conditions)
  - Alert banner (unread count)
  - Quick actions (Detect Pest, Chat)
  - Recent detections (thumbnails)

- [ ] 2.4.2: Implement pull-to-refresh
- [ ] 2.4.3: Navigate to detail screens

### Task 2.5: Weather Screen
- [ ] 2.5.1: Create current weather display
- [ ] 2.5.2: Create 7-day forecast list
- [ ] 2.5.3: Display ML predictions/insights

### Task 2.6: Pest Detection Screen
- [ ] 2.6.1: Create image picker (camera/gallery)
- [ ] 2.6.2: Create detection results display
  - Confidence bar, danger level badge
  - AI recommendations list

- [ ] 2.6.3: Implement retry flow
  - Show tips for better photos
  - Offer manual report after 3 fails

- [ ] 2.6.4: Create manual report form
- [ ] 2.6.5: Create detection history list

### Task 2.7: Alerts Screen
- [ ] 2.7.1: Create alerts list (tabs: All/Unread)
- [ ] 2.7.2: Create alert detail view
- [ ] 2.7.3: Implement mark as read

### Task 2.8: Chat Screen
- [ ] 2.8.1: Create chat message list
- [ ] 2.8.2: Create text input + send button
- [ ] 2.8.3: Create image upload in chat
- [ ] 2.8.4: Display AI responses

### Task 2.9: Profile Screen
- [ ] 2.9.1: Display user profile info
- [ ] 2.9.2: Logout button

---

## Phase 3: Testing & Deployment

### Task 3.1: Integration Testing
- [ ] 3.1.1: Test complete user journey
- [ ] 3.1.2: Test error scenarios
- [ ] 3.1.3: Test data persistence
- [ ] 3.1.4: Performance testing

### Task 3.2: Backend Deployment
- [ ] 3.2.1: Create Docker configuration
- [ ] 3.2.2: Create Docker Compose file
- [ ] 3.2.3: Deploy to server
- [ ] 3.2.4: Set up PostgreSQL
- [ ] 3.2.5: Configure SSL

### Task 3.3: Mobile Build
- [ ] 3.3.1: Build Android APK with Expo
- [ ] 3.3.2: Test on physical device

### Task 3.4: Documentation
- [ ] 3.4.1: Update README.md
- [ ] 3.4.2: Create user manual
- [ ] 3.4.3: Prepare demo presentation

---

## Task Summary

| Category | Tasks | Status |
|----------|-------|--------|
| ✅ DONE (Phase 0+1) | 44 subtasks | Complete |
| 🔧 INFRA (Phase 1A) | 14 subtasks | Pending - DO FIRST |
| 🔧 MODIFY (Phase 1B) | 12 subtasks | Pending |
| 🆕 NEW (Phase 1C) | 24 subtasks | Pending |
| 🔄 REPLACE (Phase 2) | 28 subtasks | Pending |
| Phase 3 | 11 subtasks | Pending |
| **TOTAL** | **133 subtasks** | ~33% Complete |

---

## Malaysian Locations Reference

```python
MALAYSIAN_LOCATIONS = [
    {"name": "Perlis", "lat": 6.4449, "lng": 100.2048},
    {"name": "Kedah", "lat": 6.1184, "lng": 100.3685},
    {"name": "Penang", "lat": 5.4164, "lng": 100.3327},
    {"name": "Perak", "lat": 4.5921, "lng": 101.0901},
    {"name": "Selangor", "lat": 3.0738, "lng": 101.5183},
    {"name": "Negeri Sembilan", "lat": 2.7258, "lng": 101.9424},
    {"name": "Melaka", "lat": 2.1896, "lng": 102.2501},
    {"name": "Johor", "lat": 1.4854, "lng": 103.7618},
    {"name": "Pahang", "lat": 3.8126, "lng": 103.3256},
    {"name": "Terengganu", "lat": 5.3117, "lng": 103.1324},
    {"name": "Kelantan", "lat": 6.1254, "lng": 102.2381},
    {"name": "Sabah", "lat": 5.9788, "lng": 116.0753},
    {"name": "Sarawak", "lat": 1.5533, "lng": 110.3592},
    {"name": "Kuala Lumpur", "lat": 3.1390, "lng": 101.6869}
]

CROP_TYPES = ["rice", "vegetables", "corn", "oil_palm", "rubber"]
```

---

## Recommended Execution Order

### Phase 1A: Infrastructure First (Do This First!)
1. **1A.1** - Fix Docker Compose configuration
2. **1A.2** - Update environment files
3. **1A.3** - Update database seed script (after model changes)
4. **1A.4** - Create Alembic migration (after all model changes)

### Phase 1B-1C: Backend Changes
5. **1B.1** - User model + Auth changes (foundation)
6. **1C.2** - Pest-Weather Correlations table + seed data
7. **1C.3** - Weather Cache table
8. **1B.2** - Pest Detection enhancements (confidence tiering)
9. **1B.3** - Alert System updates
10. **1C.1** - Pest Reports table + endpoints
11. **1C.5** - AI Service (OpenRouter integration)
12. **1C.4** - Pest Risk Prediction service
13. **1C.6** - Chatbot endpoints
14. **1C.7** - Dashboard endpoint
15. **1C.8** - Background Jobs

### Phase 2: Mobile App
16. **Phase 2** - React Native + Expo (fresh start)

---

## User Decisions

- **Flutter folder:** DELETE existing `mobile/` folder when starting React Native
- **Migration strategy:** CLEAR existing test users, create fresh schema with required fields
- **Starting point:** Infrastructure first (Phase 1A), then User model + Auth changes (Task 1B.1)

---

## Notes

- **JWT Expiry:** Change from 30 days to 7 days per PRD v2
- **AI Model:** Using OpenRouter API with `meta-llama/llama-3.1-8b-instruct:free`
- **ML Models:** Still using mock services until teammate's models ready
- **Database:** SQLite for development, PostgreSQL for production
- **No Push Notifications:** In-app alerts only (out of scope per PRD v2)
