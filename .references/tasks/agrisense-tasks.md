# AgriSense - Task List

**Generated from PRD:** `.references/prd/agrisense-prd.md`  
**Project:** AgriSense - IoT-Driven Early Warning System for Weather and Pest Risk Management  
**Timeline:** 14 Weeks  
**Last Updated:** January 2025

**🎯 DUAL CORE FEATURES (Equal Priority):**
1. 🌤️ **Weather Early Warning System** - Real-time forecasts, weather alerts, recommendations
2. 🐛 **Pest Risk Management System** - AI-powered pest detection, environmental monitoring

---

## 📋 Task Execution Rules

1. **Sequential Execution:** Tasks must be completed in order (top to bottom)
2. **One at a Time:** Only one subtask is worked on at a time
3. **Approval Required:** Wait for user approval before starting next subtask
4. **Atomic Tasks:** Each subtask is a complete, testable unit of work
5. **Mark Complete:** Update checkbox `[x]` after completion and review

---

## 🎯 Progress Overview

**Total Parent Tasks:** 10  
**Total Subtasks:** 87  
**Completed:** 4/87 (5%)  
**Current Phase:** Phase 0 - Setup & Planning

**⚠️ IMPORTANT:** This project has **DUAL CORE FEATURES** with equal priority:
- 🌤️ Weather Early Warning System (Task 1.7)
- 🐛 Pest Risk Management System (Tasks 1.4-1.6)

---

## Phase 0: Setup & Planning (Week 1-2)

### Task 0.1: Project Initialization
**Goal:** Set up project structure and version control  
**Dependencies:** None  
**Estimated Time:** 2 hours

- [x] 0.1.1: Create project root directory structure
  - Create `/backend` folder
  - Create `/mobile` folder
  - Create `/docs` folder
  - Create `.gitignore` for Python and Flutter
  
- [x] 0.1.2: Initialize Git repository (Already initialized)
  - Run `git init`
  - Create initial commit with folder structure
  - Create `.gitignore` with Python, Flutter, IDE exclusions
  
- [x] 0.1.3: Create README.md ✅
  - Add project title and description
  - Add tech stack overview
  - Add setup instructions placeholder
  - Add team member information

---

### Task 0.2: Backend Environment Setup
**Goal:** Set up FastAPI backend with database  
**Dependencies:** Task 0.1  
**Estimated Time:** 4 hours

- [x] 0.2.1: Initialize FastAPI project structure
  - Create `backend/main.py` with basic FastAPI app
  - Create `backend/requirements.txt` with dependencies
  - Create `backend/.env.example` for environment variables
  - Create `backend/config.py` for configuration management
  
- [ ] 0.2.2: Set up virtual environment
  - Create Python virtual environment in `/backend`
  - Install dependencies from requirements.txt
  - Verify FastAPI runs with `uvicorn main:app --reload`
  
- [ ] 0.2.3: Configure database connection
  - Install SQLAlchemy and psycopg2
  - Create `backend/database.py` with database connection
  - Create `backend/models/` folder for SQLAlchemy models
  - Test database connection with SQLite first
  
- [ ] 0.2.4: Set up Alembic for migrations
  - Initialize Alembic in backend folder
  - Configure `alembic.ini` with database URL
  - Create initial migration structure
  - Test migration with dummy table

---

### Task 0.3: Database Schema Implementation
**Goal:** Create all database tables per PRD schema  
**Dependencies:** Task 0.2  
**Estimated Time:** 3 hours

- [ ] 0.3.1: Create User model (simplified)
  - Define `users` table with SQLAlchemy
  - Fields: id, username, password_hash, created_at (simplified - no email/phone/location)
  - Add indexes on username (unique)
  - **Note:** Simplified schema for student project
  
- [ ] 0.3.2: Create SensorReading model
  - Define `sensor_readings` table
  - Fields: id, user_id, temperature, humidity, soil_moisture, timestamp
  - Add foreign key to users table
  - Add index on user_id and timestamp
  
- [ ] 0.3.3: Create PestDetection model
  - Define `pest_detections` table
  - Fields: id, user_id, image_url, pest_type, confidence, severity, recommendations, detected_at
  - Add foreign key to users table
  - Add index on user_id and detected_at
  
- [ ] 0.3.4: Create Alert model
  - Define `alerts` table
  - Fields: id, user_id, alert_type, title, message, severity, is_read, created_at
  - Add foreign key to users table
  - Add index on user_id and is_read
  
- [ ] 0.3.5: Run initial migration
  - Generate migration with `alembic revision --autogenerate`
  - Review migration file
  - Apply migration with `alembic upgrade head`
  - Verify all tables created in database

---

### Task 0.4: Synthetic Data Generator
**Goal:** Create Python script to generate simulated sensor data  
**Dependencies:** Task 0.3  
**Estimated Time:** 2 hours

- [ ] 0.4.1: Create data simulator script
  - Create `backend/utils/data_simulator.py`
  - Implement function to generate realistic temperature (20-35°C)
  - Implement function to generate realistic humidity (40-90%)
  - Implement function to generate realistic soil moisture (20-80%)
  
- [ ] 0.4.2: Add time-based variations
  - Add daily temperature cycle (cooler at night)
  - Add humidity variations (higher in morning/evening)
  - Add random fluctuations within realistic ranges
  
