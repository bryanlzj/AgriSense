# AgriSense Development Handover Document

> **Date:** 2026-03-05
> **Session Summary:** SSL fix for mobile app + alerts endpoint bug fix
> **Previous Session:** ML deployment plan creation + Linux env setup
> **Next Session:** Deploy alert fix to production, continue with Priority features

---

## Current Project State

### Infrastructure
- **Backend URL:** `https://agrisense.bryanlzj.work`
- **Database (Adminer):** `https://db.bryanlzj.work`
- **Server Location:** Oracle Cloud at `/opt/agrisense` (24GB RAM, 200GB disk)
- **Deployment:** CI/CD via GitHub Actions (`.github/workflows/deploy.yml`)
- **Database:** PostgreSQL running in Docker on server
- **Dev Environment:** Windows at `C:\AgriSense`, venv at `backend/venv/`

### Integration Progress

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1-6 | ✅ Complete | Login, signup, dashboard, weather, alerts, sectors, pest detection, chatbot, polish |
| ML Model Deployment | ✅ Complete | User deployed ML model to production (6 tasks from plan executed) |
| **SSL Fix (Mobile)** | ✅ Complete locally | Trusted HTTP client added, all services updated |
| **Alerts Bug Fix** | ✅ Complete locally | `alert_metadata` JSON string parsing fixed |
| **Deploy fixes to prod** | 🔲 Not yet | Need to push changes and redeploy |

### Test Coverage

| Type | Count | Coverage | Status |
|------|-------|----------|--------|
| Backend (pytest) | 139 | 77% overall, 92-100% routers | ✅ 122 passed, 1 pre-existing DB error |
| Mobile (flutter test) | 29 | - | ✅ All passing |

---

## What Was Accomplished This Session

### 1. Diagnosed Login Failure on Mobile App
- **Symptom:** User couldn't log in from Flutter app on Android emulator
- **Root cause:** `CERTIFICATE_VERIFY_FAILED: self signed certificate in certificate chain`
- Cloudflare's SSL certificate chain is not trusted by Dart's `http` package on Android emulator
- The server was healthy and credentials were correct (`admin` / `admin123`)
- Verified by testing the production login endpoint directly with curl (works with `--ssl-no-revoke`)

### 2. Created Trusted HTTP Client for Flutter
- **File created:** `mobile/lib/utils/http_client.dart`
- Creates an `IOClient` with `badCertificateCallback` that accepts all certs **in debug mode only**
- In release mode, uses default strict certificate validation
- Singleton `appHttpClient` instance shared across all services

### 3. Updated All Mobile Services to Use Trusted Client
All 7 services updated from `http.get/post/put/delete` to `appHttpClient.get/post/put/delete`:
- `auth_service.dart` — login, register, getCurrentUser
- `alert_service.dart` — all CRUD + bulk + stats
- `chat_service.dart` — sendMessage, sendImage, getStatus
- `dashboard_service.dart` — getDashboard, getQuickDashboard
- `pest_service.dart` — detectPest (MultipartRequest via `appHttpClient.send()`), getDetections, etc.
- `sector_service.dart` — all CRUD + stats
- `weather_service.dart` — getCurrentWeather, getForecast, getSummary

### 4. Fixed Alerts Endpoint 500 Error
- **Symptom:** `GET /api/v1/alert/` returned `Internal Server Error` on both local and production
- **Root cause:** `AlertResponse` schema had `alert_metadata: Optional[dict]` but the database stores it as a `Text` column (JSON string). Pydantic v2 `from_attributes=True` reads the raw string and fails validation: `Input should be a valid dictionary`
- **Fix:** Changed `alert_metadata` type to `Optional[str]` in schema, added `@model_serializer(mode='wrap')` to parse the JSON string to dict during serialization
- **Files changed:**
  - `backend/schemas/alert.py` — type changed + model_serializer added
  - Verified locally: alerts endpoint now returns proper JSON with parsed metadata

### 5. Emulator Troubleshooting
- ADB had broken pipe issues after emulator lost connection
- Cold boot (`-no-snapshot-load`) broke emulator's internet (ICMP blocked, but HTTP worked)
- Normal boot restored network connectivity
- Ping to google.com shows 100% packet loss from emulator, but browser loads pages fine (ICMP blocked, TCP works)

