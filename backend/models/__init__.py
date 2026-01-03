"""
Models Package

This package contains all SQLAlchemy database models.

Import all models here so Alembic can detect them for migrations.
"""

from backend.models.user import User
from backend.models.sensor_reading import SensorReading

# Import other models as they are created
# from backend.models.pest_detection import PestDetection
# from backend.models.alert import Alert

# Export all models
__all__ = [
    "User",
    "SensorReading",
    # "PestDetection",
    # "Alert",
]
