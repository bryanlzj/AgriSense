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
    port: int = Field(default=5000, env="PORT")
    
    # ===================================
    # Database Configuration
    # ===================================
    database_url: str = Field(
        default="sqlite:///./agrisense.db",
        env="DATABASE_URL"
    )
    
    # PostgreSQL specific (optional)
    postgres_user: Optional[str] = Field(default=None, env="POSTGRES_USER")
    postgres_password: Optional[str] = Field(default=None, env="POSTGRES_PASSWORD")
    postgres_db: Optional[str] = Field(default=None, env="POSTGRES_DB")
    postgres_host: Optional[str] = Field(default="localhost", env="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, env="POSTGRES_PORT")
    
    # ===================================
    # Authentication & Security
    # ===================================
    secret_key: str = Field(
        default="dev-secret-key-change-in-production",
        env="SECRET_KEY"
    )
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_days: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_DAYS")
    bcrypt_rounds: int = Field(default=12, env="BCRYPT_ROUNDS")
    
    # ===================================
    # Weather API (OpenWeatherMap)
    # ===================================
    openweather_api_key: str = Field(
        default="",
        env="OPENWEATHER_API_KEY"
    )
    openweather_base_url: str = Field(
        default="https://api.openweathermap.org/data/2.5",
        env="OPENWEATHER_BASE_URL"
    )
    default_latitude: float = Field(default=3.1390, env="DEFAULT_LATITUDE")
    default_longitude: float = Field(default=101.6869, env="DEFAULT_LONGITUDE")
    default_location: str = Field(default="Kuala Lumpur", env="DEFAULT_LOCATION")
    weather_cache_duration: int = Field(default=1800, env="WEATHER_CACHE_DURATION")
    
    # ===================================
    # ML Service Configuration
    # ===================================
    use_mock_ml: bool = Field(default=True, env="USE_MOCK_ML")
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
    # Sensor Data Simulation
    # ===================================
    sensor_poll_interval: int = Field(default=30, env="SENSOR_POLL_INTERVAL")
    temp_min: float = Field(default=20.0, env="TEMP_MIN")
    temp_max: float = Field(default=35.0, env="TEMP_MAX")
    humidity_min: float = Field(default=40.0, env="HUMIDITY_MIN")
    humidity_max: float = Field(default=90.0, env="HUMIDITY_MAX")
    soil_moisture_min: float = Field(default=20.0, env="SOIL_MOISTURE_MIN")
    soil_moisture_max: float = Field(default=80.0, env="SOIL_MOISTURE_MAX")
    light_min: float = Field(default=100.0, env="LIGHT_MIN")
    light_max: float = Field(default=1000.0, env="LIGHT_MAX")
    
    # ===================================
    # Alert System Configuration
    # ===================================
    temp_high_threshold: float = Field(default=32.0, env="TEMP_HIGH_THRESHOLD")
    temp_low_threshold: float = Field(default=18.0, env="TEMP_LOW_THRESHOLD")
    humidity_high_threshold: float = Field(default=85.0, env="HUMIDITY_HIGH_THRESHOLD")
    soil_moisture_low_threshold: float = Field(
        default=30.0,
        env="SOIL_MOISTURE_LOW_THRESHOLD"
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
        default="sqlite:///./test_agrisense.db",
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
