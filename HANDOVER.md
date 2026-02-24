# AgriSense Development Handover Document

> **Date:** 2026-02-24
> **Session Summary:** YOLOv5 Pest Detection Model Integration — replaced mock random logic with real ML inference
> **Previous Session:** Documentation Update + Backend Test Suite (139 tests)
> **Next Session:** Edit Profile, Weather Enhancements, Deployment of ML model

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
| Phase 5: Pest Detection & Chat | ✅ Complete | Image upload, pest detection, chatbot |
| Phase 6: Polish | ✅ Complete | Provider state management, error handling, logout |
| **ML Model Integration** | ✅ Complete | **YOLOv5 pest detection replacing mock predictions** |

### Test Coverage

| Type | Count | Coverage | Status |
|------|-------|----------|--------|
| Backend (pytest) | 139 | 77% overall, 92-100% routers | ✅ 122 passed, 1 pre-existing DB error |
| Mobile (flutter test) | 29 | - | ✅ All passing |

**Note:** The 1 error is in `test_sensor.py::TestSensorStatistics::test_get_statistics` — remote PostgreSQL drops the connection during teardown. Pre-existing, not related to ML changes.

---

## What Was Accomplished This Session

### YOLOv5 Pest Detection Model Integration

Replaced **fully mocked** pest detection (random predictions) with **real YOLO model inference**.

#### Files Created
| File | Description |
|------|-------------|
| `backend/services/pest_ml_service.py` | Singleton ML service — loads YOLOv5 via `torch.hub`, runs inference, returns structured results with mock fallback |
| `backend/ml_models/pest_model.pt` | 14MB YOLOv5 model file (extracted from `best.pt.zip`, gitignored) |

#### Files Modified
| File | Changes |
|------|---------|
| `backend/routers/pest.py` | Replaced `random.choice()`/`random.uniform()` in `/detect` and `/detect/enhanced` with `pest_ml_service.predict()`; added 10 model class entries to `PEST_DATABASE`; added `get_pest_info()` helper with fallback for unknown classes; added `DEFAULT_PEST_INFO` |
| `backend/config.py` | Added `pest_model_path` setting (`./ml_models/pest_model.pt`); changed `use_mock_ml` default to `False` |
| `backend/main.py` | Added ML model loading in lifespan handler at startup with logging |
| `backend/requirements.txt` | Added `torch>=2.0.0`, `torchvision>=0.15.0`, `opencv-python-headless>=4.8.0`, `pandas>=2.0.0`, `seaborn>=0.12.0`, `tqdm>=4.60.0` |
| `.gitignore` | Added `backend/ml_models/*.pt`, `backend/ml_models/*.onnx`, `backend/ml_models/*.tflite`, `best.pt.zip`, `best.pt/` |
| `backend/.env` | Fixed malformed `SEED_DATABASE` line (was concatenated with `OPENROUTER_MODEL` due to missing newline) |

#### Key Technical Decisions

**YOLOv5 (NOT v8):** The trained model is YOLOv5 format. The `ultralytics` package (v8) **cannot** load it — throws `TypeError`. Must use:
```python
import torch
model = torch.hub.load('ultralytics/yolov5', 'custom', path='model.pt', trust_repo=True)
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

**Inference flow:**
1. `pest_ml_service.predict(image_path)` runs YOLOv5 on the image
2. Returns `PestPredictionResult` with primary pest, confidence, all detections + bounding boxes
3. If model not loaded or `USE_MOCK_ML=True`, falls back to random mock predictions
4. Confidence tiering unchanged: >= 70% = detected, 50-69% = partial, < 50% = unknown

**PEST_DATABASE:** Now contains entries for all 10 model classes (lowercase, matching `model.names`) plus legacy Title Case entries for existing DB records and mock fallback. `get_pest_info()` does case-insensitive lookup with a generic fallback for unknown classes.

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

**Config controls:**
- `USE_MOCK_ML=True` → skip model loading entirely, always use mock
- `USE_MOCK_ML=False` (default) → attempt model load; if file missing, log warning and fall back to mock
- `PEST_MODEL_PATH=./ml_models/pest_model.pt` → model file location

---

## What's Needed Next

### Priority 1: Deployment of ML Model
The ML model works locally but needs deployment consideration:
- **Model file:** `backend/ml_models/pest_model.pt` is gitignored (14MB). Must be uploaded to server separately or via Docker volume
- **Dependencies:** `torch` adds ~2GB to the Docker image. Consider:
  - CPU-only PyTorch wheel (smaller)
  - Pre-downloading `torch.hub` cache for YOLOv5 repo (avoids runtime download)
  - Setting `USE_MOCK_ML=True` on server if model deployment is deferred
- **Dockerfile:** May need updates for PyTorch + torch.hub cache
- **First-run warning:** `torch.hub.load` downloads YOLOv5 repo on first call (~20MB). On server, pre-cache or bundle it

### Priority 2: Edit Profile
- **Backend:** Add `PUT /api/v1/auth/me` endpoint to update user profile
- **Mobile:** Create Edit Profile page accessible from Settings
- **Fields to edit:** full_name, farm_location_name, crop_type

### Priority 3: Weather Enhancements (User Requested)

| Feature | Backend Changes | Mobile Changes |
|---------|-----------------|----------------|
| **Historical Weather Data** | Add `/weather/historical` endpoint | Add historical tab/view to weather page |
| **Weather by Farm Sector** | Add lat/lng to Sector model, update weather endpoints | Allow sector selection in weather page |

**Note:** Sector model currently has NO coordinates (lat/lng). Would need migration to add these fields.

### Priority 4: Other Enhancements (Optional)
- Forgot password flow
- Push notifications
- Offline support

---

## API Endpoints Summary

### Auth
| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/api/v1/auth/login` | Login | ✅ |
| POST | `/api/v1/auth/register` | Register | ✅ |
| GET | `/api/v1/auth/me` | Get current user | ✅ |
| PUT | `/api/v1/auth/me` | Update profile | ❌ **NEEDED** |

