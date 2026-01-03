"""
AgriSense Backend API
FastAPI application for IoT-driven weather and pest risk management system
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="AgriSense API",
    description="IoT-Driven Early Warning System for Weather and Pest Risk Management",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/redoc"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "AgriSense API is running",
        "version": "1.0.0",
        "status": "healthy",
        "features": [
            "Weather Early Warning System",
            "Pest Risk Management System",
            "Environmental Monitoring",
            "Unified Alert System"
        ]
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "api": "operational",
        "database": "not_configured",  # Will be updated after DB setup
        "services": {
            "weather_api": "not_configured",
            "ml_service": "not_configured"
        }
    }

# Exception handler for general errors
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc)
        }
    )

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=True  # Enable auto-reload during development
    )
