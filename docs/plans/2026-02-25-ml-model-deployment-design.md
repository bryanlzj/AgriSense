# ML Model Deployment Design

> **Date:** 2026-02-25
> **Approach:** Full PyTorch in Docker (Approach A)
> **Server:** Oracle Cloud, 24GB RAM, 200GB disk

## Problem

The YOLOv5 pest detection model works locally but the production server still uses mock predictions. The model file is gitignored, dependencies are incomplete, and the Dockerfile doesn't account for PyTorch/torch.hub.

## Design

### 1. Fix Dependencies (`backend/requirements.txt`)

- Add `ultralytics>=8.0.0` (required by torch.hub's YOLOv5 loader)
- Add `gitpython>=3.1.30` (ultralytics dependency, avoids runtime auto-install)
- Pin `Pillow>=10.3.0,<13.0.0` (Pillow 12+ has breaking API change in `ImageFile._Tile`)

### 2. Commit Model File to Git

- Remove `backend/ml_models/*.pt` from `.gitignore`
- Keep `*.onnx` and `*.tflite` ignored
- Commit `backend/ml_models/pest_model.pt` (14MB, within GitHub's 100MB limit)

### 3. Update Dockerfile (`backend/Dockerfile`)

- Pre-cache YOLOv5 torch.hub repo during build to avoid runtime download
- Run a one-time `torch.hub.load()` call in the build step so the container starts with the repo already cached

### 4. Update Docker Compose (`docker-compose.yml`)

- Set `USE_MOCK_ML: "False"`
- Add `PEST_MODEL_PATH: /app/ml_models/pest_model.pt`

### 5. CI/CD (No Changes)

Tests run with `USE_MOCK_ML=True` so they don't need PyTorch or the model. Deploy step (`docker compose up --build`) picks up all changes automatically.

## Files Changed

| File | Change |
|------|--------|
| `backend/requirements.txt` | Add ultralytics, gitpython, pin Pillow |
| `.gitignore` | Remove `backend/ml_models/*.pt` line |
| `backend/Dockerfile` | Add torch.hub pre-cache build step |
| `docker-compose.yml` | Set USE_MOCK_ML=False, add PEST_MODEL_PATH |
