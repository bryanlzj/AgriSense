# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AgriSense is an IoT-driven agricultural monitoring system built as a capstone project for educational purposes. It's a **simulation-based system** using synthetic sensor data (no physical hardware required). The system consists of two main applications:

1. **Backend API** - FastAPI (Python) REST API with PostgreSQL/SQLite database
2. **Mobile App** - Flutter (Dart) cross-platform mobile application

**Key Features:**
- AI-powered pest detection via image upload
- Simulated environmental monitoring (temperature, humidity, soil moisture)
- Weather forecasting via OpenWeatherMap API
- Smart alert system for pest risks and weather warnings
- Historical data tracking and visualization

## Development Commands

### Backend (FastAPI)

**Setup:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac
pip install -r requirements.txt
```

**Running the server:**
```bash
cd backend
python run.py                  # Development server on port 8000
# Alternative: uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Database Migrations:**
```bash
cd backend

# Create new migration after model changes
alembic revision --autogenerate -m "Description of changes"

# Apply all pending migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# Check current migration version
alembic current

# View migration history
alembic history
```

**Testing:**
```bash
cd backend

# Run all tests
pytest

# Run with coverage report
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run specific test function
pytest tests/test_auth.py::TestUserRegistration::test_register_new_user

# Run with verbose output
pytest -v
```

**Code Quality:**
```bash
cd backend
black backend/        # Format code
flake8 backend/       # Lint code
mypy backend/         # Type checking
```

**Database Management:**
```bash
# Start PostgreSQL + Adminer (Docker)
docker compose up postgres adminer -d

# Stop database services
docker compose down

# Migrate data from SQLite to PostgreSQL
cd backend
python scripts/migrate_sqlite_to_postgres.py

# Seed test data
python scripts/seed_data.py
```

**Access Points:**
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Adminer (DB UI): http://localhost:8080 (postgres/agrisense_user/changeme/agrisense)

### Mobile (Flutter)

**Setup:**
```bash
cd mobile
flutter pub get
```

**Running:**
```bash
cd mobile

# Run on connected device/emulator
flutter run

# Run on specific device
flutter devices              # List available devices
flutter run -d <device-id>   # Run on specific device
```

**Building:**
```bash
cd mobile

# Build APK (Android)
flutter build apk --release

# Build IPA (iOS, Mac only)
flutter build ios --release
```

**Testing:**
```bash
cd mobile
flutter test                 # Run unit tests
flutter test integration_test  # Run integration tests
```

**Utilities:**
```bash
flutter clean                # Clean build artifacts
flutter pub get              # Install dependencies
flutter doctor               # Check Flutter installation
```

### Docker (Full Stack)

```bash
# Start all services (backend + postgres + adminer)
docker compose up -d

# Stop all services
docker compose down

# View logs
docker compose logs -f backend

# Rebuild backend image
docker compose build backend
```

## Architecture

### Backend Structure

The backend follows a **layered architecture** with clear separation of concerns:

**Key Layers:**
1. **Routers** (`routers/`) - API endpoints, request/response handling
2. **Services** (`services/`) - Business logic (weather fetching, alert generation)
3. **Models** (`models/`) - SQLAlchemy database models
4. **Schemas** (`schemas/`) - Pydantic validation schemas for request/response
5. **Dependencies** (`dependencies/`) - FastAPI dependencies (auth middleware)
6. **Utils** (`utils/`) - Helper functions (JWT, password hashing, file storage)

**Database Models:**
- `User` - User accounts with JWT authentication
- `SensorReading` - Environmental sensor data (temp, humidity, soil moisture, rainfall)
- `PestDetection` - Pest detection results from image uploads
- `Alert` - System alerts (weather warnings, pest alerts, sensor anomalies)

**Key Design Patterns:**
- **Dependency Injection**: FastAPI's `Depends()` for database sessions and auth
- **Repository Pattern**: Database access through SQLAlchemy ORM
- **Service Layer**: Business logic separated from HTTP layer
- **DTO Pattern**: Pydantic schemas for data validation and serialization

**Authentication Flow:**
1. User registers/logs in → JWT token generated (30-day expiration)
2. Token stored in mobile app via SharedPreferences
3. Protected endpoints require `Authorization: Bearer <token>` header
4. `get_current_user` dependency validates token and retrieves user

**Configuration:**
- All settings managed through `config.py` using pydantic-settings
- Environment variables loaded from `.env` file
- Supports both SQLite (development) and PostgreSQL (production)
- Database URL automatically selected based on `ENVIRONMENT` variable

**Alembic Migrations:**
- Migration files stored in `alembic/versions/`
- `alembic/env.py` connects to database using same config as application
- Auto-generates migrations by comparing models to database schema
- Always review auto-generated migrations before applying

### Mobile Structure

The mobile app uses **Provider** for state management with a feature-based structure:

**Key Directories:**
- `screens/` - Feature-based screen organization (auth/, dashboard/, sensor/, pest/, weather/, alerts/)
- `services/` - API client services (one per feature domain)
- `models/` - Dart data models matching backend schemas
- `widgets/` - Reusable UI components
- `utils/` - Constants, storage helpers (JWT token management)

**API Communication:**
- Services use `http` package for REST API calls
- Base URL configured in `utils/constants.dart`
- Android emulator: Use `http://10.0.2.2:8000` (not localhost)
- iOS simulator: Use `http://localhost:8000`
- Physical device: Use computer's IP address

