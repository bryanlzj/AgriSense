"""
Models Package

This package contains all SQLAlchemy database models.

Import all models here so Alembic can detect them for migrations.
"""

from backend.models.user import User
from backend.models.sensor_reading import SensorReading
from backend.models.pest_detection import PestDetection, SeverityLevel
from backend.models.alert import Alert, AlertType, AlertSeverity

# Export all models
__all__ = [
    "User",
    "SensorReading",
    "PestDetection",
    "SeverityLevel",
    "Alert",
    "AlertType",
    "AlertSeverity",
]