- [ ] 0.4.3: Create seed data script
  - Create `backend/scripts/seed_data.py`
  - Generate 7 days of historical sensor data
  - Insert data into sensor_readings table
  - Add test user account for development

---

## Phase 1: Backend Development (Week 3-8)

### Task 1.1: Authentication System - Models & Utils
**Goal:** Set up authentication infrastructure  
**Dependencies:** Task 0.3  
**Estimated Time:** 3 hours

- [ ] 1.1.1: Install authentication dependencies
  - Add `python-jose[cryptography]` to requirements.txt
  - Add `passlib[bcrypt]` for password hashing
  - Add `python-multipart` for form data
  - Install all dependencies
  
- [ ] 1.1.2: Create password hashing utilities
  - Create `backend/utils/security.py`
  - Implement `hash_password()` function using bcrypt
  - Implement `verify_password()` function
  - Add password strength validation
  
- [ ] 1.1.3: Create JWT token utilities (simplified)
  - Add JWT secret key to config
  - Implement `create_access_token()` function
  - Implement `decode_access_token()` function
  - Set token expiration to 30 days (long-lived for demo convenience)
  - **Note:** No refresh tokens - simplified for student project
  
- [ ] 1.1.4: Create authentication dependency
  - Create `backend/dependencies/auth.py`
  - Implement `get_current_user()` dependency
  - Extract token from Authorization header
  - Validate token and return user object

---

### Task 1.2: Authentication System - API Endpoints
**Goal:** Implement register and login endpoints  
**Dependencies:** Task 1.1  
**Estimated Time:** 4 hours

- [ ] 1.2.1: Create Pydantic schemas (simplified)
  - Create `backend/schemas/user.py`
  - Define `UserRegister` schema (username, password only - simplified)
  - Define `UserLogin` schema (username, password)
  - Define `UserResponse` schema (id, username, created_at)
  - Define `Token` schema (access_token, token_type, expires_in)
  - **Note:** No email/phone/location fields - simplified for demo
  
- [ ] 1.2.2: Implement registration endpoint (simplified)
  - Create `backend/routers/auth.py`
  - Implement `POST /api/auth/register`
  - Validate username uniqueness (no email validation needed)
  - Validate password min 6 chars (simplified from 8)
  - Hash password before storing
  - Return user data and JWT token immediately
  
- [ ] 1.2.3: Implement login endpoint (simplified)
  - Implement `POST /api/auth/login`
  - Verify username exists in database
  - Verify password matches hash
  - Generate and return JWT token (30-day expiry)
  - Return 401 for invalid credentials
  
- [ ] 1.2.4: Implement get current user endpoint
  - Implement `GET /api/auth/me`
  - Require authentication (use get_current_user dependency)
  - Return current user's profile data
  
- [ ] 1.2.5: Test authentication flow (simplified)
  - Test registration with valid username/password
  - Test registration with duplicate username (should fail)
  - Test login with correct credentials
  - Test login with wrong password (should fail)
  - Test protected endpoint with valid token
  - Test protected endpoint without token (should fail)
  - **Note:** No email tests needed - simplified auth

---

### Task 1.3: Sensor Data API
**Goal:** Implement endpoints to retrieve sensor readings  
**Dependencies:** Task 0.4, Task 1.1  
**Estimated Time:** 3 hours

- [ ] 1.3.1: Create sensor data schemas
  - Create `backend/schemas/sensor.py`
  - Define `SensorReadingResponse` schema
  - Define `SensorHistoryResponse` schema with pagination
  
- [ ] 1.3.2: Implement current readings endpoint
  - Create `backend/routers/sensors.py`
  - Implement `GET /api/sensors/current`
  - Require authentication
  - Return latest sensor reading for current user
  - Generate new reading if none exists in last 30 seconds
  
- [ ] 1.3.3: Implement historical readings endpoint
  - Implement `GET /api/sensors/history`
  - Add query parameters: days (default 7), limit (default 100)
  - Return paginated sensor readings
  - Order by timestamp descending
  
- [ ] 1.3.4: Implement background data generation
  - Create `backend/tasks/sensor_task.py`
  - Implement function to generate sensor reading every 30 seconds
  - Store reading in database for all users
  - Add simple in-memory scheduler (or use APScheduler)
  
- [ ] 1.3.5: Test sensor endpoints
  - Test current readings returns latest data
  - Test history returns correct number of records
  - Test pagination works correctly
  - Test authentication is required

---

### Task 1.4: Pest Risk Management System - Image Upload (CORE FEATURE #2) 🐛
**Goal:** Implement image upload and storage for pest detection  
**Dependencies:** Task 1.1  
**Estimated Time:** 3 hours  
**⚠️ CRITICAL:** This is a CORE FEATURE with equal priority to Weather Early Warning

- [ ] 1.4.1: Set up image storage
  - Create `backend/uploads/` folder for images
  - Add uploads folder to .gitignore
  - Install `python-multipart` for file uploads
  - Create `backend/utils/file_storage.py` helper
  
- [ ] 1.4.2: Implement image validation
  - Create `backend/utils/image_validator.py`
  - Validate file type (JPEG, PNG only)
  - Validate file size (max 5MB)
  - Validate image dimensions (min 224x224)
  