**State Management:**
- Provider pattern for reactive state updates
- Separate providers planned for: Auth, Sensor, Pest, Weather, Alert
- Providers will handle API calls and state updates

## Important Development Notes

### Database Migrations

**Critical workflow:**
1. **Modify model** in `backend/models/`
2. **Generate migration**: `alembic revision --autogenerate -m "description"`
3. **Review migration file** in `alembic/versions/` - verify upgrade/downgrade logic
4. **Apply migration**: `alembic upgrade head`
5. **Commit migration file** to Git

**Never:**
- Edit already-applied migrations (create new migration instead)
- Delete migrations (breaks revision chain)
- Skip migration review (auto-generate isn't perfect)

### Environment Variables

**Backend requires:**
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - JWT signing key (change in production!)
- `OPENWEATHER_API_KEY` - Weather API key from openweathermap.org
- `ENVIRONMENT` - "development" or "production"

**Mobile configuration:**
- API base URL in `lib/utils/constants.dart`
- Adjust for emulator/simulator/physical device

### Testing Philosophy

**Backend:**
- All new endpoints should have tests in `tests/`
- Test files mirror the structure: `routers/auth.py` → `tests/test_auth.py`
- Use pytest fixtures from `conftest.py` for database setup
- Tests use separate SQLite database (not development database)

**Mobile:**
- Widget tests for UI components
- Unit tests for business logic
- Integration tests for API communication

### External Services

**Weather API (OpenWeatherMap):**
- 7-day forecast via `/api/v1/weather/forecast`
- Cached for 30 minutes in `services/weather_service.py`
- Free tier: 1000 calls/day limit

**ML Service (Pest Detection):**
- Currently using **mock ML service** (random predictions for testing)
- Mock service in `routers/pest.py` returns simulated pest detections
- Real ML model integration planned (or Roboflow as backup)
- Image uploads stored in `backend/uploads/` directory

### Mobile Development Tips

**API Base URLs:**
- **Android Emulator**: `http://10.0.2.2:8000` (10.0.2.2 maps to host machine's localhost)
- **iOS Simulator**: `http://localhost:8000`
- **Physical Device**: Use your computer's IP address (e.g., `http://192.168.1.100:8000`)

**Permissions Required:**
- Android: Camera, Internet (in `android/app/src/main/AndroidManifest.xml`)
- iOS: Camera usage description (in `ios/Runner/Info.plist`)

### File Organization Conventions

**Backend:**
- One router file per feature domain (auth, sensor, pest, weather, alert)
- Routers registered in `main.py` with `/api/v1` prefix
- Services contain business logic; routers handle HTTP concerns only
- All database models inherit from `Base` (defined in `database.py`)

**Mobile:**
- Screens organized by feature (one directory per feature)
- Services mirror backend API structure
- Models use `fromJson`/`toJson` for serialization

## Database Schema Overview

**users table:**
- JWT authentication with 30-day token expiration
- Password hashing with bcrypt
- One-to-many: user → sensor_readings, pest_detections, alerts

**sensor_readings table:**
- Simulated environmental data
- Columns: temperature, humidity, soil_moisture, rainfall, timestamp
- Used for alert threshold checks

**pest_detections table:**
- Image-based pest detection results
- Stores image path, pest type, confidence score, recommendations
- Mock ML predictions until real model integrated

**alerts table:**
- Three types: weather, pest, sensor
- Severity levels: info, warning, critical
- Read/unread tracking per user

## Common Workflows

### Adding a New API Endpoint

1. Define model in `backend/models/` (if new entity)
2. Create Pydantic schemas in `backend/schemas/`
3. Create router in `backend/routers/` with endpoint logic
4. Add business logic to `backend/services/` if needed
5. Register router in `backend/main.py`
6. Generate migration: `alembic revision --autogenerate -m "Add table"`
7. Apply migration: `alembic upgrade head`
8. Write tests in `backend/tests/test_<feature>.py`
9. Update API documentation comments (FastAPI auto-generates from docstrings)

### Adding a New Mobile Screen

1. Create screen file in `mobile/lib/screens/<feature>/`
2. Create service in `mobile/lib/services/` for API calls
3. Create models in `mobile/lib/models/` matching backend schemas
4. Add route in `mobile/lib/main.dart`
5. Create provider if state management needed
6. Write widget tests in `mobile/test/`

### Database Reset (Development Only)

**SQLite:**
```bash
cd backend
rm agrisense.db
alembic upgrade head
python scripts/seed_data.py
```

**PostgreSQL:**
```bash
# Option 1: Reset via Adminer (http://localhost:8080)
# Drop all tables manually

# Option 2: Reset via scripts
cd backend/scripts
# See scripts/README.md for reset scripts
```

## Project Context

**Development Stage:** Phase 0-1 (Backend foundation complete, mobile app skeleton in place)

**Key Documentation:**
- [README.md](README.md) - Project overview and setup
- [backend/README.md](backend/README.md) - Backend details and API reference
- [mobile/README.md](mobile/README.md) - Mobile app setup and structure
- [.references/ALEMBIC_SETUP_GUIDE.md](.references/ALEMBIC_SETUP_GUIDE.md) - Detailed Alembic guide
- [.references/prd/agrisense-prd.md](.references/prd/agrisense-prd.md) - Product requirements
- [.references/tasks/agrisense-tasks.md](.references/tasks/agrisense-tasks.md) - Development tasks

**Git Workflow:**
- Main branch: `main`
- Current working branch: `bryan`
- Commit messages should be clear and descriptive
- Include co-author in commits: `Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>`
