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
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
# ultralytics pulls in opencv-python (needs GUI libs absent in slim images).
# We install everything, then swap to headless opencv as the final step.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip uninstall -y opencv-python 2>/dev/null || true && \
    pip install --no-cache-dir --force-reinstall opencv-python-headless "requests>=2.32.2"

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
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Verify only headless opencv is present (no GUI opencv)
RUN python -c "import cv2; print('cv2 OK:', cv2.__version__)"

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 agrisense

# Pre-cache YOLOv5 torch.hub repo under agrisense user's home
RUN TORCH_HOME=/home/agrisense/.cache/torch \
    python -c "import torch; torch.hub.load('ultralytics/yolov5', 'custom', path='ml_models/pest_model.pt', trust_repo=True)" && \
    echo 'YOLOv5 pre-cache SUCCESS' || echo 'YOLOv5 pre-cache FAILED'

# Create directories for uploads and logs
RUN mkdir -p uploads logs && \
    chmod 755 uploads logs && \
    chown -R agrisense:agrisense /app /home/agrisense

# Switch to non-root user
USER agrisense

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
