"""
AgriSense Backend - Main Application Entry Point

This is the main FastAPI application that serves the AgriSense API.

Features:
- RESTful API with versioning (/api/v1)
- Automatic API documentation (Swagger UI at /docs)
- CORS enabled for mobile app integration
- Organized routers by feature domain
- Database session management
- Error handling and validation

Tech Stack:
- FastAPI: Modern Python web framework
- SQLAlchemy: ORM for database operations
- Alembic: Database migrations
- Pydantic: Data validation
- Uvicorn: ASGI server

Development:
Run with: uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from contextlib import asynccontextmanager

# Import routers
from routers.auth import router as auth_router
from routers.sensor import router as sensor_router
from routers.pest import router as pest_router
from routers.weather import router as weather_router
from routers.alert import router as alert_router
from routers.chat import router as chat_router
from routers.dashboard import router as dashboard_router
from routers.sector import router as sector_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown

    Startup:
    - Initialize database (check schema, create tables, seed data)
    - Start background job scheduler

    Shutdown:
    - Stop background job scheduler
    - Clean up resources
    """
    # Startup
    from db_init import initialize_database
    from jobs.scheduler import start_scheduler, stop_scheduler
    from config import settings
    from services.pest_ml_service import pest_ml_service

    initialize_database()

    # Load pest detection ML model
    if not settings.use_mock_ml:
        loaded = pest_ml_service.load_model(settings.pest_model_path)
        if loaded:
            print(f"Pest ML model loaded — classes: {list(pest_ml_service.class_names.values())}")
        else:
            print("Pest ML model not found, falling back to mock predictions")
    else:
        print("USE_MOCK_ML=True — skipping ML model load, using mock predictions")

    # Start background jobs (weather check, pest risk check)
    # Comment out if you want to disable background jobs
    try:
        start_scheduler()
    except Exception as e:
        print(f"Warning: Failed to start scheduler: {e}")

    yield

    # Shutdown
    try:
        stop_scheduler()
    except Exception as e:
        print(f"Warning: Error stopping scheduler: {e}")


# Create FastAPI application
app = FastAPI(
    title="AgriSense API",
    description="Backend API for AgriSense - Agricultural Early Warning System",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc alternative documentation
    lifespan=lifespan,  # Add lifespan handler
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows the Flutter mobile app to make requests to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Mount static files for uploaded images
UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# Register API routers with /api/v1 prefix
app.include_router(auth_router, prefix="/api/v1")
app.include_router(sensor_router, prefix="/api/v1")
app.include_router(pest_router, prefix="/api/v1")
app.include_router(weather_router, prefix="/api/v1")
app.include_router(alert_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(sector_router, prefix="/api/v1")


@app.get("/")
async def root():
    """
    Root endpoint - API health check
    
    Returns:
        dict: Welcome message and API status
    """
    return {
        "message": "Welcome to AgriSense API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    
    Used by monitoring tools to verify the API is running.
    Checks database connectivity and returns current timestamp.
    
    Returns:
        dict: Health status with database connection and timestamp
    """
    from datetime import datetime
    from sqlalchemy import text
    from database import SessionLocal
    
    # Check database connection
    db_status = "disconnected"
    try:
        db = SessionLocal()
        # Try a simple query to verify database is accessible
        db.execute(text("SELECT 1"))
        db.close()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


# Error handlers can be added here
# Example:
# @app.exception_handler(ValueError)
# async def value_error_handler(request, exc):
#     return JSONResponse(
#         status_code=400,
#         content={"detail": str(exc)},
#     )


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    # This is only used when running: python main.py
    # In production, use: uvicorn main:app --host 0.0.0.0 --port 8000
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (development only)
    )
