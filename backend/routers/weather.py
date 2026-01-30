"""
Weather router for weather forecast and alert endpoints.

This module provides endpoints for:
- Current weather conditions
- Weather forecasts (5 days)
- Weather summary (current + forecast)
- Agricultural recommendations based on weather

Learning Notes:
- Uses OpenWeatherMap API for weather data
- Implements caching to reduce API calls
- Generates alerts and recommendations automatically
- Requires authentication for all endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import httpx

from database import get_db
from models.user import User
from dependencies.auth import get_current_user
from schemas.weather import (
    CurrentWeatherResponse,
    WeatherForecastResponse,
    WeatherSummaryResponse,
    LocationInput
)
from services.weather_service import (
    get_current_weather,
    get_weather_forecast,
    get_weather_summary
)


# ============================================================================
# ROUTER SETUP
# ============================================================================

router = APIRouter(
    prefix="/weather",
    tags=["weather"],
    responses={
        401: {"description": "Unauthorized - Invalid or missing token"},
        500: {"description": "Internal server error"}
    }
)


# ============================================================================
# WEATHER ENDPOINTS
# ============================================================================

@router.get("/current", response_model=CurrentWeatherResponse)
async def get_current_weather_endpoint(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude coordinate"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude coordinate"),
    location_name: Optional[str] = Query(None, description="Optional location name"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current weather conditions with alerts and recommendations.
    
    **Authentication Required:** Yes
    
    **Query Parameters:**
    - latitude: Latitude coordinate (-90 to 90)
    - longitude: Longitude coordinate (-180 to 180)
    - location_name: Optional location name for display
    
    **Returns:**
    - Current weather conditions
    - Active weather alerts
    - Agricultural recommendations
    - Timestamp of data update
    
    **Example:**
    ```
    GET /api/v1/weather/current?latitude=3.1390&longitude=101.6869&location_name=Kuala%20Lumpur
    ```
    
    **Response:**
    ```json
    {
      "location": {
        "latitude": 3.1390,
        "longitude": 101.6869,
        "location_name": "Kuala Lumpur"
      },
      "current": {
        "temperature": 28.5,
        "feels_like": 32.1,
        "humidity": 75,
        "pressure": 1012,
        "wind_speed": 3.5,
        "wind_direction": 180,
        "clouds": 40,
        "visibility": 10000,
        "weather_main": "Clouds",
        "weather_description": "scattered clouds",
        "rain_1h": null,
        "rain_3h": null
      },
      "alerts": [],
      "recommendations": [
        {
          "category": "irrigation",
          "priority": "medium",
          "title": "Normal Irrigation",
          "description": "Maintain regular irrigation schedule.",
          "reason": "Temperature: 28.5°C, Humidity: 75%",
          "actions": ["Water early morning or late evening"]
        }
      ],
      "updated_at": "2025-01-04T10:30:00"
    }
    ```
    
    **Learning Notes:**
    - Weather data is cached for 10 minutes to reduce API calls
    - Alerts are generated based on weather conditions
    - Recommendations are tailored for Malaysian agriculture
    - Free OpenWeatherMap API allows 1000 calls/day
    """
    try:
        weather_data = await get_current_weather(latitude, longitude, location_name)
        return weather_data
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch weather data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/forecast", response_model=WeatherForecastResponse)
async def get_weather_forecast_endpoint(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude coordinate"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude coordinate"),
    location_name: Optional[str] = Query(None, description="Optional location name"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get 5-day weather forecast with alerts and recommendations.
    
    **Authentication Required:** Yes
    
    **Query Parameters:**
    - latitude: Latitude coordinate (-90 to 90)
    - longitude: Longitude coordinate (-180 to 180)
    - location_name: Optional location name for display
    
    **Returns:**
    - Weather forecast (5 days, 3-hour intervals = 40 data points)
    - Active weather alerts
    - Agricultural recommendations
    - Timestamp of data update
    
    **Example:**
    ```
    GET /api/v1/weather/forecast?latitude=3.1390&longitude=101.6869
    ```
    
    **Response:**
    ```json
    {
      "location": {
        "latitude": 3.1390,
        "longitude": 101.6869,
        "location_name": null
      },
      "forecast": [
        {
          "forecast_time": "2025-01-04T12:00:00",
          "temperature": 29.0,
          "feels_like": 33.2,
          "humidity": 70,
          "pressure": 1013,
          "wind_speed": 4.0,
          "clouds": 50,
          "weather_main": "Clouds",
          "weather_description": "broken clouds",
          "rain_probability": 0.2,
          "rain_volume": null
        },
        // ... 39 more forecast items
      ],
      "alerts": [],
      "recommendations": [],
      "updated_at": "2025-01-04T10:30:00"
    }
    ```
    
    **Learning Notes:**
    - OpenWeatherMap free tier provides 5-day forecast
    - Forecast data is in 3-hour intervals (8 per day)
    - rain_probability is 0-1 (0% to 100%)
    - Useful for planning agricultural activities
    """
    try:
        forecast_data = await get_weather_forecast(latitude, longitude, location_name)
        return forecast_data
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch forecast data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/summary", response_model=WeatherSummaryResponse)
async def get_weather_summary_endpoint(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude coordinate"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude coordinate"),
    location_name: Optional[str] = Query(None, description="Optional location name"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get complete weather summary (current + forecast + alerts + recommendations).
    
    **Authentication Required:** Yes
    
    **Query Parameters:**
    - latitude: Latitude coordinate (-90 to 90)
    - longitude: Longitude coordinate (-180 to 180)
    - location_name: Optional location name for display
    
    **Returns:**
    - Current weather conditions
    - 5-day weather forecast
    - Active weather alerts
    - Agricultural recommendations
    - Timestamp of data update
    
    **Example:**
    ```
    GET /api/v1/weather/summary?latitude=3.1390&longitude=101.6869&location_name=Kuala%20Lumpur
    ```
    
    **Response:**
    ```json
    {
      "location": {
        "latitude": 3.1390,
        "longitude": 101.6869,
        "location_name": "Kuala Lumpur"
      },
      "current": {
        "temperature": 28.5,
        "feels_like": 32.1,
        "humidity": 75,
        // ... more current weather fields
      },
      "forecast": [
        {
          "forecast_time": "2025-01-04T12:00:00",
          "temperature": 29.0,
          // ... more forecast fields
        },
        // ... 39 more forecast items
      ],
      "alerts": [
        {
          "alert_type": "Heavy Rain Forecast",
          "severity": "medium",
          "title": "Heavy Rain Expected",
          "description": "High probability of rain in next 24 hours.",
          "start_time": "2025-01-04T15:00:00",
          "end_time": "2025-01-05T03:00:00",
          "recommendations": [
            "Complete urgent field work before rain",
            "Prepare drainage systems"
          ]
        }
      ],
      "recommendations": [
        {
          "category": "irrigation",
          "priority": "high",
          "title": "Suspend Irrigation",
          "description": "Rain expected soon. Suspend irrigation to avoid waterlogging.",
          "reason": "Rain probability: 80%",
          "actions": [
            "Turn off irrigation systems",
            "Check soil moisture levels"
          ]
        }
      ],
      "updated_at": "2025-01-04T10:30:00"
    }
    ```
    
    **Learning Notes:**
    - Most comprehensive endpoint - combines current + forecast
    - Alerts are generated based on both current and forecast data
    - Recommendations consider upcoming weather conditions
    - Ideal for dashboard/home screen display
    - Makes 2 API calls but uses caching to optimize
    """
    try:
        summary_data = await get_weather_summary(latitude, longitude, location_name)
        return summary_data
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch weather summary: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


# ============================================================================
# HELPER ENDPOINTS
# ============================================================================

@router.get("/test")
async def test_weather_api(
    current_user: User = Depends(get_current_user)
):
    """
    Test endpoint to verify OpenWeatherMap API is configured correctly.
    
    **Authentication Required:** Yes
    
    **Returns:**
    - API configuration status
    - Sample weather data for Kuala Lumpur
    
    **Example:**
    ```
    GET /api/v1/weather/test
    ```
    
    **Response:**
    ```json
    {
      "status": "ok",
      "message": "Weather API is configured correctly",
      "sample_location": "Kuala Lumpur",
      "sample_data": {
        "temperature": 28.5,
        "weather": "Clouds"
      }
    }
    ```
    """
    try:
        # Test with Kuala Lumpur coordinates
        weather_data = await get_current_weather(3.1390, 101.6869, "Kuala Lumpur")
        
        return {
            "status": "ok",
            "message": "Weather API is configured correctly",
            "sample_location": "Kuala Lumpur",
            "sample_data": {
                "temperature": weather_data.current.temperature,
                "weather": weather_data.current.weather_main,
                "humidity": weather_data.current.relative_humidity
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Weather API test failed: {str(e)}"
        )