- [ ] 1.4.3: Implement image upload endpoint
  - Create `backend/routers/pest_detection.py`
  - Implement `POST /api/pest-detection/upload`
  - Require authentication
  - Accept multipart/form-data with image file
  - Validate image using validator
  - Save image to uploads folder with unique filename
  - Return image URL and upload ID

---

### Task 1.5: Pest Detection API - Mock ML Service
**Goal:** Create mock ML service for pest detection  
**Dependencies:** Task 1.4  
**Estimated Time:** 2 hours

- [ ] 1.5.1: Create mock ML service
  - Create `backend/services/ml_service.py`
  - Implement `detect_pest()` function
  - Return mock predictions with random pest types
  - Include confidence scores (0.75-0.95)
  - Include severity levels (low, medium, high)
  
- [ ] 1.5.2: Define pest types and recommendations
  - Create `backend/data/pest_data.json`
  - Define 5-10 common Malaysian pests (aphids, whiteflies, etc.)
  - Add treatment recommendations for each pest
  - Add prevention tips
  
- [ ] 1.5.3: Integrate mock service with upload endpoint
  - Call `detect_pest()` after image upload
  - Store detection result in pest_detections table
  - Return detection result to client
  - Include image URL, pest type, confidence, recommendations

---

### Task 1.6: Pest Detection API - History & Details
**Goal:** Implement endpoints to retrieve past detections  
**Dependencies:** Task 1.5  
**Estimated Time:** 2 hours

- [ ] 1.6.1: Create pest detection schemas
  - Create `backend/schemas/pest_detection.py`
  - Define `PestDetectionResponse` schema
  - Define `PestDetectionListResponse` with pagination
  
- [ ] 1.6.2: Implement detection history endpoint
  - Implement `GET /api/pest-detection/history`
  - Require authentication
  - Return user's past detections
  - Add pagination (limit, offset)
  - Order by detected_at descending
  
- [ ] 1.6.3: Implement detection details endpoint
  - Implement `GET /api/pest-detection/{detection_id}`
  - Require authentication
  - Verify detection belongs to current user
  - Return full detection details including image URL
  
- [ ] 1.6.4: Test pest detection flow
  - Test image upload with valid image
  - Test upload with invalid file type (should fail)
  - Test upload with oversized file (should fail)
  - Test detection result is stored in database
  - Test history endpoint returns detections
  - Test details endpoint returns correct detection

---

### Task 1.7: Weather Early Warning System (CORE FEATURE #1) 🌤️
**Goal:** Integrate OpenWeatherMap API for weather forecasts, alerts, and recommendations  
**Dependencies:** Task 1.1  
**Estimated Time:** 4 hours  
**⚠️ CRITICAL:** This is a CORE FEATURE with equal priority to Pest Detection

- [ ] 1.7.1: Set up OpenWeatherMap API
  - Sign up for free OpenWeatherMap API key
  - Add API key to .env file
  - Add API key to config.py
  - Install `requests` library
  
- [ ] 1.7.2: Create weather service
  - Create `backend/services/weather_service.py`
  - Implement `get_current_weather(lat, lon)` function
  - Implement `get_forecast(lat, lon, days=7)` function
  - Handle API errors gracefully
  
- [ ] 1.7.3: Implement weather caching
  - Create `backend/utils/cache.py` (simple in-memory cache)
  - Cache weather data for 30 minutes
  - Return cached data if available
  - Reduce API calls to stay within free tier limits
  
- [ ] 1.7.4: Create weather schemas
  - Create `backend/schemas/weather.py`
  - Define `CurrentWeatherResponse` schema
  - Define `ForecastDayResponse` schema
  - Define `WeatherForecastResponse` schema
  
- [ ] 1.7.5: Implement weather endpoints
  - Create `backend/routers/weather.py`
  - Implement `GET /api/weather/current`
  - Implement `GET /api/weather/forecast`
  - Require authentication
  - Use user's location from profile (default: Kuala Lumpur)
  - Return weather data from OpenWeatherMap
  
- [ ] 1.7.6: Test weather endpoints
  - Test current weather returns valid data
  - Test forecast returns 7 days
  - Test caching works (check API call count)
  - Test error handling for invalid API key

---

### Task 1.8: Alert System - Generation Logic
**Goal:** Implement alert generation based on sensor data and weather  
**Dependencies:** Task 1.3, Task 1.7  
**Estimated Time:** 3 hours

- [ ] 1.8.1: Create alert generation service
  - Create `backend/services/alert_service.py`
  - Implement `generate_sensor_alerts(user_id)` function
  - Check temperature thresholds (>35°C = high temp alert)
  - Check humidity thresholds (<40% or >90% = alert)
  - Check soil moisture (<30% = low moisture alert)
  
- [ ] 1.8.2: Implement weather-based alerts (CORE FEATURE)
  - Implement `generate_weather_alerts(user_id)` function
  - Check for heavy rain forecast (>50mm = high priority alert)
  - Check for extreme heat (>35°C = medium priority alert)
  - Check for storms (wind >40 km/h = high priority alert)
  - Check for low temperature (<15°C = low priority alert)
  - Generate actionable recommendations (e.g., "Cover crops, prepare drainage")
  