---

## Bugs Found & Fixed This Session

### Bug 1: SSL Certificate Rejection (Mobile)
- **Location:** All mobile services using `http` package
- **Impact:** Cannot connect to production `https://agrisense.bryanlzj.work` from Android emulator
- **Fix:** Created `appHttpClient` with `badCertificateCallback` for debug mode
- **Status:** ✅ Fixed locally, needs deployment (push + rebuild APK)

### Bug 2: Alerts Endpoint 500 Error (Backend)
- **Location:** `backend/schemas/alert.py` → `AlertResponse.alert_metadata`
- **Impact:** `GET /api/v1/alert/` crashes with `ResponseValidationError` — 11 validation errors
- **Fix:** Changed type from `Optional[dict]` to `Optional[str]`, added `@model_serializer` to parse JSON string
- **Status:** ✅ Fixed locally, needs deployment to production

### Bug 3: OpenRouter Model Deprecated
- **Observed in logs:** `OpenRouter API error: 404 - No endpoints found for meta-llama/llama-3.1-8b-instruct:free`
- **Location:** `.env` → `OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free`
- **Impact:** Chatbot AI responses fail
- **Status:** ❌ Not fixed yet — need to update to a working free model

---

## Important Technical Details

### Trusted HTTP Client (`mobile/lib/utils/http_client.dart`)
```dart
// In debug mode: accepts all SSL certificates (Cloudflare workaround)
// In release mode: uses default strict validation
final http.Client appHttpClient = createHttpClient();
```
- Only affects HTTPS connections; local HTTP (`10.0.2.2:8000`) is unaffected
- All services import `package:fyp_prototype/utils/http_client.dart`

### Alert Metadata Serialization (`backend/schemas/alert.py`)
```python
# alert_metadata stored as Text (JSON string) in DB
# model_serializer parses it to dict in API response
@model_serializer(mode='wrap')
def serialize(self, handler):
    data = handler(self)
    if isinstance(data.get('alert_metadata'), str):
        data['alert_metadata'] = json.loads(data['alert_metadata'])
    return data
```

### Database Credentials
- **Only user in DB:** `admin` / `admin123` (ID: 153)
- **DB connection:** `postgresql://agrisense_user:PwGszJbrHGnxVplLFmjc3X31gtHr412+@168.138.188.113:5432/agrisense`

### Mobile Base URL
- Currently set to `production` (`https://agrisense.bryanlzj.work`) in `api_constants.dart:14`
- For local testing: change to `androidEmulator` (`http://10.0.2.2:8000`)
- Backend must run on `0.0.0.0:8000` (not `127.0.0.1`) for emulator access
- `run.py` hardcodes `127.0.0.1` — use `uvicorn main:app --host 0.0.0.0 --port 8000` instead

---

## Architecture: ML Service

```
main.py lifespan
  └─ pest_ml_service.load_model(settings.pest_model_path)
       └─ torch.hub.load('ultralytics/yolov5', 'custom', ...)
       └─ stores model.names → {0: 'rice leaf roller', ...}

routers/pest.py /detect and /detect/enhanced
  └─ pest_ml_service.predict(file_path)
       ├─ model loaded → real YOLO inference → PestPredictionResult
       └─ model not loaded → mock random prediction → PestPredictionResult
```

**Model Classes (10):**
| Index | Class Name | Danger Level |
|-------|------------|-------------|
| 0 | rice leaf roller | Medium |
| 1 | rice leaf caterpillar | Medium |
| 2 | asiatic rice borer | High |
| 3 | rice gall midge | High |
| 4 | brown plant hopper | High |
| 5 | red spider | Medium |
| 6 | corn borer | High |
| 7 | army worm | High |
| 8 | aphids | Low |
| 9 | flea beetle | Low |

**Config controls:**
- `USE_MOCK_ML=True` → skip model loading, always mock
- `USE_MOCK_ML=False` → attempt model load; if missing, fall back to mock
- `PEST_MODEL_PATH=./ml_models/pest_model.pt` → model file location

