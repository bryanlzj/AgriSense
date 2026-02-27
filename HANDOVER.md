# AgriSense Development Handover Document

> **Date:** 2026-02-27
> **Session Summary:** Linux environment setup + ML deployment planning
> **Previous Session:** YOLOv5 Pest Detection Model Integration
> **Next Session:** Execute ML model deployment plan (6 tasks)

---

## Current Project State

### Infrastructure
- **Backend URL:** `https://agrisense.bryanlzj.work`
- **Database (Adminer):** `https://db.bryanlzj.work`
- **Server Location:** Oracle Cloud at `/opt/agrisense` (24GB RAM, 200GB disk)
- **Deployment:** CI/CD via GitHub Actions (`.github/workflows/deploy.yml`)
- **Database:** PostgreSQL running in Docker on server
- **Dev Environment:** WSL2 Linux (Ubuntu) at `/home/bryan/AgriSense`

### Integration Progress

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1-6 | ✅ Complete | Login, signup, dashboard, weather, alerts, sectors, pest detection, chatbot, polish |
| ML Model Integration | ✅ Complete locally | YOLOv5 pest detection works locally, server still uses mock |
| **ML Model Deployment** | 🔲 Ready to execute | Plan written, 6 tasks to implement |

### Test Coverage

| Type | Count | Coverage | Status |
|------|-------|----------|--------|
| Backend (pytest) | 139 | 77% overall, 92-100% routers | ✅ 122 passed, 1 pre-existing DB error |
| Mobile (flutter test) | 29 | - | ✅ All passing |

---

## What Was Accomplished This Session

