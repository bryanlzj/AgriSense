# AgriSense - Session Handover Document

**Last Updated:** January 10, 2026
**Current Branch:** `bryan`
**Purpose:** Continue development in a new Claude Code session

---

## Quick Start for New Session

Say: *"Continue from the handover document at `.references/agrisense-handover.md`"*

### Environment Setup (Do This First!)

```bash
# 1. Start PostgreSQL
docker compose up postgres -d

# 2. Activate virtual environment
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install dependencies (IMPORTANT - don't skip this!)
pip install -r requirements.txt

# 4. Run migrations
alembic upgrade head

# 5. Run tests to verify everything works
python -m pytest -v
```

---

## Current Project Status

### All Tests Passing: 118/118

| Test File | Tests | Status |
|-----------|-------|--------|
| test_auth.py | 11 | ✅ Pass |
| test_alert.py | 17 | ✅ Pass |
| test_chat.py | 15 | ✅ Pass |
| test_dashboard.py | 15 | ✅ Pass |
| test_pest.py | 26 | ✅ Pass |
| test_sensor.py | 14 | ✅ Pass |
| test_weather.py | 17 | ✅ Pass |

---

## Project Phase Status

| Phase | Status | Notes |
|-------|--------|-------|
| Phase 0: Setup | ✅ Complete | Git, folders, README |
| Phase 1: Backend Foundation | ✅ Complete | Auth, Sensor, Pest, Weather, Alerts |
| Phase 1A: Infrastructure | ✅ Complete | Docker, env files, migrations |
| Phase 1B: Backend Mods (PRD v2) | ✅ Complete | User model, Pest detection, Alerts |
| Phase 1C: New Features | ✅ Complete | All features implemented & tested |
| Phase 1D: ML Service | **On Hold** | Waiting for ML framework decision |
| Phase 2: Mobile (Flutter) | **On Hold** | Waiting for teammate's code import |
| Phase 3: Testing & Deployment | **Pending** | |

### Phase 1C Tasks (All Complete)

- [x] 1C.1: Pest Reports table & endpoints
- [x] 1C.3.2: Weather service (using WeatherAPI.com)
- [x] 1C.4: Pest Risk Prediction service & endpoint
- [x] 1C.5: AI Service (OpenRouter with x-ai/grok-4.1-fast)
- [x] 1C.6: Chatbot endpoints
- [x] 1C.7: Enhanced Dashboard endpoint
- [x] 1C.8: Background Jobs (apscheduler)

---

## Configuration Summary

### Database
- Host: `localhost:5432`
- Database: `agrisense`
- User: `agrisense_user`
- Password: `strongpassword`

### API Keys (configured in backend/.env)

| Service | Variable | Status |
|---------|----------|--------|
| WeatherAPI.com | `WEATHERAPI_KEY` | ✅ Configured |
| OpenRouter AI | `OPENROUTER_API_KEY` | ✅ Configured |

### Key Configuration Changes Made

1. **Passwords standardized** to `strongpassword` across all config files
2. **Weather API** switched from OpenWeatherMap to WeatherAPI.com
3. **AI Model** set to `x-ai/grok-4.1-fast` for OpenRouter

---

## Key Files Reference

### Configuration
```
backend/.env              # Backend environment variables
backend/config.py         # Settings with pydantic-settings
docker-compose.yml        # PostgreSQL + Adminer services
.env                      # Root env (for docker-compose)
```

### Test Files
```
backend/tests/
├── conftest.py          # Fixtures
├── test_auth.py         # Auth tests
├── test_alert.py        # Alert tests
├── test_chat.py         # Chat tests
├── test_dashboard.py    # Dashboard tests
├── test_pest.py         # Pest tests
├── test_sensor.py       # Sensor tests
└── test_weather.py      # Weather tests
```

---

## Common Commands

```bash
# Start database
docker compose up postgres adminer -d

# Run backend
cd backend && python run.py

# Run all tests
cd backend && python -m pytest -v

# Run specific test file
cd backend && python -m pytest tests/test_auth.py -v

# Apply migrations
cd backend && alembic upgrade head

# Database UI (Adminer)
http://localhost:8080
# Server: postgres, User: agrisense_user, Pass: strongpassword, DB: agrisense

# API Documentation
http://localhost:8000/docs
```

---

## Recent Bug Fixes (This Session)

1. **Pest Router Route Ordering** - Moved `/{detection_id}` routes to end of file to prevent matching before static routes like `/risk`, `/reports`

2. **Dashboard Router Field Names** - Fixed `PestDetection.created_at` → `detected_at`, `alert.type` → `alert.alert_type.value`

3. **Chat Tests** - Fixed response key `"response"` → `"message"`, fixed image tests to use JSON with `image_url` instead of file upload

---

## Project Context

### What is AgriSense?
A Final Year Project (FYP) - proof-of-concept mobile app providing early warning for weather threats and pest risks to Malaysian rice farmers.

### Tech Stack
| Component | Technology |
|-----------|------------|
| Backend | FastAPI (Python 3.12) |
| Database | PostgreSQL |
| Mobile | Flutter (teammate building) |
| Weather API | WeatherAPI.com |
| AI/Recommendations | OpenRouter API (x-ai/grok-4.1-fast) |
| ML Models | TBD (teammate building) |

### Key Design Decisions
- JWT tokens expire in 7 days
- Weather cache: 30 minutes
- Pest detection confidence tiers: >=70% (success), 50-69% (partial), <50% (unknown)
- 3 retry attempts before offering manual report
- No push notifications - in-app alerts only

---

## Reference Documents

- **PRD v2:** `.references/prd/agrisense-prd-v2.md`
- **Task List:** `.references/tasks/agrisense-tasks.md`
- **Project Guide:** `CLAUDE.md`

---

**End of Handover Document**
