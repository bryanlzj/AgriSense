# AgriSense

**IoT-Driven Agricultural Monitoring System for Malaysian Farmers**

> **Personal Learning Project**
> A capstone project focused on learning full-stack mobile development (Flutter + FastAPI) with AI assistance. Built as a simulation-based system for educational purposes - no physical hardware required.

AgriSense is a mobile application that helps farmers monitor their crops through AI-powered pest detection, environmental monitoring, and weather forecasting.

---

## Project Overview

AgriSense provides farmers with:
- **AI Pest Detection** - Upload crop images to identify pest infestations
- **Environmental Monitoring** - Track temperature, humidity, and soil moisture
- **Weather Forecasting** - 7-day weather predictions with alerts
- **Smart Alerts** - Notifications for pest risks and weather warnings
- **AI Chatbot** - Get farming recommendations via chat
- **Historical Data** - View trends and past detections

**Note:** This is a simulation-based system using synthetic sensor data - no physical IoT hardware required.

---

## Technology Stack

### Backend
| Component | Technology |
|-----------|------------|
| Framework | FastAPI (Python 3.10+) |
| Database | PostgreSQL 15 |
| Authentication | JWT (7-day expiration) |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Background Jobs | APScheduler |
| API Docs | Swagger UI (auto-generated) |

### Mobile App
| Component | Technology |
|-----------|------------|
| Framework | Flutter (Dart) |
| State Management | Provider |
| HTTP Client | http package |
| Storage | SharedPreferences |
| Platforms | Android & iOS |

### External Services
| Service | Provider |
|---------|----------|
| Weather API | WeatherAPI.com |
| AI/Recommendations | OpenRouter API (Grok model) |
| ML Service | Mock service (real model TBD) |

---

## Project Structure

```
AgriSense/
├── backend/                 # FastAPI backend
│   ├── alembic/            # Database migrations
│   ├── dependencies/       # FastAPI dependencies (auth)
│   ├── jobs/               # Background scheduled jobs
│   ├── models/             # SQLAlchemy models
│   ├── routers/            # API endpoints
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   ├── tests/              # Backend tests (118 tests)
│   ├── utils/              # Helper functions
│   ├── config.py           # Settings configuration
│   ├── database.py         # Database connection
│   ├── main.py             # FastAPI application
│   ├── run.py              # Development server
│   └── requirements.txt    # Python dependencies
│
├── mobile/                 # Flutter mobile app
│   ├── lib/
│   │   ├── models/         # Data models
│   │   ├── screens/        # UI screens
│   │   ├── services/       # API services
│   │   ├── utils/          # Helper functions
│   │   ├── widgets/        # Reusable widgets
│   │   └── main.dart       # App entry point
│   └── pubspec.yaml        # Flutter dependencies
│
├── .references/            # Project documentation
│   ├── prd/                # Product Requirements Document
│   └── tasks/              # Task tracking
│
├── docker-compose.yml      # Docker services
├── CLAUDE.md               # Development guide
└── README.md               # This file
```

---

## Quick Start

### Prerequisites

- **Python 3.10+** - https://www.python.org/downloads
- **Docker Desktop** - https://www.docker.com/products/docker-desktop
- **Flutter SDK 3.0+** - https://docs.flutter.dev/get-started/install
- **Git** - https://git-scm.com/downloads

### 1. Clone Repository

```bash
git clone <repository-url>
cd AgriSense
```

### 2. Start Database

```bash
docker compose up postgres adminer -d
```

### 3. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy environment file and configure
cp .env.example .env
# Edit .env with your API keys (see Environment Variables section)

# Run database migrations
alembic upgrade head

# Start server
python run.py
```

### 4. Verify Setup

```bash
# Run tests (should pass 118/118)
python -m pytest -v
```

### 5. Access Points

| Service | URL |
|---------|-----|
| Backend API | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |
| Database UI (Adminer) | http://localhost:8080 |

**Adminer Login:**
- Server: `postgres`
- Username: `agrisense_user`
- Password: `strongpassword`
- Database: `agrisense`

---

## Environment Variables

Create `backend/.env` from `.env.example`:

```env
# Database
DATABASE_URL=postgresql://agrisense_user:strongpassword@localhost:5432/agrisense

