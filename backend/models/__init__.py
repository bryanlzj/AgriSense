"""
Models Package

This package contains all SQLAlchemy database models.

Import all models here so Alembic can detect them for migrations.
"""

from .user import User
from .sensor_reading import SensorReading
from .pest_detection import PestDetection, SeverityLevel
from .alert import Alert, AlertType, AlertSeverity
from .pest_report import PestReport, ObservedSeverity, ReportStatus
from .pest_weather_correlation import PestWeatherCorrelation
from .weather_cache import WeatherCache

# Export all models
__all__ = [
    "User",
    "SensorReading",
    "PestDetection",
    "SeverityLevel",
    "Alert",
    "AlertType",
    "AlertSeverity",
    "PestReport",
    "ObservedSeverity",
    "ReportStatus",
    "PestWeatherCorrelation",
    "WeatherCache",
]
