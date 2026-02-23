"""
Configuration management for AgriSense backend
Loads environment variables and provides typed configuration
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional
import os
import json
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # ===================================
    # Application Settings
    # ===================================
    app_name: str = Field(default="AgriSense", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=True, env="DEBUG")
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    # ===================================
    # Server Configuration
    # ===================================
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # ===================================
    # Database Configuration (PostgreSQL Only)
    # ===================================
    database_url: str = Field(
        default="postgresql://agrisense_user:strongpassword@localhost:5432/agrisense",
        env="DATABASE_URL"
    )
    
    # Database initialization
    seed_database: bool = Field(default=False, env="SEED_DATABASE")
    
    # ===================================
    # Authentication & Security
    # ===================================
    secret_key: str = Field(
        default="dev-secret-key-change-in-production",
        env="SECRET_KEY"
    )
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_days: int = Field(default=7, env="ACCESS_TOKEN_EXPIRE_DAYS")
    bcrypt_rounds: int = Field(default=12, env="BCRYPT_ROUNDS")
    
    # ===================================
    # AI Service (OpenRouter)
    # ===================================
    openrouter_api_key: str = Field(
        default="",
        env="OPENROUTER_API_KEY"
    )
    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1",
        env="OPENROUTER_BASE_URL"
    )
    # Free models: meta-llama/llama-3.1-8b-instruct:free, google/gemma-2-9b-it:free
    # Paid models: anthropic/claude-3.5-sonnet, openai/gpt-4o, x-ai/grok-4.1-fast
    openrouter_model: str = Field(
        default="meta-llama/llama-3.1-8b-instruct:free",
        env="OPENROUTER_MODEL"
    )

    # ===================================
    # Open-Meteo API (Free, no API key required)
    # ===================================
    openmeteo_base_url: str = Field(
        default="https://api.open-meteo.com/v1",
        env="OPENMETEO_BASE_URL"
    )
    default_latitude: float = Field(default=3.1390, env="DEFAULT_LATITUDE")
    default_longitude: float = Field(default=101.6869, env="DEFAULT_LONGITUDE")
    default_location: str = Field(default="Kuala Lumpur", env="DEFAULT_LOCATION")
    # ===================================
    # ML Service Configuration
    # ===================================
    use_mock_ml: bool = Field(default=False, env="USE_MOCK_ML")
    pest_model_path: str = Field(
        default="./ml_models/pest_model.pt",
        env="PEST_MODEL_PATH"
    )
    ml_service_url: str = Field(
        default="http://localhost:8001/predict",
        env="ML_SERVICE_URL"
    )
    ml_service_timeout: int = Field(default=10, env="ML_SERVICE_TIMEOUT")
    
    # Roboflow API (backup)
    roboflow_api_key: Optional[str] = Field(default=None, env="ROBOFLOW_API_KEY")
    roboflow_model_id: Optional[str] = Field(default=None, env="ROBOFLOW_MODEL_ID")
    roboflow_version: int = Field(default=1, env="ROBOFLOW_VERSION")
    
    # ===================================
    # File Upload Configuration
    # ===================================
    upload_dir: str = Field(default="./uploads", env="UPLOAD_DIR")
    max_upload_size: int = Field(default=10485760, env="MAX_UPLOAD_SIZE")  # 10MB
    allowed_image_extensions: List[str] = Field(
        default=["jpg", "jpeg", "png"],
        env="ALLOWED_IMAGE_EXTENSIONS"
    )
    
    # ===================================
    # Sensor Data Simulation (Open-Meteo aligned)
    # ===================================
    sensor_poll_interval: int = Field(default=30, env="SENSOR_POLL_INTERVAL")
    temp_min: float = Field(default=20.0, env="TEMP_MIN")
    temp_max: float = Field(default=35.0, env="TEMP_MAX")
    humidity_min: float = Field(default=40.0, env="HUMIDITY_MIN")
    humidity_max: float = Field(default=90.0, env="HUMIDITY_MAX")
    # Soil moisture in volumetric units (m³/m³), typical range 0.1-0.5
    soil_moisture_min: float = Field(default=0.1, env="SOIL_MOISTURE_MIN")
    soil_moisture_max: float = Field(default=0.5, env="SOIL_MOISTURE_MAX")
    # Rain in mm
    rain_min: float = Field(default=0.0, env="RAIN_MIN")
    rain_max: float = Field(default=50.0, env="RAIN_MAX")
    # Wind speed in km/h
    wind_speed_min: float = Field(default=0.0, env="WIND_SPEED_MIN")
    wind_speed_max: float = Field(default=60.0, env="WIND_SPEED_MAX")
    # Solar radiation (GHI) in W/m²
    solar_radiation_min: float = Field(default=0.0, env="SOLAR_RADIATION_MIN")
    solar_radiation_max: float = Field(default=1000.0, env="SOLAR_RADIATION_MAX")
    # Soil temperature in °C
    soil_temp_min: float = Field(default=20.0, env="SOIL_TEMP_MIN")
    soil_temp_max: float = Field(default=35.0, env="SOIL_TEMP_MAX")
    
    # ===================================
    # Alert System Configuration
    # ===================================
    temp_high_threshold: float = Field(default=32.0, env="TEMP_HIGH_THRESHOLD")
    temp_low_threshold: float = Field(default=18.0, env="TEMP_LOW_THRESHOLD")
    humidity_high_threshold: float = Field(default=85.0, env="HUMIDITY_HIGH_THRESHOLD")
    # Soil moisture threshold in volumetric units (m³/m³)
    soil_moisture_low_threshold: float = Field(
        default=0.2,
        env="SOIL_MOISTURE_LOW_THRESHOLD"
    )
    # Wind speed threshold in km/h
    wind_speed_high_threshold: float = Field(
        default=50.0,
        env="WIND_SPEED_HIGH_THRESHOLD"
    )
    # Rain threshold in mm (heavy rain)
    rain_heavy_threshold: float = Field(
        default=10.0,
        env="RAIN_HEAVY_THRESHOLD"
    )
    pest_confidence_threshold: float = Field(
        default=0.80,
        env="PEST_CONFIDENCE_THRESHOLD"
    )
    alert_check_interval: int = Field(default=60, env="ALERT_CHECK_INTERVAL")
    
    # ===================================
    # Redis Configuration
    # ===================================
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_db: int = Field(default=0, env="REDIS_DB")
    redis_password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    
    # ===================================
    # Logging Configuration
    # ===================================
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="./logs/agrisense.log", env="LOG_FILE")
    
    # ===================================
    # CORS Configuration
    # ===================================
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        env="CORS_ORIGINS"
    )
    
    # ===================================
    # Testing Configuration
    # ===================================
    test_database_url: str = Field(
        default="postgresql://agrisense_user:strongpassword@localhost:5432/agrisense_test",
        env="TEST_DATABASE_URL"
    )
    
    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        """Parse comma-separated or JSON array CORS origins into a list"""
        if isinstance(v, str):
            # Try to parse as JSON first
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except (json.JSONDecodeError, ValueError):
                pass
            # Fall back to comma-separated
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("allowed_image_extensions", pre=True)
    def parse_allowed_extensions(cls, v):
        """Parse comma-separated or JSON array extensions into a list"""
        if isinstance(v, str):
            # Try to parse as JSON first
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except (json.JSONDecodeError, ValueError):
                pass
            # Fall back to comma-separated
            return [ext.strip() for ext in v.split(",")]
        return v
    
    @validator("upload_dir", "log_file")
    def create_directories(cls, v):
        """Ensure directories exist"""
        path = Path(v)
        if path.suffix:  # It's a file path
            path.parent.mkdir(parents=True, exist_ok=True)
        else:  # It's a directory path
            path.mkdir(parents=True, exist_ok=True)
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra environment variables not defined in the model


# Create global settings instance
settings = Settings()


# Helper functions
def get_database_url() -> str:
    """Get the appropriate database URL based on environment"""
    if settings.environment == "test":
        return settings.test_database_url
    return settings.database_url


def is_production() -> bool:
    """Check if running in production environment"""
    return settings.environment == "production"


def is_development() -> bool:
    """Check if running in development environment"""
    return settings.environment == "development"


def get_cors_origins() -> List[str]:
    """Get list of allowed CORS origins"""
    if isinstance(settings.cors_origins, str):
        return [origin.strip() for origin in settings.cors_origins.split(",")]
    return settings.cors_origins


# Export settings
__all__ = ["settings", "get_database_url", "is_production", "is_development", "get_cors_origins"]