---

## What's Needed Next

### Immediate: Deploy Fixes to Production
1. Commit the alert schema fix (`backend/schemas/alert.py`)
2. Commit the mobile HTTP client changes (all service files + `http_client.dart`)
3. Push to `main` → CI/CD deploys backend fix
4. Rebuild and test mobile APK against production

### Priority 1: Fix Chatbot (OpenRouter Model)
- Update `OPENROUTER_MODEL` in `.env` and production env to a working free model
- Check https://openrouter.ai/models for available free models

### Priority 2: Edit Profile
- **Backend:** Add `PUT /api/v1/auth/me` endpoint to update user profile
- **Mobile:** Create Edit Profile page accessible from Settings
- **Fields to edit:** full_name, farm_location_name, crop_type

### Priority 3: Weather Enhancements
- Historical weather data endpoint (`/weather/historical`)
- Weather by farm sector (requires adding lat/lng to Sector model + migration)

### Priority 4: Other Enhancements (Optional)
- Forgot password flow
- Push notifications
- Offline support

---

## API Endpoints Summary

### Auth
| Method | Endpoint | Status |
|--------|----------|--------|
| POST | `/api/v1/auth/login` | ✅ |
| POST | `/api/v1/auth/register` | ✅ |
| GET | `/api/v1/auth/me` | ✅ |
| PUT | `/api/v1/auth/me` | ❌ NEEDED |

### Pest Detection
| Method | Endpoint | Status |
|--------|----------|--------|
| POST | `/api/v1/pest/detect` | ✅ ML deployed to production |
| POST | `/api/v1/pest/detect/enhanced` | ✅ ML deployed to production |
| POST | `/api/v1/pest/upload` | ✅ |
| GET | `/api/v1/pest/` | ✅ |
| GET | `/api/v1/pest/stats/summary` | ✅ |
| GET | `/api/v1/pest/risk` | ✅ |
| GET | `/api/v1/pest/risk/summary` | ✅ |
| POST | `/api/v1/pest/report` | ✅ |

### Weather
| Method | Endpoint | Status |
|--------|----------|--------|
| GET | `/api/v1/weather/current` | ✅ |
| GET | `/api/v1/weather/forecast` | ✅ |
| GET | `/api/v1/weather/summary` | ✅ |
| GET | `/api/v1/weather/historical` | ❌ NEEDED |

### Alerts
| Method | Endpoint | Status |
|--------|----------|--------|
| GET | `/api/v1/alert/` | ⚠️ Fixed locally, 500 on production (needs deploy) |
| GET | `/api/v1/alert/{id}` | ⚠️ Same issue |
| PUT | `/api/v1/alert/{id}` | ✅ |
| DELETE | `/api/v1/alert/{id}` | ✅ |
| PUT | `/api/v1/alert/bulk` | ✅ |
| GET | `/api/v1/alert/stats/summary` | ✅ |

### Other (All Working)
- `/api/v1/dashboard` — Dashboard data
- `/api/v1/sector/` — Sectors CRUD
- `/api/v1/chat/` — ⚠️ Chatbot broken (OpenRouter model 404)

---

## How to Run

