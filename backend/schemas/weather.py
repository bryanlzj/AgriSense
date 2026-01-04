"""
Weather schemas for API requests and responses.

This module defines Pydantic schemas for weather-related data including:
- Current weather conditions
- Weather forecasts
- Weather alerts
- Agricultural recommendations based on weather

Learning Notes:
- Pydantic schemas provide automatic validation and serialization
- Optional fields use Optional[type] = None
- datetime fields are automatically parsed from ISO format strings
- Nested schemas allow for complex data structures
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ============================================================================
# WEATHER CONDITION SCHEMAS
# ============================================================================

class WeatherCondition(BaseModel):
    """
    Current weather condition details.
    
    Attributes:
        temperature: Temperature in Celsius
        feels_like: Perceived temperature in Celsius
        humidity: Humidity percentage (0-100)
        pressure: Atmospheric pressure in hPa
        wind_speed: Wind speed in m/s
        wind_direction: Wind direction in degrees (0-360)
        clouds: Cloudiness percentage (0-100)
        visibility: Visibility in meters
        weather_main: Main weather condition (e.g., "Rain", "Clear")
        weather_description: Detailed weather description
        rain_1h: Rain volume for last hour in mm (optional)
        rain_3h: Rain volume for last 3 hours in mm (optional)
    """
    temperature: float = Field(..., description="Temperature in Celsius")
    feels_like: float = Field(..., description="Perceived temperature in Celsius")
    humidity: int = Field(..., ge=0, le=100, description="Humidity percentage")
    pressure: int = Field(..., description="Atmospheric pressure in hPa")
    wind_speed: float = Field(..., ge=0, description="Wind speed in m/s")
    wind_direction: int = Field(..., ge=0, le=360, description="Wind direction in degrees")
    clouds: int = Field(..., ge=0, le=100, description="Cloudiness percentage")
    visibility: int = Field(..., ge=0, description="Visibility in meters")
    weather_main: str = Field(..., description="Main weather condition")
    weather_description: str = Field(..., description="Detailed weather description")
    rain_1h: Optional[float] = Field(None, description="Rain volume for last hour in mm")
    rain_3h: Optional[float] = Field(None, description="Rain volume for last 3 hours in mm")


class WeatherForecastItem(BaseModel):
    """
    Single forecast item for a specific time.
    
    Attributes:
        forecast_time: Time of the forecast
        temperature: Temperature in Celsius
        feels_like: Perceived temperature in Celsius
        humidity: Humidity percentage
        pressure: Atmospheric pressure in hPa
        wind_speed: Wind speed in m/s
        clouds: Cloudiness percentage
        weather_main: Main weather condition
        weather_description: Detailed weather description
        rain_probability: Probability of precipitation (0-1)
        rain_volume: Expected rain volume in mm (optional)
    """
    forecast_time: datetime = Field(..., description="Time of the forecast")
    temperature: float = Field(..., description="Temperature in Celsius")
    feels_like: float = Field(..., description="Perceived temperature in Celsius")
    humidity: int = Field(..., ge=0, le=100, description="Humidity percentage")
    pressure: int = Field(..., description="Atmospheric pressure in hPa")
    wind_speed: float = Field(..., ge=0, description="Wind speed in m/s")
    clouds: int = Field(..., ge=0, le=100, description="Cloudiness percentage")
    weather_main: str = Field(..., description="Main weather condition")
    weather_description: str = Field(..., description="Detailed weather description")
    rain_probability: float = Field(..., ge=0, le=1, description="Probability of precipitation")
    rain_volume: Optional[float] = Field(None, description="Expected rain volume in mm")


# ============================================================================
# WEATHER ALERT SCHEMAS
# ============================================================================

class WeatherAlert(BaseModel):
    """
    Weather alert/warning information.
    
    Attributes:
        alert_type: Type of alert (e.g., "Heavy Rain", "Strong Wind")
        severity: Severity level (low, medium, high, extreme)
        title: Alert title
        description: Detailed alert description
        start_time: Alert start time
        end_time: Alert end time
        recommendations: List of recommended actions
    """
    alert_type: str = Field(..., description="Type of alert")
    severity: str = Field(..., description="Severity level")
    title: str = Field(..., description="Alert title")
    description: str = Field(..., description="Detailed alert description")
    start_time: datetime = Field(..., description="Alert start time")
    end_time: datetime = Field(..., description="Alert end time")
    recommendations: List[str] = Field(default_factory=list, description="Recommended actions")


# ============================================================================
# AGRICULTURAL RECOMMENDATION SCHEMAS
# ============================================================================

class AgriculturalRecommendation(BaseModel):
    """
    Agricultural recommendations based on weather conditions.
    
    Attributes:
        category: Recommendation category (irrigation, pest_control, harvesting, etc.)
        priority: Priority level (low, medium, high)
        title: Recommendation title
        description: Detailed recommendation
        reason: Reason for the recommendation based on weather
        actions: List of specific actions to take
    """
    category: str = Field(..., description="Recommendation category")
    priority: str = Field(..., description="Priority level")
    title: str = Field(..., description="Recommendation title")
    description: str = Field(..., description="Detailed recommendation")
    reason: str = Field(..., description="Reason based on weather")
    actions: List[str] = Field(default_factory=list, description="Specific actions to take")


# ============================================================================
# LOCATION SCHEMAS
# ============================================================================

class LocationInput(BaseModel):
    """
    Location input for weather queries.
    
    Attributes:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        location_name: Optional location name for display
    """
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    location_name: Optional[str] = Field(None, description="Location name for display")


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================

class CurrentWeatherResponse(BaseModel):
    """
    Response for current weather endpoint.
    
    Attributes:
        location: Location information
        current: Current weather conditions
        alerts: List of active weather alerts
        recommendations: Agricultural recommendations
        updated_at: Timestamp of data update
    """
    location: LocationInput
    current: WeatherCondition
    alerts: List[WeatherAlert] = Field(default_factory=list)
    recommendations: List[AgriculturalRecommendation] = Field(default_factory=list)
    updated_at: datetime


class WeatherForecastResponse(BaseModel):
    """
    Response for weather forecast endpoint.
    
    Attributes:
        location: Location information
        forecast: List of forecast items (next 5 days, 3-hour intervals)
        alerts: List of active weather alerts
        recommendations: Agricultural recommendations
        updated_at: Timestamp of data update
    """
    location: LocationInput
    forecast: List[WeatherForecastItem]
    alerts: List[WeatherAlert] = Field(default_factory=list)
    recommendations: List[AgriculturalRecommendation] = Field(default_factory=list)
    updated_at: datetime


class WeatherSummaryResponse(BaseModel):
    """
    Response for weather summary endpoint (current + forecast).
    
    Attributes:
        location: Location information
        current: Current weather conditions
        forecast: List of forecast items
        alerts: List of active weather alerts
        recommendations: Agricultural recommendations
        updated_at: Timestamp of data update
    """
    location: LocationInput
    current: WeatherCondition
    forecast: List[WeatherForecastItem]
    alerts: List[WeatherAlert] = Field(default_factory=list)
    recommendations: List[AgriculturalRecommendation] = Field(default_factory=list)
    updated_at: datetime
