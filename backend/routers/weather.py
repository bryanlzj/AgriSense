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
from datetime import datetime, timedelta, timezone
from collections import Counter
import httpx

from database import get_db
from models.user import User
from models.sensor_reading import SensorReading
from dependencies.auth import get_current_user
from schemas.weather import (
    CurrentWeatherResponse,
    WeatherForecastResponse,
    WeatherSummaryResponse,
    LocationInput,
    CurrentSensorWeatherResponse,
    HistoricalWeatherResponse,
    HistoricalSummary,
    SensorWeatherReading,
)
from services.weather_service import (
    get_current_weather,
    get_weather_forecast,
    get_weather_summary
)
from services.weather_ml_service import weather_ml_service


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

@router.get("/current", response_model=None)
async def get_current_weather_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current weather conditions from the latest sensor reading.

    Uses the most recent sensor reading for the authenticated user and
    runs ML weather classification to determine the current condition.

    **Authentication Required:** Yes

    **Returns:**
    - Current sensor-based weather data with ML classification
    - 404 if no sensor data exists for the user
    """
    # Get latest sensor reading for this user
    latest = (
        db.query(SensorReading)
        .filter(SensorReading.user_id == current_user.id)
        .order_by(SensorReading.timestamp.desc())
        .first()
    )

    if not latest:
        raise HTTPException(status_code=404, detail="No sensor data available")

    # Always run prediction to get fresh confidence/probability values
    features = {
        "temperature": latest.temperature,
        "relative_humidity": latest.relative_humidity,
        "rain": latest.rain,
        "wind_speed": latest.wind_speed,
        "soil_temperature": latest.soil_temperature,
        "soil_moisture": latest.soil_moisture,
        "solar_radiation": latest.solar_radiation,
    }
    prediction = weather_ml_service.predict(features)

    weather_condition = latest.weather_condition or prediction.condition

    return CurrentSensorWeatherResponse(
        source="sensor",
        weather_condition=weather_condition,
        confidence=prediction.confidence,
        probabilities=prediction.probabilities,
        temperature=latest.temperature,
        relative_humidity=latest.relative_humidity,
        rain=latest.rain,
        wind_speed=latest.wind_speed,
        soil_temperature=latest.soil_temperature,
        soil_moisture=latest.soil_moisture,
        solar_radiation=latest.solar_radiation,
        weather_code=latest.weather_code,
        timestamp=latest.timestamp,
        model_loaded=prediction.model_loaded,
    )


@router.get("/historical", response_model=HistoricalWeatherResponse)
async def get_historical_weather_endpoint(
    period: str = Query("24h", description="Period: '24h', '7d', or 'custom'"),
    start_date: Optional[str] = Query(None, description="Start date (ISO format) for custom period"),
    end_date: Optional[str] = Query(None, description="End date (ISO format) for custom period"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get historical weather data from sensor readings.

    **Authentication Required:** Yes

    **Query Parameters:**
    - period: '24h', '7d', or 'custom' (default '24h')
    - start_date: ISO datetime string (required for custom period)
    - end_date: ISO datetime string (required for custom period)

    **Returns:**
    - List of sensor readings within the period
    - Summary statistics (avg/max/min temp, avg humidity, total rain, condition breakdown)
    """
    now = datetime.now(timezone.utc)

    if period == "24h":
        start = now - timedelta(hours=24)
        end = now
    elif period == "7d":
        start = now - timedelta(days=7)
        end = now
    elif period == "custom":
        if not start_date or not end_date:
            raise HTTPException(
                status_code=400,
                detail="start_date and end_date are required for custom period"
            )
        try:
            start = datetime.fromisoformat(start_date)
            end = datetime.fromisoformat(end_date)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Use ISO format (e.g. 2025-01-01T00:00:00)"
            )
        # Ensure timezone-aware
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
        if end.tzinfo is None:
            end = end.replace(tzinfo=timezone.utc)
        if (end - start).days > 30:
            raise HTTPException(
                status_code=400,
                detail="Custom period cannot exceed 30 days"
            )
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid period. Use '24h', '7d', or 'custom'"
        )

    readings = (
        db.query(SensorReading)
        .filter(
            SensorReading.user_id == current_user.id,
            SensorReading.timestamp >= start,
            SensorReading.timestamp <= end,
        )
        .order_by(SensorReading.timestamp.asc())
        .all()
    )

    # Build readings list
    reading_items = [
        SensorWeatherReading(
            timestamp=r.timestamp,
            temperature=r.temperature,
            relative_humidity=r.relative_humidity,
            rain=r.rain,
            wind_speed=r.wind_speed,
            soil_temperature=r.soil_temperature,
            soil_moisture=r.soil_moisture,
            solar_radiation=r.solar_radiation,
            weather_code=r.weather_code,
            weather_condition=r.weather_condition,
        )
        for r in readings
    ]

    # Calculate summary
    if readings:
        temps = [r.temperature for r in readings]
        humidities = [r.relative_humidity for r in readings]
        rains = [r.rain for r in readings]
        conditions = [r.weather_condition for r in readings if r.weather_condition]

        condition_counts = dict(Counter(conditions))
        dominant = max(condition_counts, key=condition_counts.get) if condition_counts else None

        summary = HistoricalSummary(
            avg_temperature=round(sum(temps) / len(temps), 2),
            max_temperature=max(temps),
            min_temperature=min(temps),
            avg_humidity=round(sum(humidities) / len(humidities), 2),
            total_rain=round(sum(rains), 2),
            dominant_condition=dominant,
            condition_breakdown=condition_counts,
        )
    else:
        summary = HistoricalSummary(
            avg_temperature=0.0,
            max_temperature=0.0,
            min_temperature=0.0,
            avg_humidity=0.0,
            total_rain=0.0,
            dominant_condition=None,
            condition_breakdown={},
        )

    return HistoricalWeatherResponse(
        period=period,
        start=start,
        end=end,
        readings_count=len(readings),
        readings=reading_items,
        summary=summary,
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