- [ ] 1.8.3: Implement pest risk alerts
  - Implement `generate_pest_alerts(user_id)` function
  - Create alert when high-severity pest detected
  - Create alert for recurring pest detections
  
- [ ] 1.8.4: Create background alert task
  - Create `backend/tasks/alert_task.py`
  - Run alert generation every 5 minutes
  - Check all users and generate alerts
  - Avoid duplicate alerts (check if similar alert exists in last 24h)
  
- [ ] 1.8.5: Test alert generation
  - Test high temperature triggers alert
  - Test low soil moisture triggers alert
  - Test weather forecast triggers alert
  - Test pest detection triggers alert
  - Test no duplicate alerts created

---

### Task 1.9: Alert System - API Endpoints
**Goal:** Implement endpoints to retrieve and manage alerts  
**Dependencies:** Task 1.8  
**Estimated Time:** 2 hours

- [ ] 1.9.1: Create alert schemas
  - Create `backend/schemas/alert.py`
  - Define `AlertResponse` schema
  - Define `AlertListResponse` with pagination
  - Define `AlertUpdateRequest` schema
  
- [ ] 1.9.2: Implement get alerts endpoint
  - Create `backend/routers/alerts.py`
  - Implement `GET /api/alerts`
  - Require authentication
  - Return user's alerts ordered by created_at descending
  - Add filter for unread alerts only
  - Add pagination
  
- [ ] 1.9.3: Implement mark as read endpoint
  - Implement `PUT /api/alerts/{alert_id}/read`
  - Require authentication
  - Verify alert belongs to current user
  - Update is_read to true
  - Return updated alert
  
- [ ] 1.9.4: Implement unread count endpoint
  - Implement `GET /api/alerts/unread-count`
  - Require authentication
  - Return count of unread alerts for current user
  
- [ ] 1.9.5: Test alert endpoints
  - Test get alerts returns user's alerts
  - Test filter for unread alerts works
  - Test mark as read updates alert
  - Test unread count is accurate
  - Test user cannot access other user's alerts

---

### Task 1.10: Backend Testing & Documentation
**Goal:** Add comprehensive tests and API documentation  
**Dependencies:** All Phase 1 tasks  
**Estimated Time:** 4 hours

- [ ] 1.10.1: Set up pytest
  - Install pytest and pytest-asyncio
  - Create `backend/tests/` folder
  - Create `conftest.py` with test fixtures
  - Create test database configuration
  
- [ ] 1.10.2: Write authentication tests
  - Create `backend/tests/test_auth.py`
  - Test user registration
  - Test user login
  - Test JWT token validation
  - Test protected endpoints
  
- [ ] 1.10.3: Write API endpoint tests
  - Create `backend/tests/test_sensors.py`
  - Create `backend/tests/test_pest_detection.py`
  - Create `backend/tests/test_weather.py`
  - Create `backend/tests/test_alerts.py`
  - Test all CRUD operations
  - Test error cases
  
- [ ] 1.10.4: Configure Swagger documentation
  - Add API title and description to main.py
  - Add tags to all router groups
  - Add response models to all endpoints
  - Add example requests/responses
  - Test Swagger UI at `/docs`
  
- [ ] 1.10.5: Create API documentation
  - Create `docs/API.md`
  - Document all endpoints with examples
  - Document authentication flow
  - Document error codes
  - Add Postman collection export

---

### Task 1.11: Backend Deployment Preparation
**Goal:** Prepare backend for deployment to own server  
**Dependencies:** Task 1.10  
**Estimated Time:** 3 hours

- [ ] 1.11.1: Create Docker configuration
  - Create `backend/Dockerfile`
  - Use Python 3.10 slim image
  - Copy requirements and install dependencies
  - Expose port 8000
  - Set CMD to run uvicorn
  
- [ ] 1.11.2: Create Docker Compose file
  - Create `docker-compose.yml` in project root
  - Add backend service
  - Add PostgreSQL service
  - Add volume for database persistence
  - Add volume for uploaded images
  - Configure environment variables
  
- [ ] 1.11.3: Create deployment scripts
  - Create `backend/scripts/deploy.sh`
  - Add commands to build Docker image
  - Add commands to run migrations
  - Add commands to start services
  
- [ ] 1.11.4: Create environment configuration
  - Create `.env.production.example`
  - Document all required environment variables
  - Add production database URL
  - Add JWT secret generation instructions
  
- [ ] 1.11.5: Test Docker deployment locally
  - Build Docker image
  - Run docker-compose up
  - Test all API endpoints work in Docker
  - Test database persistence
  - Test image uploads work with volumes

---

## Phase 2: Mobile App Development (Week 9-12)

### Task 2.1: Flutter Project Setup
**Goal:** Initialize Flutter project with dependencies  
**Dependencies:** Task 1.11 (backend must be ready)  
**Estimated Time:** 2 hours

- [ ] 2.1.1: Create Flutter project
  - Run `flutter create agrisense_mobile`
  - Set package name to `com.agrisense.app`
  - Configure Android minSdkVersion to 21
  - Configure iOS deployment target to 12.0
  
- [ ] 2.1.2: Add dependencies to pubspec.yaml
  - Add `http` for API calls
  - Add `shared_preferences` for local storage
  - Add `provider` for state management
  - Add `image_picker` for camera/gallery
  - Add `fl_chart` for data visualization
  - Add `intl` for date formatting
  
