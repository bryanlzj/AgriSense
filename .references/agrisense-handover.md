# AgriSense - Session Handover Document

**Last Updated:** January 10, 2026
**Current Branch:** `bryan`
**Purpose:** Continue development in a new Claude Code session

---

## Quick Start for New Session

Say: *"Continue from the handover document at `.references/agrisense-handover.md`. First task: debug and fix pytest errors."*

---

## Current Session Progress

### Completed This Session

1. **Test Infrastructure Updated**
   - `backend/tests/conftest.py` - Updated with:
     - New User model fields (full_name, farm_location_name, lat/lng, crop_type)
     - Transaction rollback approach (non-destructive to existing data)
     - New fixture: `test_pest_weather_correlation`
     - Database URL corrected: `agrisense_dev_password_123`

2. **Test Files Created/Updated**
   | File | Status | Notes |
   |------|--------|-------|
   | `test_auth.py` | Updated | New registration fields |
   | `test_alert.py` | Updated | Added `is_acknowledged` field |
   | `test_pest.py` | **NEW** | Comprehensive pest tests |
   | `test_weather.py` | **NEW** | Weather endpoint tests |
   | `test_chat.py` | **NEW** | Chatbot tests |
   | `test_dashboard.py` | **NEW** | Dashboard tests |

3. **Bug Fixes Applied**
   - `backend/models/alert.py` - Added missing `is_acknowledged` column
   - `backend/routers/alert.py` - Fixed statistics query for `is_acknowledged`
   - `backend/.env` - Fixed DATABASE_URL password mismatch

4. **Environment Files Reviewed**
   - All required variables have values
   - API keys have placeholders (need real keys for full functionality)

---

## Immediate Next Steps

### 1. Fix pytest Errors (Priority)

Tests are showing ERROR status (setup/collection errors). Run:
```bash
cd backend
python -m pytest tests/test_auth.py -v
```

**Known issues to investigate:**
- Fixture/import problems
- PestDetection model field names (`confidence_score` vs `confidence`, `image_url` vs `image_path`)
- `test_chat.py:217` has invalid `headers_override` parameter

### 2. API Keys Needed

| Key | Purpose | Get From |
|-----|---------|----------|
| `OPENWEATHER_API_KEY` | Weather features | https://openweathermap.org/api |
| `OPENROUTER_API_KEY` | AI/Chat features | https://openrouter.ai/keys |

Without these, weather and AI features will fail or use mocks.

---

## Project Phase Status

| Phase | Status | Notes |
|-------|--------|-------|
| Phase 0: Setup | Complete | Git, folders, README |
| Phase 1: Backend Foundation | Complete | Auth, Sensor, Pest, Weather, Alerts |
| Phase 1A: Infrastructure | Complete | Docker, env files, migrations |
| Phase 1B: Backend Mods (PRD v2) | Complete | User model, Pest detection, Alerts |
| Phase 1C: New Features | **In Progress** | See remaining tasks below |
| Phase 1D: ML Service | **On Hold** | Waiting for ML framework decision |
| Phase 2: Mobile (Flutter) | **On Hold** | Waiting for teammate's code import |
| Phase 3: Testing & Deployment | Pending | |

### Phase 1C Remaining Tasks

- [ ] 1C.1: Pest Reports table & endpoints
- [ ] 1C.3.2: Update weather service to use database cache
- [ ] 1C.4: Pest Risk Prediction service & endpoint
- [ ] 1C.5: AI Service (OpenRouter integration)
- [ ] 1C.6: Chatbot endpoints
- [ ] 1C.7: Enhanced Dashboard endpoint
- [ ] 1C.8: Background Jobs setup

**Full task breakdown:** `.claude/plans/humming-baking-meerkat.md`

---

## Key Files Reference

### Configuration
```
backend/.env              # Backend environment variables
backend/config.py         # Settings with pydantic-settings
docker-compose.yml        # PostgreSQL + Adminer services
```

### Database
- Host: `localhost:5432`
- Database: `agrisense`
- User: `agrisense_user`
- Password: `agrisense_dev_password_123`

### Test Files
```
backend/tests/
├── conftest.py          # Fixtures (updated)
├── test_auth.py         # Auth tests (updated)
├── test_alert.py        # Alert tests (updated)
├── test_pest.py         # Pest tests (NEW)
├── test_weather.py      # Weather tests (NEW)
├── test_chat.py         # Chat tests (NEW)
├── test_dashboard.py    # Dashboard tests (NEW)
└── test_sensor.py       # Sensor tests (existing)
```

---

## Common Commands

```bash
# Start database (if not running via Rancher)
docker compose up postgres adminer -d

# Run backend
cd backend && python run.py

# Run all tests
cd backend && python -m pytest -v

# Run specific test file
cd backend && python -m pytest tests/test_auth.py -v

# Apply migrations
cd backend && alembic upgrade head

# Database UI
http://localhost:8080
# Server: postgres, User: agrisense_user, Pass: agrisense_dev_password_123, DB: agrisense
```

---

## Uncommitted Changes

**Modified files:**
- `backend/.env.example`, `backend/Dockerfile`, `backend/config.py`
- `backend/db_init.py`, `backend/models/alert.py`, `backend/models/user.py`
- `backend/routers/auth.py`, `backend/routers/pest.py`
- `backend/schemas/alert.py`, `backend/schemas/auth.py`, `backend/schemas/pest.py`
- `backend/utils/security.py`, `docker-compose.yml`

**New files (untracked):**
- `.claude/`, `.env.example`, `.references/prd/agrisense-prd-v2.md`
- `backend/alembic/versions/20260109_*.py` (3 migration files)
- `backend/models/pest_weather_correlation.py`, `backend/models/weather_cache.py`
- `backend/tests/test_chat.py`, `test_dashboard.py`, `test_pest.py`, `test_weather.py`

**Consider committing** before starting new work.

---

## Project Context

### What is AgriSense?
A Final Year Project (FYP) - proof-of-concept mobile app providing early warning for weather threats and pest risks to Malaysian rice farmers.

### Tech Stack
| Component | Technology |
|-----------|------------|
| Backend | FastAPI (Python 3.10+) |
| Database | PostgreSQL |
| Mobile | Flutter (teammate building) |
| Weather API | OpenWeatherMap |
| AI/Recommendations | OpenRouter API |
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
- **Plan File:** `.claude/plans/humming-baking-meerkat.md`
- **Project Guide:** `CLAUDE.md`

---

**End of Handover Document**
