# AgriSense Development Handover Document

> **Date:** 2026-02-02
> **Session Summary:** Completed Phases 1-4 of backend-mobile integration
> **Next Session:** Continue with Phase 5 (Pest Detection & Chat) or Phase 6 (Polish)

---

## Current Project State

### Infrastructure
- **Backend URL:** `https://agrisense.bryanlzj.work`
- **Database (Adminer):** `https://db.bryanlzj.work`
- **Server Location:** Oracle Cloud at `/opt/agrisense`
- **Deployment:** CI/CD via GitHub Actions (`.github/workflows/deploy.yml`)
- **Database:** PostgreSQL running in Docker on server

### Integration Progress

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1: Foundation | ✅ Complete | Login working end-to-end |
| Phase 2: Sign Up & Dashboard | ✅ Complete | Registration with farm details, dashboard shows real data |
| Phase 3: Weather & Alerts | ✅ Complete | Weather page, alerts page with real API data |
| Phase 4: Farm Sectors | ✅ Complete | CRUD for farm sectors (backend + mobile) |
| Phase 5: Pest Detection & Chat | 🔴 Not Started | Image upload, pest detection, chatbot |
| Phase 6: Polish | 🔴 Not Started | Provider state management, error handling |

---

## Files Created/Modified This Session

### Backend Files

**New Files:**
- `backend/models/sector.py` - Sector database model
- `backend/schemas/sector.py` - Pydantic schemas for sector API
- `backend/routers/sector.py` - CRUD endpoints for sectors

**Modified Files:**
- `backend/models/__init__.py` - Added Sector export
- `backend/models/user.py` - Added sectors relationship
- `backend/main.py` - Registered sector router
- `backend/services/weather_service.py` - Added comprehensive WMO weather codes (0-99)
- `backend/routers/dashboard.py` - Fixed `.humidity` to `.relative_humidity`
- `backend/routers/weather.py` - Fixed `.humidity` to `.relative_humidity`
- `backend/jobs/scheduler.py` - Fixed `.humidity` to `.relative_humidity`
- `backend/services/chat_service.py` - Fixed `.humidity` to `.relative_humidity`

### Mobile Files

**New Files:**
- `mobile/lib/services/sector_service.dart` - API service for sectors
- `mobile/lib/services/weather_service.dart` - Weather API service
- `mobile/lib/services/alert_service.dart` - Alerts API service
- `mobile/lib/services/dashboard_service.dart` - Dashboard API service
- `mobile/lib/pages/alerts_page.dart` - Full alerts management UI

**Modified Files:**
- `mobile/lib/utils/api_constants.dart` - Added sector endpoints, uses production URL
- `mobile/lib/models/farm_sector.dart` - Added id, fromJson, toJson
- `mobile/lib/models/weather_data.dart` - Updated to match backend response
- `mobile/lib/models/alert.dart` - Updated with proper fields
- `mobile/lib/models/risk_status.dart` - Updated to match backend
- `mobile/lib/models/home_page_data.dart` - Updated for dashboard integration
- `mobile/lib/pages/farm_management_page.dart` - Uses real SectorService
- `mobile/lib/pages/weather_page.dart` - Full weather UI with forecast
- `mobile/lib/pages/home_page.dart` - Connected to dashboard API
- `mobile/lib/pages/main_page.dart` - Fetches real dashboard data
- `mobile/lib/pages/sign_up_page.dart` - Added farm location, crop type
- `mobile/lib/main.dart` - Added routes for alerts page

---

## API Endpoints Summary

### Sector Endpoints (New)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/sector/` | Create sector |
| GET | `/api/v1/sector/` | List user's sectors |
| GET | `/api/v1/sector/{id}` | Get specific sector |
| PUT | `/api/v1/sector/{id}` | Update sector |
| DELETE | `/api/v1/sector/{id}` | Delete sector |
| GET | `/api/v1/sector/stats/summary` | Get sector statistics |

### Other Key Endpoints
- `POST /api/v1/auth/login` - Login (username, not email)
- `POST /api/v1/auth/register` - Register with farm details
- `GET /api/v1/dashboard` - Full dashboard data
- `GET /api/v1/weather/summary` - Weather with forecast
- `GET /api/v1/alert/` - List alerts (note trailing slash)
- `PUT /api/v1/alert/{id}` - Update alert (mark read)

---

## Known Issues / Notes

### Resolved Issues
1. **Weather "Unknown" condition** - Added WMO codes 0-99 to `weather_service.py`
2. **Alert API failing** - Fixed by adding trailing slash to endpoint
3. **`.humidity` attribute error** - Changed to `.relative_humidity` in 4 files
4. **Weather page overflow** - Fixed with SafeArea and Expanded widgets
5. **Time format wrong** - Fixed to show local time with date

### Current State
- All Phase 1-4 features are deployed and working
- Sectors table exists in production database (empty, ready for use)
- Mobile app connects to production backend at `agrisense.bryanlzj.work`

### User Preferences
- **"Never use mock data under any circumstances unless I say ok"** - Always use real API data

---

## How to Run

### Android Emulator
```bash
# List available emulators
emulator -list-avds

# Start emulator (existing one)
emulator -avd Medium_Phone_API_36.1

# Run Flutter app
cd mobile
flutter run -d emulator-5554

# Hot reload: press 'r' in terminal
# Quit: press 'q' in terminal
```

### Chrome (Alternative)
```bash
cd mobile
flutter run -d chrome
```

### Backend (Local Development)
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run.py
```

### Deployment
Push to `main` branch triggers CI/CD:
- Builds Docker image
- Deploys to Oracle Cloud server
- Runs migrations automatically

---

## Next Steps (Phase 5: Pest Detection & Chat)

### Tasks from INTEGRATION_PLAN.md
1. Add `image_picker` package to pubspec.yaml
2. Create `lib/services/pest_service.dart`
3. Build pest detection UI (capture/upload image)
4. Display detection results
5. Create `lib/services/chat_service.dart`
6. Update `chatbot_page.dart` to send/receive messages
7. Test pest detection flow
8. Test chatbot flow

### Backend Endpoints Already Available
- `POST /api/v1/pest/detect` - Upload & detect pests
- `GET /api/v1/pest/` - List pest detections
- `POST /api/v1/chat/message` - Send message to AI chatbot

---

## File Locations Quick Reference

```
AgriSense/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── routers/             # API endpoints
│   ├── services/            # Business logic
│   └── alembic/             # Database migrations
├── mobile/
│   ├── lib/
│   │   ├── main.dart        # Flutter app entry point
│   │   ├── pages/           # Screen widgets
│   │   ├── services/        # API services
│   │   ├── models/          # Data models
│   │   ├── widgets/         # Reusable components
│   │   └── utils/           # Constants, helpers
│   └── pubspec.yaml         # Flutter dependencies
├── INTEGRATION_PLAN.md      # Detailed integration roadmap
├── CLAUDE.md                # Project instructions for Claude
└── HANDOVER.md              # This file
```

---

## Database Schema (Key Tables)

- `users` - User accounts with farm location and crop type
- `sectors` - Farm sectors/plots (NEW - Phase 4)
- `sensor_readings` - Environmental sensor data
- `pest_detections` - Pest detection results
- `alerts` - System alerts (weather, pest, etc.)
- `alembic_version` - Migration tracking

---

## Contact / Resources

- **API Docs:** https://agrisense.bryanlzj.work/docs
- **GitHub Repo:** Check `.git/config` for remote URL
- **Server Access:** SSH to Oracle Cloud instance