- [ ] 2.1.3: Configure project structure
  - Create `lib/models/` folder
  - Create `lib/services/` folder
  - Create `lib/screens/` folder
  - Create `lib/widgets/` folder
  - Create `lib/utils/` folder
  - Create `lib/constants/` folder
  
- [ ] 2.1.4: Set up app theme
  - Create `lib/constants/app_theme.dart`
  - Define primary color (green for agriculture)
  - Define text styles
  - Define spacing constants
  - Configure MaterialApp theme

---

### Task 2.2: API Service Layer
**Goal:** Create service classes to communicate with backend  
**Dependencies:** Task 2.1  
**Estimated Time:** 3 hours

- [ ] 2.2.1: Create API configuration
  - Create `lib/constants/api_constants.dart`
  - Define base URL (configurable for dev/prod)
  - Define all API endpoints as constants
  - Add timeout configuration
  
- [ ] 2.2.2: Create HTTP client wrapper
  - Create `lib/services/api_client.dart`
  - Implement GET, POST, PUT, DELETE methods
  - Add automatic JWT token injection from storage
  - Add error handling and response parsing
  - Add request/response logging for debugging
  
- [ ] 2.2.3: Create authentication service
  - Create `lib/services/auth_service.dart`
  - Implement `register()` method
  - Implement `login()` method
  - Implement `logout()` method
  - Implement `getCurrentUser()` method
  - Implement token storage using shared_preferences
  
- [ ] 2.2.4: Create data models
  - Create `lib/models/user.dart`
  - Create `lib/models/sensor_reading.dart`
  - Create `lib/models/pest_detection.dart`
  - Create `lib/models/weather.dart`
  - Create `lib/models/alert.dart`
  - Add `fromJson()` and `toJson()` methods

---

### Task 2.3: Authentication Screens
**Goal:** Build login and registration UI  
**Dependencies:** Task 2.2  
**Estimated Time:** 4 hours

- [ ] 2.3.1: Create login screen UI
  - Create `lib/screens/auth/login_screen.dart`
  - Add email text field with validation
  - Add password text field with obscure text
  - Add login button
  - Add "Don't have account? Register" link
  - Add loading indicator during API call
  
- [ ] 2.3.2: Implement login logic
  - Create form key for validation
  - Validate email format
  - Validate password not empty
  - Call auth_service.login() on button press
  - Show error message on failure
  - Navigate to dashboard on success
  - Store JWT token in shared_preferences
  
- [ ] 2.3.3: Create registration screen UI
  - Create `lib/screens/auth/register_screen.dart`
  - Add full name text field
  - Add email text field
  - Add phone text field
  - Add location text field (default: Kuala Lumpur)
  - Add password text field
  - Add confirm password text field
  - Add register button
  
- [ ] 2.3.4: Implement registration logic
  - Validate all fields not empty
  - Validate email format
  - Validate phone format
  - Validate passwords match
  - Call auth_service.register() on button press
  - Show success message
  - Navigate to login screen
  
- [ ] 2.3.5: Create splash screen
  - Create `lib/screens/splash_screen.dart`
  - Show app logo and name
  - Check if user is logged in (token exists)
  - Navigate to dashboard if logged in
  - Navigate to login if not logged in
  
- [ ] 2.3.6: Test authentication flow
  - Test registration with valid data
  - Test registration with invalid email
  - Test registration with mismatched passwords
  - Test login with correct credentials
  - Test login with wrong password
  - Test token persistence (close and reopen app)

---

### Task 2.4: Dashboard Screen - Layout
**Goal:** Create main dashboard with sensor data and weather  
**Dependencies:** Task 2.3  
**Estimated Time:** 4 hours

- [ ] 2.4.1: Create dashboard screen structure
  - Create `lib/screens/dashboard/dashboard_screen.dart`
  - Add AppBar with title and logout button
  - Add RefreshIndicator for pull-to-refresh
  - Add ScrollView for content
  - Add bottom navigation bar (Dashboard, Detection, Alerts, Profile)
  
- [ ] 2.4.2: Create sensor data service
  - Create `lib/services/sensor_service.dart`
  - Implement `getCurrentReading()` method
  - Implement `getHistory()` method
  - Add error handling
  
- [ ] 2.4.3: Create sensor data cards
  - Create `lib/widgets/sensor_card.dart`
  - Display temperature with icon and unit
  - Display humidity with icon and unit
  - Display soil moisture with icon and unit
  - Add color coding (green=good, yellow=warning, red=danger)
  - Add timestamp of last reading
  
- [ ] 2.4.4: Implement sensor data fetching
  - Call sensor_service.getCurrentReading() on screen load
  - Display loading indicator while fetching
  - Display sensor cards with data
  - Handle error state (show error message)
  - Implement pull-to-refresh to reload data
  
- [ ] 2.4.5: Create weather service
  - Create `lib/services/weather_service.dart`
  - Implement `getCurrentWeather()` method
  - Implement `getForecast()` method
  
- [ ] 2.4.6: Create weather widget
  - Create `lib/widgets/weather_card.dart`
  - Display current temperature
  - Display weather condition with icon
  - Display humidity and wind speed
  - Display 3-day forecast preview
  
