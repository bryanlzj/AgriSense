# ML Model Deployment Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Deploy the YOLOv5 pest detection model to production so the hosted backend uses real ML inference instead of mock predictions.

**Architecture:** Update requirements.txt with missing dependencies, un-gitignore the model file, update Dockerfile to pre-cache torch.hub, and flip USE_MOCK_ML to False in docker-compose. No code changes to the application itself.

**Tech Stack:** PyTorch, YOLOv5 (torch.hub), ultralytics, Docker, docker-compose

---

### Task 1: Fix requirements.txt

**Files:**
- Modify: `backend/requirements.txt:27` (Pillow line)
- Modify: `backend/requirements.txt:29-35` (ML section)

**Step 1: Update Pillow version pin**

In `backend/requirements.txt`, change line 27:
```
Pillow==10.1.0
```
to:
```
Pillow>=10.3.0,<13.0.0
```

Pillow 12+ introduced a breaking change in `ImageFile._Tile`. This pin allows upgrades but avoids the broken version.

**Step 2: Add ultralytics and gitpython to ML section**

In `backend/requirements.txt`, after the existing ML dependencies (after line 35 `tqdm>=4.60.0`), add:
```
ultralytics>=8.0.0
gitpython>=3.1.30
```

The full ML section should now read:
```
# ML / Pest Detection (YOLOv5 via torch.hub)
torch>=2.0.0
torchvision>=0.15.0
opencv-python-headless>=4.8.0
pandas>=2.0.0
seaborn>=0.12.0
tqdm>=4.60.0
ultralytics>=8.0.0
gitpython>=3.1.30
```

**Step 3: Verify locally**

Run:
```bash
cd /home/bryan/AgriSense/backend
source venv/bin/activate
pip install -r requirements.txt
```
Expected: Installs successfully with no errors.

**Step 4: Smoke test model load**

Run:
```bash
cd /home/bryan/AgriSense/backend
source venv/bin/activate
python3 -c "
from services.pest_ml_service import pest_ml_service
result = pest_ml_service.load_model('./ml_models/pest_model.pt')
print(f'Model loaded: {result}')
print(f'Classes: {pest_ml_service.class_names}')
"
```
Expected: `Model loaded: True` and all 10 class names printed.

**Step 5: Commit**

```bash
git add backend/requirements.txt
git commit -m "fix: add missing ML dependencies (ultralytics, gitpython) and pin Pillow"
```

---

### Task 2: Un-gitignore and commit the model file

**Files:**
- Modify: `.gitignore:109` (remove `backend/ml_models/*.pt` line)
- Add to git: `backend/ml_models/pest_model.pt` (14MB)

**Step 1: Update .gitignore**

In `.gitignore`, change the ML model files section (lines 108-113) from:
```
# ML model files
backend/ml_models/*.pt
backend/ml_models/*.onnx
backend/ml_models/*.tflite
best.pt.zip
best.pt/
```
to:
```
# ML model files (keep .pt tracked for deployment, ignore large/converted formats)
backend/ml_models/*.onnx
backend/ml_models/*.tflite
best.pt.zip
best.pt/
```

**Step 2: Verify the model file is now trackable**

Run:
```bash
cd /home/bryan/AgriSense
git status
```
Expected: `backend/ml_models/pest_model.pt` shows as untracked.

**Step 3: Commit**

```bash
git add .gitignore backend/ml_models/pest_model.pt
git commit -m "feat: track pest_model.pt in git for deployment (14MB)"
```

---

### Task 3: Update Dockerfile for PyTorch + torch.hub cache

**Files:**
- Modify: `backend/Dockerfile`

**Step 1: Update the Dockerfile**

Replace the entire contents of `backend/Dockerfile` with:

```dockerfile
# ===================================
# AgriSense Backend - Dockerfile
# ===================================
# Multi-stage build for optimized production image

# ===================================
# Stage 1: Builder
# ===================================
FROM python:3.10-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ===================================
# Stage 2: Production
# ===================================
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Pre-cache YOLOv5 torch.hub repo so it doesn't download at runtime
RUN python -c "import torch; torch.hub.load('ultralytics/yolov5', 'custom', path='ml_models/pest_model.pt', trust_repo=True)" || true

# Create directories for uploads and logs
RUN mkdir -p uploads logs && \
    chmod 755 uploads logs

# Create non-root user for security
RUN useradd -m -u 1000 agrisense && \
    chown -R agrisense:agrisense /app

# Switch to non-root user
USER agrisense

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Key changes from original:
- Added `libgl1-mesa-glx` and `libglib2.0-0` to both stages (OpenCV runtime deps)
- Added `RUN python -c "import torch; torch.hub.load(...)"` to pre-cache YOLOv5 repo
- The `|| true` ensures the build doesn't fail if the model test run produces warnings

**Step 2: Commit**

```bash
git add backend/Dockerfile
git commit -m "feat: update Dockerfile for PyTorch and torch.hub pre-caching"
```

---

### Task 4: Update docker-compose.yml

**Files:**
- Modify: `docker-compose.yml:57-58` (USE_MOCK_ML and ML_SERVICE_URL lines)

**Step 1: Update environment variables**

In `docker-compose.yml`, in the backend service environment section, change:
```
      USE_MOCK_ML: ${USE_MOCK_ML:-True}
      ML_SERVICE_URL: ${ML_SERVICE_URL:-http://ml-service:8001/predict}
```
to:
```
      USE_MOCK_ML: ${USE_MOCK_ML:-False}
      PEST_MODEL_PATH: /app/ml_models/pest_model.pt
      ML_SERVICE_URL: ${ML_SERVICE_URL:-http://ml-service:8001/predict}
```

**Step 2: Commit**

```bash
git add docker-compose.yml
git commit -m "feat: enable real ML inference in production (USE_MOCK_ML=False)"
```

---

### Task 5: Local Docker build test

**Step 1: Build the Docker image locally**

Run:
```bash
cd /home/bryan/AgriSense
docker compose build backend
```
Expected: Build completes successfully. The torch.hub pre-cache step should print YOLOv5 model summary with 10 classes.

**Step 2: Verify image was created**

Run:
```bash
docker images | grep agrisense
```
Expected: Image listed (will be ~3-4GB).

**Step 3: (Optional) Quick container test**

Run:
```bash
docker compose up backend -d
docker compose logs backend --tail 20
```
Expected: Logs show "Pest ML model loaded — classes: [rice leaf roller, ...]"

Run:
```bash
docker compose down
```

**Step 4: Commit the design doc and plan**

```bash
git add docs/plans/
git commit -m "docs: add ML deployment design and implementation plan"
```

---

### Task 6: Deploy to production

**Step 1: Push to main**

Merge changes to `main` branch. This triggers the GitHub Actions CI/CD pipeline which will:
1. Run tests (with USE_MOCK_ML=True, no PyTorch needed)
2. SSH to server, pull code, `docker compose up --build`

**Step 2: Verify deployment**

After CI/CD completes, check the production API:
```bash
curl https://agrisense.bryanlzj.work/health
```
Expected: `{"status": "healthy", ...}`

**Step 3: Test pest detection endpoint**

Upload a test image to the production pest detection endpoint and verify `model_loaded: true` in the response (not mock predictions).