### 1. Linux Environment Setup
- Installed `python3.12-venv` package (was missing on Ubuntu)
- Created Python venv at `backend/venv/`
- Installed all requirements from `requirements.txt`
- Discovered `ultralytics` package was missing from requirements (needed by torch.hub's YOLOv5 loader)
- Discovered Pillow auto-upgrades to 12.x which breaks JPEG saving (`ImageFile._Tile` removed)

### 2. Verified ML Model Status
- **Model file exists:** `backend/ml_models/pest_model.pt` (14MB)
- **Model loads successfully:** All 10 classes detected
- **Inference works:** Correctly returns 0 detections on blank image (real inference, not mock)
- **Key finding:** Previous session claimed model worked but `ultralytics` was never added to requirements — model was silently falling back to mock predictions

### 3. ML Deployment Plan Created
- Design doc: `docs/plans/2026-02-25-ml-model-deployment-design.md`
- Implementation plan: `docs/plans/2026-02-25-ml-model-deployment.md`
- Approach: Full PyTorch in Docker (server has plenty of resources)

---

## ML Deployment Plan — Ready to Execute

### Task 1: Fix requirements.txt
- Pin `Pillow>=10.3.0,<13.0.0` (replace `==10.1.0`)
- Add `ultralytics>=8.0.0` and `gitpython>=3.1.30` to ML section

### Task 2: Un-gitignore and commit model file
- Remove `backend/ml_models/*.pt` from `.gitignore`
- Commit `backend/ml_models/pest_model.pt` (14MB, within GitHub 100MB limit)

### Task 3: Update Dockerfile
- Add `libgl1-mesa-glx` and `libglib2.0-0` (OpenCV runtime deps) to both build stages
- Add `RUN python -c "import torch; torch.hub.load(...)"` to pre-cache YOLOv5 repo during build

### Task 4: Update docker-compose.yml
- Change `USE_MOCK_ML` default from `True` to `False`
- Add `PEST_MODEL_PATH: /app/ml_models/pest_model.pt`

### Task 5: Local Docker build test
- `docker compose build backend` — verify image builds
- Check logs show model loading with 10 classes

### Task 6: Deploy to production
- Push to `main` → CI/CD runs tests → deploys to Oracle Cloud
- Verify with `curl https://agrisense.bryanlzj.work/health`

Full details in `docs/plans/2026-02-25-ml-model-deployment.md`.

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

## What's Needed After ML Deployment

### Priority 1: Edit Profile
- **Backend:** Add `PUT /api/v1/auth/me` endpoint to update user profile
- **Mobile:** Create Edit Profile page accessible from Settings
- **Fields to edit:** full_name, farm_location_name, crop_type

### Priority 2: Weather Enhancements
- Historical weather data endpoint (`/weather/historical`)
- Weather by farm sector (requires adding lat/lng to Sector model + migration)

### Priority 3: Other Enhancements (Optional)
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
| POST | `/api/v1/pest/detect` | ✅ Uses real ML locally, mock on server |
| POST | `/api/v1/pest/detect/enhanced` | ✅ Uses real ML locally, mock on server |
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

### Other (All Working)
- `/api/v1/dashboard` — Dashboard data
- `/api/v1/alert/` — Alerts CRUD
- `/api/v1/sector/` — Sectors CRUD
- `/api/v1/chat/` — Chatbot

---

## How to Run

### Backend (Local — Linux/WSL2)
```bash
cd /home/bryan/AgriSense/backend
source venv/bin/activate
python run.py
```

### Run Tests
```bash
cd /home/bryan/AgriSense/backend
source venv/bin/activate
TEST_DATABASE_URL="postgresql://agrisense_user:PwGszJbrHGnxVplLFmjc3X31gtHr412+@168.138.188.113:5432/agrisense" python -m pytest -v
```

### Deployment
Push to `main` branch triggers CI/CD automatically.

---

## Known Issues / Notes

### Dependency Versions
- `ultralytics` auto-installs updated versions of `Pillow`, `requests`, and `gitpython` at runtime via torch.hub — pre-installing them in requirements avoids this
- YOLOv5 torch.hub prints deprecation warnings about `torch.cuda.amp.autocast` — harmless

### .env File
- `USE_MOCK_ML=True` in local `.env` — change to `False` for local ML testing
- `TEST_DATABASE_URL` must be set as env var when running tests (not in .env)

### Pre-existing Test Flake
`test_sensor.py::TestSensorStatistics::test_get_statistics` occasionally errors with `psycopg2.OperationalError: server closed the connection unexpectedly` during teardown. Remote PostgreSQL connection timeout, not a code bug.

### User Preferences
- **"Never use mock data under any circumstances unless I say ok"** — Always use real API data

### Sector Model Limitation
Sector model has NO latitude/longitude. Weather-by-sector requires adding columns + migration.

---

## File Locations Quick Reference

```
AgriSense/
├── backend/
│   ├── main.py              # FastAPI app (loads ML model in lifespan)
│   ├── config.py            # Settings (pest_model_path, use_mock_ml)
│   ├── Dockerfile           # Multi-stage build (needs torch.hub update)
│   ├── requirements.txt     # Dependencies (needs ultralytics, Pillow pin)
│   ├── .env                 # Local env vars
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── routers/
│   │   └── pest.py          # Pest endpoints (ML inference integrated)
│   ├── services/
│   │   └── pest_ml_service.py  # YOLOv5 singleton service
│   ├── ml_models/
│   │   └── pest_model.pt    # YOLOv5 weights (14MB, currently gitignored)
│   ├── venv/                # Python venv (Linux, created this session)
│   └── tests/               # pytest tests (139 tests)
├── mobile/                  # Flutter app
├── docker-compose.yml       # Docker services config
├── docs/plans/
│   ├── 2026-02-25-ml-model-deployment-design.md
│   └── 2026-02-25-ml-model-deployment.md
├── CLAUDE.md                # Project instructions for Claude
└── HANDOVER.md              # This file
```

---

## Contact / Resources

- **API Docs:** https://agrisense.bryanlzj.work/docs
- **GitHub Repo:** Check `.git/config` for remote URL
- **Server Access:** SSH to Oracle Cloud instance