- [ ] 2.4.7: Add weather to dashboard
  - Call weather_service.getCurrentWeather() on load
  - Display weather card below sensor cards
  - Add "View 7-day forecast" button
  - Navigate to detailed forecast screen

---

### Task 2.5: Dashboard Screen - Charts & History
**Goal:** Add data visualization and historical trends  
**Dependencies:** Task 2.4  
**Estimated Time:** 3 hours

- [ ] 2.5.1: Create chart widget
  - Create `lib/widgets/sensor_chart.dart`
  - Use fl_chart package
  - Display line chart for sensor readings
  - Add x-axis with time labels
  - Add y-axis with value labels
  - Add legend for multiple data series
  
- [ ] 2.5.2: Implement historical data fetching
  - Call sensor_service.getHistory(days: 7) on load
  - Parse data for chart display
  - Handle empty data state
  
- [ ] 2.5.3: Add chart to dashboard
  - Add "Historical Data" section to dashboard
  - Add tab selector (Temperature, Humidity, Soil Moisture)
  - Display chart for selected metric
  - Add date range selector (1 day, 7 days, 30 days)
  
- [ ] 2.5.4: Test dashboard functionality
  - Test sensor data loads correctly
  - Test weather data loads correctly
  - Test pull-to-refresh works
  - Test charts display historical data
  - Test tab switching works
  - Test error handling for API failures

---

### Task 2.6: Pest Detection Screen - Camera & Upload
**Goal:** Implement image capture and upload functionality  
**Dependencies:** Task 2.4  
**Estimated Time:** 4 hours

- [ ] 2.6.1: Create pest detection service
  - Create `lib/services/pest_detection_service.dart`
  - Implement `uploadImage(File image)` method
  - Implement `getHistory()` method
  - Implement `getDetectionDetails(String id)` method
  
- [ ] 2.6.2: Create pest detection screen UI
  - Create `lib/screens/pest_detection/detection_screen.dart`
  - Add "Take Photo" button with camera icon
  - Add "Choose from Gallery" button
  - Add preview area for selected image
  - Add "Analyze" button (disabled until image selected)
  
- [ ] 2.6.3: Implement image picker
  - Request camera and storage permissions
  - Implement camera capture using image_picker
  - Implement gallery selection using image_picker
  - Display selected image in preview area
  - Add option to retake/reselect image
  
- [ ] 2.6.4: Implement image upload
  - Compress image before upload (reduce file size)
  - Show loading indicator during upload
  - Call pest_detection_service.uploadImage()
  - Handle upload errors (show error message)
  - Navigate to results screen on success
  
- [ ] 2.6.5: Create detection results screen
  - Create `lib/screens/pest_detection/results_screen.dart`
  - Display uploaded image
  - Display detected pest type
  - Display confidence score with progress bar
  - Display severity level with color coding
  - Display treatment recommendations
  - Add "Save to History" button
  - Add "Detect Another" button
  
- [ ] 2.6.6: Test pest detection flow
  - Test camera capture works
  - Test gallery selection works
  - Test image upload succeeds
  - Test results display correctly
  - Test error handling for upload failures
  - Test navigation flow

---

### Task 2.7: Pest Detection Screen - History
**Goal:** Display past pest detections  
**Dependencies:** Task 2.6  
**Estimated Time:** 2 hours

- [ ] 2.7.1: Create detection history screen
  - Create `lib/screens/pest_detection/history_screen.dart`
  - Add AppBar with title
  - Add ListView for detection items
  - Add pull-to-refresh
  
- [ ] 2.7.2: Create detection list item widget
  - Create `lib/widgets/detection_list_item.dart`
  - Display thumbnail image
  - Display pest type
  - Display detection date
  - Display confidence score
  - Add tap to view details
  
- [ ] 2.7.3: Implement history fetching
  - Call pest_detection_service.getHistory() on load
  - Display loading indicator
  - Display list of detections
  - Handle empty state (no detections yet)
  - Implement pagination (load more on scroll)
  
- [ ] 2.7.4: Implement detection details
  - Navigate to results screen on item tap
  - Load full detection details
  - Display all information (image, pest, recommendations)
  
- [ ] 2.7.5: Test history functionality
  - Test history loads correctly
  - Test list items display properly
  - Test tap navigation works
  - Test empty state shows message
  - Test pagination works

---

### Task 2.8: Alerts Screen
**Goal:** Display and manage alerts  
**Dependencies:** Task 2.4  
**Estimated Time:** 3 hours

- [ ] 2.8.1: Create alert service
  - Create `lib/services/alert_service.dart`
  - Implement `getAlerts()` method
  - Implement `getUnreadCount()` method
  - Implement `markAsRead(String id)` method
  
- [ ] 2.8.2: Create alerts screen UI
  - Create `lib/screens/alerts/alerts_screen.dart`
  - Add AppBar with title
  - Add filter tabs (All, Unread)
  - Add ListView for alert items
  - Add pull-to-refresh
  
- [ ] 2.8.3: Create alert list item widget
  - Create `lib/widgets/alert_list_item.dart`
  - Display alert icon based on type
  - Display alert title
  - Display alert message (truncated)
  - Display timestamp
  - Add visual indicator for unread alerts
  - Add severity color coding
  
- [ ] 2.8.4: Implement alerts fetching
  - Call alert_service.getAlerts() on load
  - Display loading indicator
  - Display list of alerts
  - Handle empty state
  - Implement filter for unread alerts
  