# Authentication (generate with: openssl rand -hex 32)
SECRET_KEY=your-secret-key-change-in-production

# Weather API (get from https://www.weatherapi.com)
WEATHERAPI_KEY=your_weatherapi_key_here

# AI Service (get from https://openrouter.ai/keys)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Development settings
ENVIRONMENT=development
SEED_DATABASE=True
USE_MOCK_ML=True
```

---

## Mobile Setup

```bash
cd mobile

# Install dependencies
flutter pub get

# Run on emulator/device
flutter run
```

**API Base URL Configuration:**
- Android Emulator: `http://10.0.2.2:8000`
- iOS Simulator: `http://localhost:8000`
- Physical Device: Use your computer's IP (e.g., `http://192.168.1.x:8000`)

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login and get JWT token |
| GET | `/api/v1/auth/me` | Get current user profile |

### Sensors
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/sensors/current` | Get current sensor readings |
| GET | `/api/v1/sensors/history` | Get historical sensor data |
| POST | `/api/v1/sensors/readings` | Submit sensor reading |

### Pest Detection
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/pest/detect` | Upload image for pest detection |
| GET | `/api/v1/pest/history` | Get detection history |
| GET | `/api/v1/pest/risk` | Get pest risk prediction |
| POST | `/api/v1/pest/reports` | Submit manual pest report |

### Weather
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/weather/current` | Get current weather |
| GET | `/api/v1/weather/forecast` | Get 7-day forecast |

### Alerts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/alerts` | Get user alerts |
| PUT | `/api/v1/alerts/{id}/read` | Mark alert as read |
| PUT | `/api/v1/alerts/{id}/acknowledge` | Acknowledge alert |

### Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/chat` | Send message to AI chatbot |
| GET | `/api/v1/chat/history` | Get chat history |

### Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/dashboard/summary` | Get dashboard summary |

---

## Testing

### Backend Tests
```bash
cd backend

# Run all tests
python -m pytest -v

# Run with coverage
python -m pytest --cov=. --cov-report=html

# Run specific test file
python -m pytest tests/test_auth.py -v
```

### Test User (Auto-seeded)
When `SEED_DATABASE=True`:
- Email: `test@example.com`
- Password: `password123`

---

## Docker Deployment

### Full Stack
```bash
docker compose up -d
```

### Database Only
```bash
docker compose up postgres adminer -d
```

### Stop Services
```bash
docker compose down
```

---

## Development Status

### Phase Status
| Phase | Status |
|-------|--------|
| Phase 0: Setup | Complete |
| Phase 1: Backend Foundation | Complete |
| Phase 1A: Infrastructure | Complete |
| Phase 1B: Backend Modifications | Complete |
| Phase 1C: New Features | Complete |
| Phase 1D: ML Service | On Hold |
| Phase 2: Mobile (Flutter) | In Progress |
| Phase 3: Testing & Deployment | Pending |

### Test Coverage
- **118 tests passing**
- Auth, Sensors, Pest Detection, Weather, Alerts, Chat, Dashboard

---

## Documentation

| Document | Location |
|----------|----------|
| Development Guide | `CLAUDE.md` |
| Project Handover | `.references/agrisense-handover.md` |
| Product Requirements | `.references/prd/agrisense-prd-v2.md` |
| Task Tracking | `.references/tasks/agrisense-tasks.md` |
| API Documentation | http://localhost:8000/docs |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 5432 in use | Stop existing PostgreSQL or change port in docker-compose.yml |
| Database connection failed | Ensure Docker is running: `docker compose up postgres -d` |
| Tests failing | Apply migrations: `alembic upgrade head` |
| Module not found | Activate venv and reinstall: `pip install -r requirements.txt` |

---

## Team

**Project Type:** Final Year Capstone Project (Bachelor of Software Engineering)

- Integration Lead - Backend, Mobile, ML Integration
- ML Team - Pest detection model training

---

## License

This project is developed for educational purposes as part of a Bachelor of Software Engineering capstone project.

---

**Built for Malaysian farmers**