### Backend (Local — Windows)
```bash
cd C:\AgriSense\backend
# Must use 0.0.0.0 for emulator access (run.py hardcodes 127.0.0.1)
C:\AgriSense\backend\venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Mobile (Flutter)
```bash
cd C:\AgriSense\mobile
flutter run
# Ensure baseUrl in api_constants.dart points to correct server
# Production: https://agrisense.bryanlzj.work
# Local (emulator): http://10.0.2.2:8000
```

### Run Tests
```bash
cd C:\AgriSense\backend
SET TEST_DATABASE_URL=postgresql://agrisense_user:PwGszJbrHGnxVplLFmjc3X31gtHr412+@168.138.188.113:5432/agrisense
C:\AgriSense\backend\venv\Scripts\python.exe -m pytest -v
```

### Deployment
Push to `main` branch triggers CI/CD automatically.

---

## Known Issues / Notes

### Cloudflare SSL + Android Emulator
- Cloudflare's SSL cert chain is rejected by Dart's `http` package: `CERTIFICATE_VERIFY_FAILED: self signed certificate in certificate chain`
- Same issue on Windows `curl`: `CRYPT_E_NO_REVOCATION_CHECK`
- **Workaround:** Custom `appHttpClient` with `badCertificateCallback` in debug mode
- This is a Cloudflare certificate chain issue, not a device issue
- Production release APK should be tested to confirm it works (release mode uses strict validation)

### Android Emulator Network
- `ping` from emulator always shows 100% packet loss (ICMP blocked) — this is normal
- HTTP/HTTPS works fine (browser loads pages, API calls work)
- Cold boot (`-no-snapshot-load`) can break emulator networking — use normal boot

### Dependency Versions
- `ultralytics` auto-installs updated versions of `Pillow`, `requests`, and `gitpython` at runtime via torch.hub
- YOLOv5 torch.hub prints deprecation warnings about `torch.cuda.amp.autocast` — harmless

### .env File
- `USE_MOCK_ML=True` in local `.env` — change to `False` for local ML testing
- `TEST_DATABASE_URL` must be set as env var when running tests (not in .env)
- `OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free` — BROKEN, needs update

### Pre-existing Test Flake
`test_sensor.py::TestSensorStatistics::test_get_statistics` occasionally errors with `psycopg2.OperationalError: server closed the connection unexpectedly` during teardown. Remote PostgreSQL connection timeout, not a code bug.

### User Preferences
- **"Never use mock data under any circumstances unless I say ok"** — Always use real API data

### Sector Model Limitation
Sector model has NO latitude/longitude. Weather-by-sector requires adding columns + migration.

---

## Files Changed This Session

```
Mobile (Flutter):
├── lib/utils/http_client.dart          # NEW — Trusted HTTP client for Cloudflare SSL
├── lib/utils/api_constants.dart        # baseUrl = production (was already)
├── lib/services/auth_service.dart      # Uses appHttpClient + debug logging
├── lib/services/alert_service.dart     # Uses appHttpClient
├── lib/services/chat_service.dart      # Uses appHttpClient
├── lib/services/dashboard_service.dart # Uses appHttpClient
├── lib/services/pest_service.dart      # Uses appHttpClient (incl. MultipartRequest)
├── lib/services/sector_service.dart    # Uses appHttpClient
└── lib/services/weather_service.dart   # Uses appHttpClient

Backend (FastAPI):
├── schemas/alert.py                    # alert_metadata: Optional[str] + model_serializer
└── models/alert.py                     # No changes (reverted attempted hybrid_property)
```

---

## File Locations Quick Reference

```
AgriSense/
├── backend/
│   ├── main.py              # FastAPI app (loads ML model in lifespan)
│   ├── config.py            # Settings (pest_model_path, use_mock_ml)
│   ├── Dockerfile           # Multi-stage build
│   ├── requirements.txt     # Dependencies
│   ├── .env                 # Local env vars
│   ├── models/
│   │   └── alert.py         # Alert model (alert_metadata is Text column)
│   ├── schemas/
│   │   └── alert.py         # Alert schema (model_serializer parses JSON)
│   ├── routers/
│   │   └── pest.py          # Pest endpoints (ML inference integrated)
│   ├── services/
│   │   └── pest_ml_service.py  # YOLOv5 singleton service
│   ├── ml_models/
│   │   └── pest_model.pt    # YOLOv5 weights (14MB)
│   ├── venv/                # Python venv (Windows)
│   └── tests/               # pytest tests (139 tests)
├── mobile/
│   └── lib/
│       ├── utils/
│       │   ├── api_constants.dart  # Base URL config
│       │   └── http_client.dart    # Trusted HTTP client (NEW)
│       └── services/           # All use appHttpClient now
├── docker-compose.yml       # Docker services config
├── CLAUDE.md                # Project instructions for Claude
└── HANDOVER.md              # This file
```

---

## Contact / Resources

- **API Docs:** https://agrisense.bryanlzj.work/docs
- **GitHub Repo:** Check `.git/config` for remote URL
- **Server Access:** SSH to Oracle Cloud instance