- [ ] 2.8.5: Implement mark as read
  - Add tap handler on alert item
  - Show full alert details in dialog/bottom sheet
  - Call alert_service.markAsRead() on tap
  - Update UI to reflect read status
  
- [ ] 2.8.6: Add unread badge to navigation
  - Call alert_service.getUnreadCount() periodically
  - Display badge on Alerts tab in bottom navigation
  - Update count when alerts are read
  
- [ ] 2.8.7: Test alerts functionality
  - Test alerts load correctly
  - Test filter tabs work
  - Test mark as read updates UI
  - Test unread badge displays correct count
  - Test alert details display properly

---

### Task 2.9: Profile Screen
**Goal:** Display user profile and settings  
**Dependencies:** Task 2.4  
**Estimated Time:** 2 hours

- [ ] 2.9.1: Create profile screen UI
  - Create `lib/screens/profile/profile_screen.dart`
  - Add AppBar with title
  - Display user avatar (placeholder icon)
  - Display user name
  - Display user email
  - Display user phone
  - Display user location
  
- [ ] 2.9.2: Add settings options
  - Add "Edit Profile" button (placeholder for future)
  - Add "About" section with app version
  - Add "Privacy Policy" link (placeholder)
  - Add "Terms of Service" link (placeholder)
  
- [ ] 2.9.3: Implement logout
  - Add "Logout" button at bottom
  - Show confirmation dialog on tap
  - Call auth_service.logout()
  - Clear stored token
  - Navigate to login screen
  
- [ ] 2.9.4: Test profile functionality
  - Test user data displays correctly
  - Test logout clears token
  - Test logout navigates to login
  - Test cannot access app after logout

---

### Task 2.10: Mobile App Testing & Polish
**Goal:** Test entire app and fix bugs  
**Dependencies:** All Phase 2 tasks  
**Estimated Time:** 4 hours

- [ ] 2.10.1: Test complete user flow
  - Test registration → login → dashboard flow
  - Test pest detection → results → history flow
  - Test alerts → mark as read flow
  - Test profile → logout flow
  
- [ ] 2.10.2: Test error handling
  - Test app behavior with no internet
  - Test app behavior with API errors
  - Test app behavior with invalid tokens
  - Test app behavior with slow network
  
- [ ] 2.10.3: Fix UI issues
  - Fix layout issues on different screen sizes
  - Fix text overflow issues
  - Fix image loading issues
  - Improve loading states
  - Improve error messages
  
- [ ] 2.10.4: Add loading states
  - Add shimmer loading for lists
  - Add skeleton screens for data loading
  - Add progress indicators for uploads
  
- [ ] 2.10.5: Optimize performance
  - Optimize image loading and caching
  - Reduce unnecessary API calls
  - Implement proper state management
  - Fix memory leaks
  
- [ ] 2.10.6: Test on real device
  - Install APK on Android device
  - Test all features on real device
  - Test camera functionality
  - Test performance and responsiveness
  - Fix device-specific issues

---

## Phase 3: Integration & Deployment (Week 13-14)

### Task 3.1: ML Model Integration (Optional)
**Goal:** Replace mock ML service with real model  
**Dependencies:** Task 1.5, ML team delivery  
**Estimated Time:** 4 hours

- [ ] 3.1.1: Receive ML model from team
  - Get trained model file (.h5, .pt, or .onnx)
  - Get model input/output specifications
  - Get preprocessing requirements
  - Get class labels mapping
  
- [ ] 3.1.2: Set up ML inference
  - Install TensorFlow/PyTorch in backend
  - Load model in ml_service.py
  - Implement image preprocessing
  - Implement inference function
  - Implement postprocessing
  
- [ ] 3.1.3: Update detect_pest function
  - Replace mock logic with real model inference
  - Keep same response format
  - Add confidence threshold filtering
  - Add error handling for inference failures
  
- [ ] 3.1.4: Test ML integration
  - Test with various pest images
  - Verify predictions are reasonable
  - Test inference speed (should be <5 seconds)
  - Test error handling
  
- [ ] 3.1.5: Fallback to Roboflow (if ML team fails)
  - Sign up for Roboflow account
  - Upload pest detection dataset
  - Train model on Roboflow
  - Get API key and model endpoint
  - Integrate Roboflow API in ml_service.py

---

### Task 3.2: Backend Deployment
**Goal:** Deploy backend to production server  
**Dependencies:** Task 1.11  
**Estimated Time:** 3 hours

- [ ] 3.2.1: Prepare production server
  - Set up Linux server (Ubuntu 22.04)
  - Install Docker and Docker Compose
  - Configure firewall (allow ports 80, 443, 8000)
  - Set up domain name (optional)
  
- [ ] 3.2.2: Configure production environment
  - Create `.env` file with production values
  - Generate secure JWT secret
  - Set up PostgreSQL database
  - Configure OpenWeatherMap API key
  
- [ ] 3.2.3: Deploy backend
  - Copy project files to server
  - Build Docker image
  - Run docker-compose up -d
  - Run database migrations
  - Seed initial data
  
- [ ] 3.2.4: Configure reverse proxy (optional)
  - Install Nginx
  - Configure SSL with Let's Encrypt
  - Set up reverse proxy to backend
  - Test HTTPS access
  
