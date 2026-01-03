"""
Models Package

This package contains all SQLAlchemy database models.

Import all models here so Alembic can detect them for migrations.
"""

from backend.models.user import User

# Import other models as they are created
# from backend.models.pest_detection import PestDetection
# from backend.models.alert import Alert
# from backend.models.sensor_reading import SensorReading

# Export all models
__all__ = [
    "User",
    # "PestDetection",
    # "Alert", 
    # "SensorReading",
]
