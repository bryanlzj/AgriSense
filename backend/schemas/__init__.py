"""
Pydantic schemas for request/response validation.
"""

from .auth import (
    UserRegister,
    UserLogin,
    Token,
    UserResponse
)
from .sensor import (
    SensorDataCreate,
    SensorDataResponse,
    SensorDataUpdate,
    SensorDataFilter
)
from .pest import (
    PestDetectionCreate,
    PestDetectionResponse,
    ImageUploadResponse,
    PestDetectionResult,
    PestDetectionAnalysisResponse,
    PestDetectionFilter,
    PestStatistics
)
from .weather import (
    WeatherCondition,
    WeatherForecastItem,
    WeatherAlert,
    AgriculturalRecommendation,
    LocationInput,
    CurrentWeatherResponse,
    WeatherForecastResponse,
    WeatherSummaryResponse
)

__all__ = [
    "UserRegister",
    "UserLogin",
    "Token",
    "UserResponse",
    "SensorDataCreate",
    "SensorDataResponse",
    "SensorDataUpdate",
    "SensorDataFilter",
    "PestDetectionCreate",
    "PestDetectionResponse",
    "ImageUploadResponse",
    "PestDetectionResult",
    "PestDetectionAnalysisResponse",
    "PestDetectionFilter",
    "PestStatistics",
    "WeatherCondition",
    "WeatherForecastItem",
    "WeatherAlert",
    "AgriculturalRecommendation",
    "LocationInput",
    "CurrentWeatherResponse",
    "WeatherForecastResponse",
    "WeatherSummaryResponse",
]