- [ ] 3.2.5: Test production deployment
  - Test all API endpoints from Postman
  - Test authentication flow
  - Test image uploads
  - Test database persistence
  - Monitor logs for errors

---

### Task 3.3: Mobile App Production Build
**Goal:** Build production APK for distribution  
**Dependencies:** Task 2.10  
**Estimated Time:** 2 hours

- [ ] 3.3.1: Update API base URL
  - Change API_BASE_URL to production server URL
  - Test app connects to production backend
  
- [ ] 3.3.2: Configure app signing
  - Generate keystore for app signing
  - Update android/app/build.gradle with signing config
  - Store keystore securely
  
- [ ] 3.3.3: Update app metadata
  - Update app name in AndroidManifest.xml
  - Update app icon (launcher icon)
  - Update app version (1.0.0)
  - Update package name if needed
  
- [ ] 3.3.4: Build release APK
  - Run `flutter build apk --release`
  - Test APK on real device
  - Verify all features work
  - Check APK size (<50MB)
  
- [ ] 3.3.5: Prepare for distribution
  - Create release notes
  - Take screenshots for documentation
  - Create user guide (optional)

---

### Task 3.4: Final Testing & Demo Preparation
**Goal:** End-to-end testing and demo preparation  
**Dependencies:** Task 3.2, Task 3.3  
**Estimated Time:** 3 hours

- [ ] 3.4.1: End-to-end testing
  - Test complete user journey from registration to detection
  - Test with multiple user accounts
  - Test concurrent users
  - Test data persistence
  - Test all error scenarios
  
- [ ] 3.4.2: Performance testing
  - Test API response times
  - Test image upload speed
  - Test app responsiveness
  - Test with poor network conditions
  
- [ ] 3.4.3: Create demo data
  - Create demo user account
  - Generate sample sensor data
  - Upload sample pest images
  - Generate sample alerts
  
- [ ] 3.4.4: Prepare demo script
  - Write step-by-step demo flow
  - Prepare talking points for each feature
  - Practice demo presentation
  - Prepare backup plan for demo failures
  
- [ ] 3.4.5: Create demo video
  - Record screen while using app
  - Add voiceover explaining features
  - Edit video (add intro/outro)
  - Export in HD quality

---

### Task 3.5: Documentation & Handover
**Goal:** Complete all documentation  
**Dependencies:** Task 3.4  
**Estimated Time:** 3 hours

- [ ] 3.5.1: Update README
  - Add project description
  - Add features list
  - Add tech stack
  - Add setup instructions
  - Add deployment instructions
  - Add screenshots
  
- [ ] 3.5.2: Create user documentation
  - Create user guide with screenshots
  - Document each feature
  - Add troubleshooting section
  - Add FAQ section
  
- [ ] 3.5.3: Create developer documentation
  - Document code structure
  - Document API endpoints
  - Document database schema
  - Add code comments
  - Create architecture diagram
  
- [ ] 3.5.4: Create deployment guide
  - Document server setup steps
  - Document environment variables
  - Document backup procedures
  - Document monitoring setup
  
- [ ] 3.5.5: Prepare final report
  - Write project summary
  - Document challenges faced
  - Document solutions implemented
  - Add future enhancement suggestions
  - Include demo video link
  - Include GitHub repository link

---

## 📊 Task Summary by Phase

| Phase | Tasks | Subtasks | Estimated Time |
|-------|-------|----------|----------------|
| Phase 0: Setup | 4 | 17 | 11 hours |
| Phase 1: Backend | 7 | 43 | 27 hours |
| Phase 2: Mobile | 6 | 22 | 26 hours |
| Phase 3: Integration | 5 | 19 | 15 hours |
| **TOTAL** | **22** | **101** | **79 hours** |

---

## 🎯 Critical Path

The following tasks are on the critical path and cannot be delayed:

1. Task 0.2: Backend Environment Setup
2. Task 0.3: Database Schema Implementation
3. Task 1.1: Authentication System - Models & Utils
4. Task 1.2: Authentication System - API Endpoints
5. Task 1.5: Pest Detection API - Mock ML Service
6. Task 2.1: Flutter Project Setup
7. Task 2.3: Authentication Screens
8. Task 2.6: Pest Detection Screen - Camera & Upload
9. Task 3.2: Backend Deployment
10. Task 3.3: Mobile App Production Build

---

## 📝 Notes

- **Sequential Execution:** Tasks must be completed in order within each phase
- **Dependencies:** Some tasks can only start after previous tasks are complete
- **Time Estimates:** Based on single developer working full-time
- **Flexibility:** Time estimates may vary based on experience and issues encountered
- **Testing:** Each task includes testing subtasks - do not skip these
- **Documentation:** Update documentation as you complete tasks

---

## ✅ Completion Checklist

Before marking the project complete, ensure:

- [ ] All 101 subtasks are marked complete
- [ ] Backend is deployed and accessible
- [ ] Mobile app APK is built and tested
- [ ] All API endpoints are documented
- [ ] All tests are passing
- [ ] Demo video is created
- [ ] Documentation is complete
- [ ] Code is pushed to GitHub
- [ ] Final report is submitted

---

**Ready to start? Begin with Task 0.1.1!** 🚀
