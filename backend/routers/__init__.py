"""
API Routers Package

This package contains all API route handlers organized by feature.
Each router handles a specific domain (auth, sensors, pests, alerts, weather).

Router Organization:
- auth.py: User authentication (register, login, token refresh)
- sensors.py: Sensor data management (create, read, list readings)
- pests.py: Pest detection management (upload image, get detections)
- alerts.py: Alert management (list, mark as read, delete)
- weather.py: Weather forecasts (get forecast, weather alerts)

All routers are registered in main.py with the /api/v1 prefix.
"""

from fastapi import APIRouter

# Import all routers (will be created in subsequent tasks)
# from .auth import router as auth_router
# from .sensors import router as sensors_router
# from .pests import router as pests_router
# from .alerts import router as alerts_router
# from .weather import router as weather_router

__all__ = [
    # "auth_router",
    # "sensors_router",
    # "pests_router",
    # "alerts_router",
    # "weather_router",
]