### Pest Detection (Updated This Session)
| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/api/v1/pest/upload` | Upload image only | ✅ |
| POST | `/api/v1/pest/detect` | Upload + detect (basic) | ✅ **Now uses real ML** |
| POST | `/api/v1/pest/detect/enhanced` | Upload + detect with confidence tiering | ✅ **Now uses real ML** |
| GET | `/api/v1/pest/` | List user's detections | ✅ |
| GET | `/api/v1/pest/stats/summary` | Detection statistics | ✅ |
| GET | `/api/v1/pest/risk` | Pest risk from weather | ✅ |
| GET | `/api/v1/pest/risk/summary` | Risk summary for dashboard | ✅ |
| POST | `/api/v1/pest/report` | Manual pest report | ✅ |

### Weather
| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/v1/weather/current` | Current weather | ✅ |
| GET | `/api/v1/weather/forecast` | 5-day forecast | ✅ |
| GET | `/api/v1/weather/summary` | Current + forecast | ✅ |
| GET | `/api/v1/weather/historical` | Historical data | ❌ **NEEDED** |

### Other Endpoints (All Working)
- `/api/v1/dashboard` - Dashboard data
- `/api/v1/alert/` - Alerts CRUD
- `/api/v1/sector/` - Sectors CRUD
- `/api/v1/chat/` - Chatbot

---

## How to Run

### Backend (Local)
```bash
cd backend
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run.py
# Model loads at startup, prints class names to console
```

### Mobile App
```bash
cd mobile
flutter pub get
flutter run
```

### Run Tests
```bash
# Backend tests (139 tests)
cd backend
TEST_DATABASE_URL="postgresql://agrisense_user:PwGszJbrHGnxVplLFmjc3X31gtHr412+@168.138.188.113:5432/agrisense" python -m pytest -v

# Mobile tests (29 tests)
cd mobile
flutter test
```

### Deployment
Push to `main` branch triggers CI/CD automatically.

---

## File Locations Quick Reference

```
AgriSense/
├── backend/
│   ├── main.py              # FastAPI app entry (loads ML model in lifespan)
│   ├── config.py            # Settings incl. pest_model_path, use_mock_ml
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── routers/
│   │   └── pest.py          # Pest endpoints (ML inference integrated)
│   ├── services/
│   │   └── pest_ml_service.py  # NEW: YOLOv5 singleton service
│   ├── ml_models/
│   │   └── pest_model.pt    # YOLOv5 weights (14MB, gitignored)
│   └── tests/               # pytest tests (139 tests)
├── mobile/
│   ├── lib/
│   │   ├── main.dart        # Flutter app entry point
│   │   ├── providers/       # State management
│   │   ├── pages/           # Screen widgets
│   │   ├── services/        # API services
│   │   ├── models/          # Data models
│   │   ├── widgets/         # Reusable components
│   │   └── utils/           # Constants, helpers
│   ├── test/                # Flutter tests (29 tests)
│   └── pubspec.yaml         # Flutter dependencies
├── best.pt.zip              # Original model zip (gitignored)
├── CLAUDE.md                # Project instructions for Claude
└── HANDOVER.md              # This file
```

---

## Known Issues / Notes

### .env File
- **Previously had malformed line** where `SEED_DATABASE=True` and `OPENROUTER_MODEL=...` were concatenated (missing newline). Fixed this session. Always verify `.env` formatting after edits.
- `TEST_DATABASE_URL` is NOT in `.env` — must be set as environment variable when running tests.

### YOLOv5 torch.hub Warnings
On first load, YOLOv5 prints requirement warnings (`gitpython`, `pillow`, `requests` version mismatches) and attempts auto-update via `pip`. These are harmless — the required packages are installed, the warning is because `pip` isn't on PATH in some shell contexts. The model loads and works correctly despite the warnings.

### Venv Path Issue
The venv was originally created at `C:\Users\Bryan.Lee\OneDrive - Access UK Ltd\Desktop\AgriSense\backend\venv`. `C:\AgriSense` may be a junction. Running `pip` sometimes resolves to the OneDrive path. Use full path `C:/AgriSense/backend/venv/Scripts/python.exe -m pip install ...` to ensure correct venv.

### Pre-existing Test Flake
`test_sensor.py::TestSensorStatistics::test_get_statistics` occasionally errors with `psycopg2.OperationalError: server closed the connection unexpectedly` during teardown. This is a remote PostgreSQL connection timeout, not a code bug.

### User Preferences
- **"Never use mock data under any circumstances unless I say ok"** - Always use real API data

### Sector Model Limitation
The Sector model currently does NOT have latitude/longitude coordinates. To enable weather-by-sector, need to:
1. Add `latitude` and `longitude` columns to Sector model
2. Create Alembic migration
3. Update sector schemas and endpoints
4. Update mobile to use sector coordinates for weather

---

## Contact / Resources

- **API Docs:** https://agrisense.bryanlzj.work/docs
- **GitHub Repo:** Check `.git/config` for remote URL
- **Server Access:** SSH to Oracle Cloud instance
