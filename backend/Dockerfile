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
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

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
